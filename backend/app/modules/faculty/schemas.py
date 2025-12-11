from pydantic import BaseModel, Field
from typing import Optional, List


class FacultyListItem(BaseModel):
    _id: str
    name: str
    position: Optional[str]


class FacultyDetail(BaseModel):
    _id: str
    name: str
    position: Optional[str]
    researchInterest: Optional[str]
    departments: List[dict]
    articles: List[dict]
    conferencePapers: List[dict]
