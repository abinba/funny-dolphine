from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.audiobook import AudiobookRepo
from src.schemas.audiobook import AudiobookSchema
from src.repo.category import CategoryRepo

router = APIRouter()


@router.get("/", response_model=list[AudiobookSchema])
async def get_audiobooks(
    request: Request,
    category_id: int = None,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await AudiobookRepo.all(session, category_id=category_id)


@router.get("/{audiobook_id}", response_model=AudiobookSchema)
async def get_audiobooks(
    request: Request,
    audiobook_id: int = None,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await AudiobookRepo.get(session, audiobook_id=audiobook_id)


@router.post("/", response_model=AudiobookSchema)
async def create_audiobook(
    request: Request,
    audiobook_id: int,
    category_id: int,
    title: str,
    author: str,
    description: str,
    duration: int,
    cover_image: str,
    listened_times: int = 0,
    rating: float = 0,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)

    if not await CategoryRepo.exists(session, category_id=category_id):
        raise HTTPException(
            status_code=404, detail=f"No category with ip {category_id} was found!"
        )

    return await AudiobookRepo.create(
        session,
        audiobook_id=audiobook_id,
        category_id=category_id,
        title=title,
        author=author,
        description=description,
        duration=duration,
        cover_image=cover_image,
        listened_times=listened_times,
        rating=rating,
    )
