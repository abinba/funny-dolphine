from fastapi import APIRouter

from .endpoints import (
    audiobook,
    category,
    settings,
    account,
    review,
    login_method,
    health,
    listening,
    shelf,
    chapter,
)

v1_router = APIRouter()

v1_router.include_router(health.router, prefix="/health", tags=["health"])
v1_router.include_router(
    login_method.router, prefix="/login_methods", tags=["login_methods"]
)
v1_router.include_router(account.router, prefix="/accounts", tags=["account"])
v1_router.include_router(audiobook.router, prefix="/audiobooks", tags=["audiobook"])
v1_router.include_router(chapter.router, prefix="/chapters", tags=["chapter"])
v1_router.include_router(category.router, prefix="/categories", tags=["category"])
v1_router.include_router(settings.router, prefix="/settings", tags=["settings"])
v1_router.include_router(review.router, prefix="/reviews", tags=["reviews"])
v1_router.include_router(shelf.router, prefix="/shelf", tags=["shelf"])
v1_router.include_router(listening.router, prefix="/listening", tags=["listening"])
