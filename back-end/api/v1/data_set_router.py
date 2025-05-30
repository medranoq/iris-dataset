# Data_set router

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ...services import get_data_set
from ...schemas.data_set_schema import IrisDataSetResponse

router = APIRouter(
    prefix="/data-set",
    tags=["Data Set"]
)

@router.get("/")
async def iris_data_set(req: Request):

    iris_data = req.app.state.iris_data

    if iris_data is None:
        return JSONResponse(
            status_code=500,
            content={"message": "Iris dataset not loaded."}
        )
    response = IrisDataSetResponse(
        data=get_data_set(iris_data),
        metadata={
            "target_names": iris_data.target_names.tolist(),
            "feature_names": iris_data.feature_names,
            "description": iris_data.DESCR,
            "file_name": iris_data.filename,
            "data_module": iris_data.data_module,
            "shape": iris_data.data.shape,
        }
    )
    return JSONResponse(content=response.model_dump())
