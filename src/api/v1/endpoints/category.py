from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import is_authenticated
from src.db import get_async_session
from src.repo.category import CategoryRepo
from src.schemas.category import CategorySchema

router = APIRouter()


@router.get("/", response_model=list[CategorySchema])
async def get_categories(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    is_authenticated(auth_header)
    return await CategoryRepo.all(session)


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(
    request: Request,
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    is_authenticated(auth_header)
    return await CategoryRepo.get(session, category_id=category_id)
