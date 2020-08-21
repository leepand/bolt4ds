from .data.lightfm_data_process import Dataset
from .algo.lightfm_auto import LFMRecommender
from .algo.approximate_als import AnnoyTransformer
import numpy as np
from lightfm import LightFM
from sklearn.base import BaseEstimator, TransformerMixin

# maps command line model argument to class name
MODELS = {"annoy_als": AnnoyTransformer,
          "lmf":LFMRecommender}


def get_model(model_name):
    print("getting model %s" % model_name)
    model_class = MODELS.get(model_name)
    if not model_class:
        raise ValueError("Unknown Model '%s'" % model_name)

    # some default params
    if issubclass(model_class, TransformerMixin):
        params = {}
    elif model_name == "bm25":
        params = {'K1': 100, 'B': 0.5}
    elif model_name == "bpr":
        params = {'factors': 63}
    elif model_name == "lmf":
        params = {'factors': 30, "iterations": 40, "regularization": 1.5}
    else:
        params = {}

    return model_class#(**params)






class TrainLightFM:
    def __init__(self):
        pass
        
    def train_test_split(self, interactions, weights):
        train_interactions, test_interactions = \
        cross_validation.random_train_test_split(
            interactions, 
            random_state=np.random.RandomState(2019))
        
        train_weights, test_weights = \
        cross_validation.random_train_test_split(
            weights, 
            random_state=np.random.RandomState(2019))
        return train_interactions,\
    test_interactions, train_weights, test_weights
    
    def fit(self, interactions, weights,
            item_features, user_features,
            cross_validation=False,no_components=150,
            learning_rate=0.05,
            loss='warp',
            random_state=2019,
            verbose=True,
            num_threads=4, epochs=5):
        ################################
        # Model building part
        ################################

        # define lightfm model by specifying hyper-parametre
        # then fit the model with ineteractions matrix,
        # item and user features
        
        model = LightFM(
            no_components,
            learning_rate,
            loss=loss,
            random_state=random_state)
        model.fit(
            interactions,
            item_features=item_features,
            user_features=user_features, sample_weight=weights,
            epochs=epochs, num_threads=num_threads, verbose=verbose)
        
        return model