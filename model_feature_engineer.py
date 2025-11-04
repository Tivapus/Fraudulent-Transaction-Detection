from sklearn.base import BaseEstimator, TransformerMixin

class AccountFeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass 

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        X['hour_of_day'] = X['time_ind'] % 24
        X['day'] = X['time_ind']//24

        X['src_ratio'] = X['amount'] / (X['src_bal'] + 1)
        X['dst_ratio'] = X['amount'] / (X['dst_bal'] + 1)
        return X
