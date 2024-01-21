from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.review import ReviewRepo
from src.schemas.review import ReviewSchema
from datetime import datetime
from src.repo.account import AccountRepo
from src.repo.audiobook import AudiobookRepo

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
    return await ReviewRepo.get_by_attribute(session, account_id=account_id)


@router.get("/audiobook/{audiobook_id}", response_model=list[ReviewSchema])
async def get_reviews_by_audiobook_id(
    request: Request,
    audiobook_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ReviewRepo.get_by_attribute(session, audiobook_id=audiobook_id)


@router.post("/", response_model=ReviewSchema)
async def create_review(
    request: Request,
    account_id: int,
    audiobook_id: int,
    rating_value: int,
    rating_date: datetime,
    review_content: str,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)

    created_at = datetime.now()
    updated_at = datetime.now()

    if not await AccountRepo.exists(session, account_id=account_id):
        raise HTTPException(
            status_code=404, detail=f"No account with ip {account_id} was found!"
        )

    if not await AudiobookRepo.exists(session, audiobook_id=audiobook_id):
        raise HTTPException(
            status_code=404, detail=f"No audiobook with ip {audiobook_id} was found!"
        )

    if await ReviewRepo.exists(
        session, account_id=account_id, audiobook_id=audiobook_id
    ):
        raise HTTPException(
            status_code=409,
            detail=f"User with id {account_id} has already reviewed audiobook with id {audiobook_id}",
        )

    review = await ReviewRepo.create(
        session,
        account_id=account_id,
        audiobook_id=audiobook_id,
        rating_value=rating_value,
        rating_date=rating_date.replace(tzinfo=None),
        review_content=review_content,
        created_at=created_at,
        updated_at=updated_at,
    )

    return review
