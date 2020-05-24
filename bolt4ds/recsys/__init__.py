from .data.lightfm_data_process import Dataset
from .algo.lightfm_auto import LFMRecommender
from .algo.approximate_als import AnnoyTransformer


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
