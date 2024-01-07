from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.audiobook import AudiobookRepo
from src.schemas.audiobook import AudiobookSchema

router = APIRouter()


@router.get("/", response_model=list[AudiobookSchema])
async def get_audiobooks(
    request: Request,
    category_id: int = None,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await AudiobookRepo.all(session, category_id=category_id)


@router.get("/{audiobook_id}", response_model=AudiobookSchema)
async def get_audiobooks(
    request: Request,
    audiobook_id: int = None,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await AudiobookRepo.get(session, audiobook_id=audiobook_id)
