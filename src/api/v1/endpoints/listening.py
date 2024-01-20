from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.listening import ListeningRepo
from src.schemas.listening import ListeningSchema

router = APIRouter()


@router.get("/", response_model=list[ListeningSchema])
async def get_listening(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ListeningRepo.all(session)


@router.get("/", response_model=list[ListeningSchema])
async def get_listening_by_account_id_and_audiobook_id(
        request: Request,
        account_id: int,
        audiobook_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ListeningRepo.get(session,
                                   account_id=account_id,
                                   audiobook_id=audiobook_id)


@router.post("/", response_model=list[ListeningSchema])
async def create_review(
        request: Request,
        client_id: int,
        audiobook_id: int,
        current_chapter_id: int,
        start_time: datetime,
        last_access_time: datetime,
        finish_time: datetime,
        is_favorite: bool,
        session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ListeningRepo.create(session,
                                      client_id=client_id,
                                      audiobook_id=audiobook_id,
                                      current_chapter_id=current_chapter_id,
                                      start_time=start_time,
                                      last_access_time=last_access_time,
                                      finish_time=finish_time,
                                      is_favorite=is_favorite)
