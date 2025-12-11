from pydantic import BaseModel, Field
from typing import List, Optional


class PublicationBase(BaseModel):
    title: str
    kind: str
    keywords: List[str] = Field(default_factory=list)


class PublicationListItem(PublicationBase):
    _id: str
    authors: List[dict]


class PublicationDetail(PublicationListItem):
    pass
