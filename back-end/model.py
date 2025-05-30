import joblib
from sklearn.datasets import load_iris

def load_iris_model():

    return joblib.load("back-end/iris_lg_r.pkl")


def load_iris_ds():
    return load_iris()
