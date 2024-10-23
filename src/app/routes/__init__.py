from fastapi import APIRouter
from app.config.config import settings

from .page import router as pages_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    pages_router,
    prefix=settings.api.v1.page,
)