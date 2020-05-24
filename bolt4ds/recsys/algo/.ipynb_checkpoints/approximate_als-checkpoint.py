
""" Models that use various Approximate Nearest Neighbours libraries in order to quickly
generate recommendations and lists of similar items.
See http://www.benfrederickson.com/approximate-nearest-neighbours-for-recommender-systems/
"""
import time
import sys
import numpy
import itertools
try:
    import annoy
except ImportError:
    print("The package 'annoy' is required to run this example.")
    sys.exit()

try:
    import nmslib
except ImportError:
    print("The package 'nmslib' is required to run this example.")
    sys.exit()

import numpy as np
from scipy.sparse import csr_matrix

from sklearn.base import BaseEstimator, TransformerMixin
import logging
log = logging.getLogger("recsys")



def augment_inner_product_matrix(factors):
    """ This function transforms a factor matrix such that an angular nearest neighbours search
    will return top related items of the inner product.
    This involves transforming each row by adding one extra dimension as suggested in the paper:
    "Speeding Up the Xbox Recommender System Using a Euclidean Transformation for Inner-Product
    Spaces" https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/XboxInnerProduct.pdf
    Basically this involves transforming each feature vector so that they have the same norm, which
    means the cosine of this transformed vector is proportional to the dot product (if the other
    vector in the cosine has a 0 in the extra dimension). """
    norms = numpy.linalg.norm(factors, axis=1)
    max_norm = norms.max()

    # add an extra dimension so that the norm of each row is the same
    # (max_norm)
    extra_dimension = numpy.sqrt(max_norm ** 2 - norms ** 2)
    return max_norm, numpy.append(factors, extra_dimension.reshape(norms.shape[0], 1), axis=1)


class AnnoyTransformer(TransformerMixin, BaseEstimator):
    """Wrapper for using annoy.AnnoyIndex as sklearn's KNeighborsTransformer"""

    def __init__(self, n_neighbors=5, metric='euclidean', n_trees=10,
                 search_k=-1,approximate_similar_items=True,approximate_recommend=True,
                 user_embeddings= None,item_embeddings=None):
        self.n_neighbors = n_neighbors
        self.n_trees = n_trees
        self.search_k = search_k
        self.metric = metric
        self.approximate_similar_items = approximate_similar_items
        self.approximate_recommend=approximate_recommend
        self.user_embeddings = user_embeddings
        self.item_embeddings = item_embeddings
    def fit(self, X):
        self.n_samples_fit_ = X.shape[0]
        metric = self.metric if self.metric != 'sqeuclidean' else 'euclidean'
        self.annoy_ = annoy.AnnoyIndex(X.shape[1], metric=metric)
        for i, x in enumerate(X):
            self.annoy_.add_item(i, x.tolist())
        self.annoy_.build(self.n_trees)
        
        #New add
        self.item_factors = X
        if self.approximate_similar_items:
            
            log.debug("Building annoy similar items index")
            self.similar_items_index = annoy.AnnoyIndex(
                self.item_factors.shape[1], 'angular')
            for i, row in enumerate(self.item_factors):
                self.similar_items_index.add_item(i, row)
            self.similar_items_index.build(self.n_trees)
            
        # build up a separate index for the inner product (for recommend
        # methods)
        if self.approximate_recommend:
            log.debug("Building annoy recommendation index")
            self.max_norm, extra = augment_inner_product_matrix(self.item_factors)
            self.recommend_index = annoy.AnnoyIndex(extra.shape[1], 'angular')
            for i, row in enumerate(extra):
                self.recommend_index.add_item(i, row)
            self.recommend_index.build(self.n_trees)

        return self

    def transform(self, X):
        return self._transform(X)

    def fit_transform(self, X, y=None):
        return self.fit(X)._transform(X=None)

    def _transform(self, X):
        """As `transform`, but handles X is None for faster `fit_transform`."""

        n_samples_transform = self.n_samples_fit_ if X is None else X.shape[0]

        # For compatibility reasons, as each sample is considered as its own
        # neighbor, one extra neighbor will be computed.
        n_neighbors = self.n_neighbors + 1

        indices = np.empty((n_samples_transform, n_neighbors),
                           dtype=np.int)
        distances = np.empty((n_samples_transform, n_neighbors))

        if X is None:
            for i in range(self.annoy_.get_n_items()):
                ind, dist = self.annoy_.get_nns_by_item(
                    i, n_neighbors, self.search_k, include_distances=True)

                indices[i], distances[i] = ind, dist
        else:
            for i, x in enumerate(X):
                indices[i], distances[i] = self.annoy_.get_nns_by_vector(
                    x.tolist(), n_neighbors, self.search_k,
                    include_distances=True)

        if self.metric == 'sqeuclidean':
            distances **= 2

        indptr = np.arange(0, n_samples_transform * n_neighbors + 1,
                           n_neighbors)
        kneighbors_graph = csr_matrix((distances.ravel(), indices.ravel(),
                                       indptr), shape=(n_samples_transform,
                                                       self.n_samples_fit_))

        return kneighbors_graph

    def similar_items(self, itemid, N=10):
        #if not self.approximate_similar_items:
        #    return super(AnnoyAlternatingLeastSquares, self).similar_items(itemid, N)

        neighbours, dist = self.similar_items_index.get_nns_by_item(itemid, N,
                                                                    search_k=self.search_k,
                                                                    include_distances=True)
        # transform distances back to cosine from euclidean distance
        return zip(neighbours, 1 - (numpy.array(dist) ** 2) / 2)

    def recommend(self, userid, user_items, N=10, filter_already_liked_items=True,
                  filter_items=None, recalculate_user=False):
        #if not self.approximate_recommend:
        #    return super(NMSLibAlternatingLeastSquares,
        #                 self).recommend(userid, user_items, N=N,
        #                                filter_items=filter_items,
        #                                 recalculate_user=recalculate_user)

        #user = self._user_factor(userid, user_items, recalculate_user)

        # calculate the top N items, removing the users own liked items from
        # the results
        liked = set()
        #user_items =interactions_matrix 
        
        if filter_already_liked_items:
            #liked.update(user_items[userid].indices)
            liked.update(user_items.tocsr()[userid].indices)
        if filter_items:
            liked.update(filter_items)
        count = N + len(liked)
        
        user = self.user_embeddings[userid]
        query = numpy.append(user, 0)
        ids, dist = self.recommend_index.get_nns_by_vector(query, count, include_distances=True,
                                                           search_k=self.search_k)

        # convert the distances from euclidean to cosine distance,
        # and then rescale the cosine distance to go back to inner product
        scaling = self.max_norm * numpy.linalg.norm(query)
        dist = scaling * (1 - (numpy.array(dist) ** 2) / 2)
        return list(itertools.islice((rec for rec in zip(ids, dist) if rec[0] not in liked), N))