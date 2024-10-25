from fastapi import APIRouter, Depends, HTTPException

from .crud import (
    create_notion_page,
    update_notion_page,
    delete_notion_page,
    get_notion_pages,
)
from ..auth.dependencies import get_current_user
from ..app.config import settings
from .schemas import PageCreateDTO, PageUpdateDTO, PageResponseDTO, PagesResponseDTO

from ..auth.models import User

router = APIRouter(prefix=settings.api.v1.prefix, tags=["pages"])

router.include_router(
    router,
    prefix=settings.api.v1.page,
)


@router.post("/notion/pages", response_model=PageResponseDTO)
def create_page(page: PageCreateDTO, current_user: User = Depends(get_current_user)):
    return create_notion_page(page)


@router.put("/notion/pages/{page_id}", response_model=PageResponseDTO)
def edit_page(
    page_id: str, page: PageUpdateDTO, current_user: User = Depends(get_current_user)
):
    return update_notion_page(page_id, page)


@router.delete("/notion/pages/{page_id}")
def delete_page(page_id: str, current_user: User = Depends(get_current_user)):
    return delete_notion_page(page_id)


@router.get("/notion/pages")
def retrieve_pages(skip: int = 0, take: int = 10, User = Depends(get_current_user)):
    return get_notion_pages(skip, take)
