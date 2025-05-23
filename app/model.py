import joblib
from sklearn.datasets import load_iris



def load_iris_model():

    return  joblib.load("app/iris_lg_r.pkl")


def load_iris_ds():
    return load_iris()
