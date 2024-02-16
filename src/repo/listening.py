from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Listening
from src.repo.base import BaseRepo
from src.repo.chapter import ChapterRepo
from src.schemas.listening import ListeningSchema


class ListeningRepo(BaseRepo):
    model = Listening
    validation_schema = ListeningSchema

    @classmethod
    async def get_audiobooks_by_account_id(cls, session: AsyncSession, account_id: int):
        query = select(cls.model.audiobook_id).where(cls.model.account_id == account_id)
        result = await session.scalars(query)
        return result.all()

    @classmethod
    async def update_chapter(
        cls,
        session: AsyncSession,
        account_id: int,
        audiobook_id: int,
        current_chapter_id: int,
    ):
        chapter = await ChapterRepo.get(session, chapter_id=current_chapter_id)
        if chapter.audiobook_id != audiobook_id:
            raise HTTPException(
                status_code=400,
                detail=f"Chapter with chapter_id '{current_chapter_id}' doesn't belong "
                f"to audiobook with audiobook_id '{audiobook_id}'.",
            )

        listening = await cls._get(
            session, account_id=account_id, audiobook_id=audiobook_id
        )

        if not listening:
            raise HTTPException(
                status_code=400,
                detail=f"Listening with account_id '{account_id}' and audiobook_id "
                f"'{audiobook_id}' doesn't exist.",
            )

        listening.current_chapter_id = current_chapter_id

        await session.commit()
        return listening
