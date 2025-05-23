from pydantic import BaseModel

class IrisResponse(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    class Config:
        from_attributes = True