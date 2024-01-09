from fastapi import Depends, Request, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.user_chapter import UserChapterRepo

router = APIRouter()


@router.get("/{account_id}/{chapter_id}/")
async def get_user_chapter(
    request: Request,
    account_id: int,
    chapter_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await UserChapterRepo.get(
        session, account_id=account_id, chapter_id=chapter_id
    )


@router.get("/{account_id}/{chapter_id}/explored/")
async def set_explored(
    request: Request,
    account_id: int,
    chapter_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    await UserChapterRepo.set_explored(
        session, account_id=account_id, chapter_id=chapter_id
    )
    return {"message": "success"}
