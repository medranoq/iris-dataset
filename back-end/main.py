from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from .model import load_iris_model, load_iris_ds
from .schema import IrisResponse
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # o ["*"] para permitir todo (menos seguro)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="back-end/static"), name="static")

@app.get("/")
async def root():
    return {"message": "Service is running!"}


@app.get("/iris")
async def iris_data_set():
    return JSONResponse(
        content={
            "data": get_data_set(),
            "metadata": {
                "target_names": app.state.iris_data.target_names.tolist(),
                "feature_names": app.state.iris_data.feature_names,
                "description": app.state.iris_data.DESCR,
                "file_name": app.state.iris_data.filename,
                "data_module": app.state.iris_data.data_module,
                "shape": app.state.iris_data.data.shape,
            }
        }
    )

@app.get("/spices/{target}")
async def iris_data_set_by_target(target: int):
    data = get_data_set()

    if target < 0 or target >= len(app.state.iris_data.target_names):
        return JSONResponse(
            status_code=404,
            content={"message": "Target not found"}
        )

    filtered_data = [item for item in data if item["target"] == target]

    return JSONResponse(
        content={
            "data": filtered_data,
            "metadata": {
                "size": len(filtered_data),
                "target": target,
                "target_name": app.state.iris_data.target_names[target],
            }
        }
    )

@app.get("/spices")
async def iris_target_names():

    target_names = app.state.iris_data.target_names.tolist()
    spices = [
        {
            "target": idx,
            "target_name": name.capitalize(),
            "image_url": f"/static/{idx}.jpg"  #
        }
        for idx, name in enumerate(target_names)
    ]
    return JSONResponse(content={"spices": spices})

@app.post("/predict")
async def predict(iris: IrisResponse):

    features = np.array([[iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]])

    target = app.state.model.predict(features).tolist()[0]

    return JSONResponse(
        content={
            "prediction": app.state.iris_data.target_names[target],
        }
    )


