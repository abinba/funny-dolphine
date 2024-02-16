from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import is_authenticated, is_authorized
from src.db import get_async_session
from src.repo.audiobook import AudiobookRepo
from src.repo.listening import ListeningRepo
from src.schemas.listening import ListeningSchema

router = APIRouter()


@router.get("/", response_model=list[ListeningSchema])
async def get_listening_by_account_id_and_audiobook_id(
    request: Request,
    account_id: int,
    audiobook_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    payload = is_authenticated(request.headers.get("Authorization"))
    is_authorized(payload, account_id)

    return await ListeningRepo.get(
        session, account_id=account_id, audiobook_id=audiobook_id
    )


# When user starts listening to an audiobook, create a new listening entry.
@router.post("/")
async def create_listening(
    request: Request,
    account_id: int,
    audiobook_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    payload = is_authenticated(request.headers.get("Authorization"))
    is_authorized(payload, account_id)

    audiobook = await AudiobookRepo.get(session, audiobook_id=audiobook_id)
    if not audiobook:
        raise HTTPException(
            status_code=409,
            detail=f"Audiobook with audiobook_id '{audiobook_id}' doesn't exist.",
        )

    current_chapter_id = audiobook.first_chapter_id

    return await ListeningRepo.create(
        session,
        account_id=account_id,
        audiobook_id=audiobook_id,
        current_chapter_id=current_chapter_id,
    )


# When user stops at certain chapter, update the current_chapter_id.
# TODO: if the chapter is the last chapter, set the finish_time.
@router.put("/")
async def update_chapter(
    request: Request,
    account_id: int,
    audiobook_id: int,
    current_chapter_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    payload = is_authenticated(request.headers.get("Authorization"))
    is_authorized(payload, account_id)

    return await ListeningRepo.update_chapter(
        session,
        account_id=account_id,
        audiobook_id=audiobook_id,
        current_chapter_id=current_chapter_id,
    )
