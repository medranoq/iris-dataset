from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.model import load_iris_model, load_iris_ds
from schema import IrisResponse
from .services import get_data_set
import numpy as np



@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Load the model and dataset

        app.state.model = load_iris_model()
        app.state.iris_data = load_iris_ds()

        print("Resources loaded successfully.")
        yield
    finally:
        print("Application shutting down...")


app = FastAPI(
    title="Iris Prediction API",
    description="Iris Flower Prediction API.",
    version="0.0.1",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/iris")
async def iris_data_set():
    return JSONResponse(
        content={
            "data": get_data_set(),
            "metadata": {
                "feature_names": app.state.iris_data.feature_names,
                "description": app.state.iris_data.DESCR,
                "file_name": app.state.iris_data.filename,
                "data_module": app.state.iris_data.data_module,
                "shape": app.state.iris_data.data.shape,
            }
        }
    )

@app.get("/iris/{target}")
async def iris_data_set_by_target(target: int):
    data = get_data_set()
    filtered_data = [item for item in data if item["target"] == target]

    return JSONResponse(
        content={
            "data": filtered_data,
            "metadata": {
                "shape": app.state.iris_data.data.shape,
            }
        }
    )
@app.post("/predict")
async def predict(iris: IrisResponse):

    features = np.array([[iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]])

    target = app.state.model.predict(features).tolist()

    return JSONResponse(
        content={
            "prediction": app.state.iris_data.target_names[target[0]],
        }
    )


