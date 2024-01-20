from fastapi import APIRouter

from .endpoints import (
    audiobook,
    category,
    settings,
    account,
    chapter,
    user_audiobook,
    review,
)

v1_router = APIRouter()

v1_router.include_router(audiobook.router, prefix="/audiobooks", tags=["audiobook"])
v1_router.include_router(category.router, prefix="/categories", tags=["category"])
v1_router.include_router(settings.router, prefix="/settings", tags=["settings"])
v1_router.include_router(account.router, prefix="/accounts", tags=["account"])
v1_router.include_router(
    chapter.router, prefix="/audiobook_chapters", tags=["audiobook_chapters"]
)
v1_router.include_router(
    user_audiobook.router, prefix="/user_audiobook", tags=["user_audiobook"]
)
v1_router.include_router(review.router, prefix="/reviews", tags=["reviews"])
