from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import is_authenticated, is_authorized
from src.db import get_async_session
from src.repo.account import AccountRepo
from src.repo.audiobook import AudiobookRepo
from src.schemas.audiobook import AudiobookSchema

router = APIRouter()


@router.get("/", response_model=list[AudiobookSchema])
async def get_audiobooks(
    request: Request,
    category_id: Optional[int] = None,
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    is_authenticated(auth_header)
    return await AudiobookRepo.all(session, category_id=category_id, limit=limit)


@router.get("/recently_listened", response_model=list[AudiobookSchema])
async def recently_listened_audiobooks(
    request: Request,
    account_id: int,
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    payload = is_authenticated(request.headers.get("Authorization"))
    is_authorized(payload, account_id)
    if not await AccountRepo.exists(session, account_id=account_id):
        raise HTTPException(
            status_code=400,
            detail=f"User with account_id '{account_id}' doesn't exist.",
        )

    return await AudiobookRepo.recently_listened(
        session, account_id=account_id, limit=limit
    )


@router.get("/popular", response_model=list[AudiobookSchema])
async def popular_audiobooks(
    request: Request,
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    is_authenticated(auth_header)
    return await AudiobookRepo.all(session, popular=True, limit=limit)


@router.get("/search", response_model=list[AudiobookSchema])
async def search_audiobooks(
    request: Request,
    search_query: str,
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    is_authenticated(auth_header)
    return await AudiobookRepo.search(session, search_query=search_query, limit=limit)


@router.get("/{audiobook_id}", response_model=AudiobookSchema)
async def get_audiobook(
    request: Request,
    audiobook_id: int = None,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    is_authenticated(auth_header)
    return await AudiobookRepo.get(session, audiobook_id=audiobook_id)
