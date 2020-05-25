import logging

from sklearn.base import TransformerMixin


class DataMonitor:
    _max_warning = 'found {howmany:d} runtime value(s) for feature "{feature}" greater than trained max.'
    _min_warning = 'found {howmany:d} runtime value(s) for feature "{feature}" less than trained min.'
    _categorical_warning = 'found {howmany:d} categorical runtime value(s) for feature "{feature}" ' \
                            'not in training data: {values!r}.'

    def __init__(self):
        self._schema = None

    def analyze(self, X):
        self._schema = {}
        self._fit_numeric(X)
        self._fit_categorical(X)

    def validate(self, X):
        if self._schema is None:
            raise RuntimeError('must call .fit() before .transform()')
        self._validate_numeric(X)
        self._validate_categoricals(X)
        
    @property
    def schema(self):
        # dicts are mutable, return something safe
        return self._schema.copy()
        
    def _fit_numeric(self, X):
        maxes = X.max(numeric_only=True)
        mins = X.min(numeric_only=True)
        self._schema['numeric'] = {'maxes': maxes, 'mins': mins}

    def _fit_categorical(self, X):
        self._schema['categoricals'] = {}
        for col, vals in X.select_dtypes(object).iteritems():
            self._schema['categoricals'][col] = vals.unique()
            
    def _validate_numeric(self, X):
        self._validate_maxes(X)
        self._validate_mins(X)
    
    def _validate_maxes(self, X):
        for col, fit_max in self._schema['numeric']['maxes'].items():
            over = (X[col] > fit_max)
            if over.any():
                self._log_warning(
                    self._max_warning.format(howmany=over.sum(), feature=col))
    
    def _validate_mins(self, X):
        for col, fit_min in self._schema['numeric']['mins'].items():
            under = (X[col] < fit_min)
            if under.any():
                self._log_warning(
                    self._min_warning.format(howmany=under.sum(), feature=col))

    def _validate_categoricals(self, X):
        for col, fit_vals in self._schema['categoricals'].items():
            new_vals = ~X[col].isin(fit_vals)
            if new_vals.any():
                values = X.loc[new_vals, col].unique().tolist()
                self._log_warning(
                    self._categorical_warning.format(howmany=new_vals.sum(), feature=col, values=values))
                
    def _log_warning(self, message):
        logging.getLogger(__name__).warning(message)


class DataMonitorTransformer(TransformerMixin):
    def __init__(self):
        self.data_monitor = DataMonitor()

    def fit(self, X, y=None):
        self.data_monitor.analyze(X)
        return self

    def transform(self, X, y=None):
        self.data_monitor.validate(X)
        return X
