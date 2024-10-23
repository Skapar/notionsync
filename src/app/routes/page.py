from fastapi import APIRouter, Depends

from app.repository.crud.page import create_notion_page
# ,update_notion_page, delete_notion_page, get_notion_pages
from app.schema.page import PageCreate
from app.db.db import get_sync_db
from auth.dependencies import get_current_user

router = APIRouter(tags=["Pages"])

@router.post("/notion/pages")
def create_page(page: PageCreate):
    return create_notion_page(page.title, page.content)


