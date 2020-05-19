import pandas as pd
try:
    from tensorflow.python.keras.engine.saving import load_model
except:
    from tensorflow.keras.models import load_model
from bolt4ds.flow.targets import DataTarget

class H5PandasTarget(DataTarget):
    def load(self, cached=False, **kwargs):
        opts = {**{'key':'data'},**kwargs}
        return super().load(pd.read_hdf, cached, **opts)

    def save(self, df, **kwargs):
        opts = {**{'key':'data'},**kwargs}
        return super().save(df, 'to_hdf', **opts)

class H5KerasTarget(DataTarget):
    def load(self, cached=False, **kwargs):
        return super().load(load_model, cached, **kwargs)

    def save(self, df, **kwargs):
        return super().save(df, 'save', **kwargs)