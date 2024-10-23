from notion_client import Client
from app.config import settings
import os

notion = Client(auth=settings.API_KEY)

database_id = settings.DATABASE_ID

api_key = settings.API_KEY

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
                    "rich_text": [
                        {"type": "text", "text": {"content": content}}
                    ]
                },
            }
        ],
    }
    response = notion.pages.create(**new_page)
    return response