from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel


class PageCreateDTO(BaseModel):
    title: str
    content: str

class PageUpdateDTO(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = ""

class PageResponseDTO(BaseModel):
    id: str
    title: str
    content: str

class PagesResponseDTO(BaseModel):
    results: List[PageResponseDTO]
