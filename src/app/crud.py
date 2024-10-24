from fastapi import HTTPException, status
from notion_client import Client
from typing import Optional
from ..app.config import settings
from .schemas import PageCreateDTO, PageUpdateDTO, PageResponseDTO, PagesResponseDTO

notion = Client(auth=settings.notion.api_key)

database_id = settings.notion.database_id

api_key = settings.notion.api_key


def create_notion_page(page: PageCreateDTO) -> PageResponseDTO:
    try:
        new_page = {
            "parent": {"database_id": database_id},
            "properties": {
                "Pages": {"title": [{"text": {"content": page.title}}]},
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": page.content}}
                        ]
                    },
                }
            ],
        }
        response = notion.pages.create(**new_page)
        return PageResponseDTO(
            id=response["id"], title=page.title, content=page.content
        )
    except Exception as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )


def get_notion_page_by_id(page_id: str) -> PageResponseDTO:
    try:
        response = notion.pages.retrieve(page_id=page_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Page not found",
            )
        title = response["properties"]["Pages"]["title"][0]["text"]["content"]
        content = response["children"][0]["paragraph"]["rich_text"][0]["text"][
            "content"
        ]
        return PageResponseDTO(id=response["id"], title=title, content=content)
    except Exception as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )


def update_notion_page(page_id: str, page: PageUpdateDTO) -> PageResponseDTO:
    try:
        updated_page = {
            "properties": {
                "Pages": (
                    {"title": [{"text": {"content": page.title}}]} if page.title else {}
                ),
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": page.content}}
                        ]
                    },
                }
            ],
        }
        response = notion.pages.update(page_id=page_id, **updated_page)
        return PageResponseDTO(
            id=response["id"], title=page.title or "", content=page.content
        )
    except Exception as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )


def delete_notion_page(page_id: str):
    try:
        notion.pages.update(page_id=page_id, archived=True)
        return f"Page {page_id} moved to trash successfully."
    except Exception as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )


def get_notion_pages(start_cursor=None, page_size=10):
    try:
        response = notion.databases.query(
            database_id=database_id, start_cursor=start_cursor, page_size=page_size
        )
        pages = [
            PageResponseDTO(
                id=page["id"],
                title=page["properties"]["Pages"]["title"][0]["text"]["content"],
                content="",
            )
            for page in response["results"]
        ]
        return PagesResponseDTO(results=pages)
    except Exception as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )
