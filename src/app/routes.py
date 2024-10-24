from fastapi import APIRouter, Depends, HTTPException

from .crud import create_notion_page, update_notion_page, delete_notion_page, get_notion_pages
from .schemas import PageCreate, PageUpdate
from ..auth.dependencies import get_current_user
from ..app.config import settings

from ..auth.models import User

router = APIRouter(prefix=settings.api.v1.prefix, tags=["pages"])

router.include_router(
    router,
    prefix=settings.api.v1.page,
)


@router.post("/notion/pages")
def create_page(page: PageCreate, current_user: User = Depends(get_current_user)):
    return create_notion_page(page.title, page.content)

@router.put("/notion/pages/{page_id}")
def edit_page(page_id: str, page: PageUpdate, current_user: User = Depends(get_current_user)):
    try:
        return update_notion_page(page_id, page.title, page.content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/notion/pages/{page_id}")
def delete_page(page_id: str, current_user: User = Depends(get_current_user)):
    delete_notion_page(page_id)
    return {"detail": "Page deleted"}

@router.get("/notion/pages")
def retrieve_pages(start_cursor: str = None, page_size: int = 10):
    pages = get_notion_pages(start_cursor=start_cursor, page_size=page_size)
    return pages
