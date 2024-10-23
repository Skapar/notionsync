from fastapi import APIRouter, Depends

from .crud import create_notion_page
# ,update_notion_page, delete_notion_page, get_notion_pages
from .schemas import PageCreate
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
