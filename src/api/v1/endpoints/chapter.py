from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import is_authenticated
from src.db import get_async_session
from src.repo.chapter import ChapterRepo
from src.schemas.chapter import ChapterFlat, ChapterTree

router = APIRouter()


@router.get("/{audiobook_id}", response_model=list[ChapterTree | ChapterFlat])
async def get_chapters(
    request: Request,
    audiobook_id: int,
    tree_structure: bool = Query(default=False),
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    is_authenticated(auth_header)
    return await ChapterRepo.all(
        session, audiobook_id=audiobook_id, tree_structure=tree_structure
    )
