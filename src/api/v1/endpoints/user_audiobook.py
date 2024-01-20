from fastapi import Depends, Request, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.user_audiobook import UserAudiobookRepo

router = APIRouter()


@router.get("/{account_id}/{audiobook_id}/")
async def get_user_audiobook_info(
    request: Request,
    account_id: int,
    audiobook_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)

    await UserAudiobookRepo.set_listened_times(
        session,
        account_id=account_id,
        audiobook_id=audiobook_id,
        chapter_id=None,
    )

    return await UserAudiobookRepo.all(
        session,
        account_id=account_id,
        audiobook_id=audiobook_id
    )


@router.post("/{account_id}/{audiobook_id}/{chapter_id}/explored/")
async def set_explored(
    request: Request,
    account_id: int,
    audiobook_id: int,
    chapter_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    await UserAudiobookRepo.set_explored(
        session,
        account_id=account_id,
        audiobook_id=audiobook_id,
        chapter_id=chapter_id
    )
    return {"message": "success"}
