from pydantic import BaseModel, Field
from typing import Optional, List

class DepartmentBase(BaseModel):
    name: str = Field(..., example="School of Computer Science and Digital Technologies")
    slug: str = Field(..., example="school-of-computer-science-and-digital-technologies")
    type: Optional[str] = Field(None, example="school")
    description: Optional[str] = Field(None, example="Description of department")
    isComputerScienceRelated: Optional[bool] = Field(True, example=True)

class DepartmentListItem(BaseModel):
    _id: str
    name: str
    slug: str

class DepartmentDetail(BaseModel):
    _id: str
    name: str
    slug: str
    # faculties list — but we represent minimal info here; full faculty endpoint for details
    faculties: List[dict]
