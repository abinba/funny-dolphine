from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.account import AccountRepo
from src.schemas.account import AccountSchema

router = APIRouter()


@router.get("/", response_model=list[AccountSchema])
async def get_users(
    request: Request,
    session: AsyncSession = Depends(get_async_session),  # Getting a database session
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await AccountRepo.all(session)


@router.get("/{account_id}", response_model=AccountSchema)
async def get_user(
    request: Request,
    account_id: int,
    session: AsyncSession = Depends(get_async_session),  # Getting a database session
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await AccountRepo.get(session, account_id=account_id)


@router.post("/", response_model=AccountSchema)
async def create_account(
    request: Request,
    account_id: int,
    username: str,
    is_active: bool,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)

    created_at = datetime.now()
    updated_at = datetime.now()

    return await AccountRepo.create(
        session,
        account_id=account_id,
        username=username,
        is_active=is_active,
        created_at=created_at,
        updated_at=updated_at,
    )
