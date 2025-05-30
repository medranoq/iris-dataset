from pydantic import BaseModel
from typing import List, Dict, Union, Tuple

class Metadata(BaseModel):
    target_names: List[str]
    feature_names: List[str]
    description: str
    file_name: str
    data_module: str
    shape: Tuple[int, int]

class IrisDataSetResponse(BaseModel):
    data: List[Dict[str, Union[float, str]]]
    metadata: Metadata
