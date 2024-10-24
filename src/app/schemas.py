from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel


class PageCreate(BaseModel):
    title: str
    content: str

class PageUpdate(BaseModel):
    title: str
    content: str

class PageResponse(BaseModel):
    id: str
    title: str
    content: str
    notion_id: str


class PageListResponse(BaseModel):
    pages: List[PageResponse]
    next_cursor: Optional[str]
    has_more: bool
