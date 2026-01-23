from typing import List,Literal,Optional
from pydantic import BaseModel
from datetime import datetime

class DataElementCreate(BaseModel):
    name: str
    data_type: Literal["string","integer","float","boolean","date","datetime"]
    is_required: bool = False
    is_pii: bool = False


class DataElementResponse(DataElementCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DatasetCreate(BaseModel):
    name: str
    description: str = ""


class DatasetResponse(DatasetCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DatasetResponsewithElements(DatasetCreate):
    id: int
    created_at: datetime
    elements: List[DataElementResponse] = []

    class Config:
        from_attributes = True

class DatasetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class DataElementUpdate(BaseModel):
    name: Optional[str] = None
    data_type: Optional[Literal["string", "integer", "float", "boolean", "date", "datetime"]] = None
    is_required: Optional[bool] = None
    is_pii: Optional[bool] = None

