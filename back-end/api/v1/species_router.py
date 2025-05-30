# Species router
from ...services import get_data_set
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/species",
    tags=["Species"]
)

@router.get("/")
async def iris_target_names(req: Request):
    target_names = req.app.state.iris_data.target_names.tolist()
    spices = [
        {
            "target": idx,
            "target_name": name.capitalize(),
            "image_url": f"/static/{idx}.jpg"
        }
        for idx, name in enumerate(target_names)
    ]
    return JSONResponse(content={"spices": spices})


@router.get("/{target}")
async def iris_data_set_by_target(req: Request, target: int):
    iris_data = req.app.state.iris_data
    data = get_data_set(iris_data)
    target_names = iris_data.target_names

    if target < 0 or target >= len(target_names):
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
                "target_name": target_names[target],
            }
        }
    )
