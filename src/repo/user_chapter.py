from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.models import UserChapter
from src.repo.account import AccountRepo
from src.repo.base import BaseRepo
from src.repo.chapter import ChapterRepo
from src.schemas.user_chapter import UserChapterSchema


class UserChapterRepo(BaseRepo):
    model = UserChapter
    validation_schema = UserChapterSchema

    @classmethod
    async def set_explored(
        cls,
        session: AsyncSession,
        account_id: int,
        chapter_id: int,
    ):
        if not await AccountRepo.exists(session, account_id=account_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account with id {account_id} not found",
            )

        if not await ChapterRepo.exists(session, chapter_id=chapter_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chapter with id {account_id} not found",
            )

        user_chapter = await cls.get_or_create(
            session, account_id=account_id, chapter_id=chapter_id
        )

        if user_chapter.listened_times is not None:
            user_chapter.listened_times += 1

        await session.commit()
        return user_chapter
