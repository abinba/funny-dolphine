from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.review import ReviewRepo
from src.schemas.review import ReviewSchema
from datetime import datetime
from typing import Literal

router = APIRouter()


@router.get("/", response_model=list[ReviewSchema])
async def get_reviews(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ReviewRepo.all(session)


@router.get("/account/{account_id}", response_model=list[ReviewSchema])
async def get_reviews_by_account_id(
        request: Request,
        account_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ReviewRepo.get(session, account_id=account_id)


@router.get("/audiobook/{audiobook_id}", response_model=list[ReviewSchema])
async def get_reviews_by_audiobook_id(
        request: Request,
        audiobook_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ReviewRepo.get(session, audiobook_id=audiobook_id)


@router.post("/", response_model=list[ReviewSchema])
async def create_review(
        request: Request,
        client_id: int,
        audiobook_id: int,
        rating_value: Literal[1, 2, 3, 4, 5],
        rating_date: datetime,
        review_content: str,
        session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ReviewRepo.create(session,
                                   client_id=client_id,
                                   audiobook_id=audiobook_id,
                                   rating_value=rating_value,
                                   rating_date=rating_date,
                                   review_content=review_content)
