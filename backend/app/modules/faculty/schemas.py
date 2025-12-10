from pydantic import BaseModel, Field
from typing import Optional, List

class FacultyBase(BaseModel):
    name: str = Field(..., example="Alice Smith")
    position: Optional[str] = Field(None, example="Lecturer")
    researchInterest: Optional[str] = None
    departmentIds: Optional[List[str]] = None
    articleIds: Optional[List[str]] = None
    conferencePaperIds: Optional[List[str]] = None

class FacultyDetail(BaseModel):
    _id: str
    name: str
    position: Optional[str]
    researchInterest: Optional[str]
    departments: List[dict]  # minimal dept info: _id, name, slug
    articles: Optional[List[dict]]
    conferencePapers: Optional[List[dict]]
