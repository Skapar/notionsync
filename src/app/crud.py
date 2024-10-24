from fastapi import HTTPException, status
from notion_client import Client
from ..app.config import settings
from uuid import UUID
from notion_client.errors import APIResponseError

notion = Client(auth=settings.notion.api_key)

database_id = settings.notion.database_id

api_key = settings.notion.api_key


def create_notion_page(title: str, content: str):
    new_page = {
        "parent": {"database_id": database_id},
        "properties": {
            "Pages": {"title": [{"text": {"content": title}}]},
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                },
            }
        ],
    }
    response = notion.pages.create(**new_page)
    return response

def get_notion_page_by_id(page_id: str):
    response = notion.pages.retrieve(page_id=page_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )
    return response

def update_notion_page(page_id: str, title: str, content: str):
    updated_page = {
        "properties": {
            "Pages": {"title": [{"text": {"content": title}}]},
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                },
            }
        ],
    }
    response = notion.pages.update(page_id=page_id, **updated_page)
    return response

def delete_notion_page(page_id: str):
    page = get_notion_page_by_id(page_id=page_id)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found",
        )
    notion.pages.update(page_id=page_id, in_trash=True)
    
def get_notion_pages(start_cursor=None, page_size=10):
    response = notion.databases.query(
        database_id=database_id,
        start_cursor=start_cursor,
        page_size=page_size
    )
    return response
