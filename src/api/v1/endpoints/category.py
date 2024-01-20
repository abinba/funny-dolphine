from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import authorize_user
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
    authorize_user(auth_header)
    return await CategoryRepo.all(session)


@router.get("/{category_id}", response_model=CategorySchema)
async def get_categories(
    request: Request,
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await CategoryRepo.get(session, category_id=category_id)


@router.post("/", response_model=CategorySchema)
async def create_category(
    request: Request,
    category_id: int,
    name: str,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)

    if await CategoryRepo.exists(session, category_id=category_id):
        raise HTTPException(
            status_code=409, detail=f"Category with ip {category_id} already exists!"
        )

    if await CategoryRepo.exists(session, name=name):
        raise HTTPException(
            status_code=409, detail=f"Category with name {name} already exists!"
        )

    return await CategoryRepo.create(session, category_id=category_id, name=name)
