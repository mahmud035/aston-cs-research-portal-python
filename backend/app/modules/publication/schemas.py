from pydantic import BaseModel, Field
from typing import List, Optional

class PublicationBase(BaseModel):
    title: str = Field(..., example="Artificial intelligence-enabled predictive modelling in psychiatry: overview of machine learning applications in mental health research")
    kind: str = Field(..., example="article")  # e.g. "article" or "conference"
    keywords: Optional[List[str]] = Field(default_factory=list)

class PublicationListItem(PublicationBase):
    _id: str
    authors: Optional[List[dict]]  # minimal author info: _id, name, position

class PublicationDetail(PublicationListItem):
    # could add more fields if you store them, e.g. 'source', 'createdAt', etc.
    pass
