from notion_client import Client
from app.config import settings
import os

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
