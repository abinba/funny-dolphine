from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import is_authenticated, is_authorized
from src.db import get_async_session
from src.repo.user_settings import UserSettingsRepo
from src.schemas.user_settings import UserSettingsSchema

router = APIRouter()


@router.get("/{account_id}", response_model=UserSettingsSchema)
async def get_settings(
    request: Request,
    account_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    payload = is_authenticated(request.headers.get("Authorization"))
    is_authorized(payload, account_id)
    return await UserSettingsRepo.get(session, account_id=account_id)
