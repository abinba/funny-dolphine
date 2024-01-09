from typing import Union

from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.chapter import ChapterRepo
from src.schemas.chapter import ChapterFlat, ChapterTree

router = APIRouter()


@router.get("/{audiobook_id}", response_model=list[Union[ChapterTree, ChapterFlat]])
async def get_chapters(
    request: Request,
    audiobook_id: int,
    tree_structure: bool = Query(default=False),
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ChapterRepo.all(
        session, audiobook_id=audiobook_id, tree_structure=tree_structure
    )
