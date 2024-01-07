from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.user_settings import UserSettingsRepo
from src.schemas.user_settings import UserSettingsSchema

router = APIRouter()


@router.get("/{account_id}", response_model=UserSettingsSchema)
async def get_categories(
    request: Request,
    account_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await UserSettingsRepo.get(session, account_id=account_id)
