from pydantic import BaseModel, Field
from typing import Optional


class DepartmentListItem(BaseModel):
    _id: str
    name: str
    slug: str


class DepartmentDetail(BaseModel):
    _id: str
    name: str
    slug: str
    type: Optional[str]
    description: Optional[str]
    isComputerScienceRelated: Optional[bool]
