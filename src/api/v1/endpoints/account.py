from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import is_authenticated, is_authorized
from src.db import get_async_session
from src.repo.account import AccountRepo
from src.schemas.account import AccountSchema

router = APIRouter()


@router.get("/{account_id}", response_model=AccountSchema)
async def get_user_info(
    request: Request,
    account_id: int,
    session: AsyncSession = Depends(get_async_session),  # Getting a database session
):
    payload = is_authenticated(request.headers.get("Authorization"))
    is_authorized(payload, account_id)
    return await AccountRepo.get(session, account_id=account_id)
