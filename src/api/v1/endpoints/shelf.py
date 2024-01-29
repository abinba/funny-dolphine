from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import is_authenticated, is_authorized
from src.db import get_async_session
from src.repo.account import AccountRepo
from src.repo.audiobook import AudiobookRepo
from src.repo.shelf import ShelfRepo
from src.schemas.audiobook import AudiobookSchema

router = APIRouter()


@router.get("/{account_id}", response_model=list[AudiobookSchema])
async def get_shelf_by_account_id(
    request: Request,
    account_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    payload = is_authenticated(request.headers.get("Authorization"))
    is_authorized(payload, account_id)

    if not AccountRepo.exists(session, account_id=account_id):
        raise HTTPException(
            status_code=409,
            detail=f"User with account_id '{account_id}' doesn't exist.",
        )

    return await ShelfRepo.get_audiobooks(session, account_id=account_id)


@router.post("/")
async def add_to_shelf(
    request: Request,
    account_id: int,
    audiobook_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    payload = is_authenticated(request.headers.get("Authorization"))
    is_authorized(payload, account_id)

    if not AccountRepo.exists(session, account_id=account_id):
        raise HTTPException(
            status_code=409,
            detail=f"User with account_id '{account_id}' doesn't exist.",
        )

    if not AudiobookRepo.exists(session, audiobook_id=audiobook_id):
        raise HTTPException(
            status_code=409,
            detail=f"Audiobook with audiobook_id '{audiobook_id}' doesn't exist.",
        )

    return await ShelfRepo.create_or_update(
        session,
        account_id=account_id,
        audiobook_id=audiobook_id,
    )


@router.delete("/")
async def remove_from_shelf(
    request: Request,
    account_id: int,
    audiobook_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    payload = is_authenticated(request.headers.get("Authorization"))
    is_authorized(payload, account_id)

    if not AccountRepo.exists(session, account_id=account_id):
        raise HTTPException(
            status_code=409,
            detail=f"User with account_id '{account_id}' doesn't exist.",
        )

    if not AudiobookRepo.exists(session, audiobook_id=audiobook_id):
        raise HTTPException(
            status_code=409,
            detail=f"Audiobook with audiobook_id '{audiobook_id}' doesn't exist.",
        )

    await ShelfRepo.remove_from_shelf(
        session,
        account_id=account_id,
        audiobook_id=audiobook_id,
    )

    return {"message": "success"}
