from fastapi import APIRouter

from .endpoints import audiobook, category, settings, account

v1_router = APIRouter()

v1_router.include_router(audiobook.router, prefix="/audiobooks", tags=["audiobook"])
v1_router.include_router(category.router, prefix="/categories", tags=["category"])
v1_router.include_router(settings.router, prefix="/settings", tags=["settings"])
v1_router.include_router(account.router, prefix="/account", tags=["settings"])
