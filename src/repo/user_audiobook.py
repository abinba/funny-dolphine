from collections import defaultdict
from typing import Optional

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.models import UserAudiobook
from src.repo.account import AccountRepo
from src.repo.base import BaseRepo
from src.repo.chapter import ChapterRepo
from src.repo.user_chapter import UserChapterRepo
from src.schemas.user_audiobook import UserAudiobookSchema


class UserAudiobookRepo(BaseRepo):
    model = UserAudiobook
    validation_schema = UserAudiobookSchema

    @classmethod
    async def get_last_listened_chapter(
        cls,
        session: AsyncSession,
        account_id: int,
        audiobook_id: int,
    ):
        result = await cls._get(
            session,
            account_id=account_id,
            audiobook_id=audiobook_id,
        )
        if not result:
            first_chapter_id = await ChapterRepo._get(
                session, audiobook_id=audiobook_id, parent_id=None
            )
            if not first_chapter_id:
                # TODO: What can we do in this case
                raise ValidationError("Audiobook has no chapters")
            return first_chapter_id.chapter_id
        return result.last_listened_chapter_id

    @classmethod
    async def all(
        cls,
        session: AsyncSession,
        account_id: int = None,
        audiobook_id: int = None,
        tree_structure: bool = False,
    ):
        result = defaultdict(list)
        chapters = await ChapterRepo.all(
            session, audiobook_id=audiobook_id, tree_structure=False
        )
        result["last_listened_chapter_id"] = await cls.get_last_listened_chapter(
            session, account_id, audiobook_id
        )

        for chapter in chapters:
            chapter_info = {"chapter": chapter}
            user_chapter = await UserChapterRepo._get(session, account_id=account_id)

            if user_chapter:
                chapter_info["listened_times"] = user_chapter.listened_times
            else:
                chapter_info["listened_times"] = 0

            result["chapters"].append(chapter_info)
        print(result)
        return cls.validation_schema.model_validate(result)

    @classmethod
    async def set_listened_times(
        cls,
        session: AsyncSession,
        account_id: int,
        audiobook_id: int,
        chapter_id: Optional[int],
    ):
        user_audiobook_info = await cls._get(
            session,
            account_id=account_id,
            audiobook_id=audiobook_id,
        )

        if not chapter_id:
            chapter_id = await cls.get_last_listened_chapter(
                session, account_id, audiobook_id
            )

        if not user_audiobook_info:
            await cls.create(
                session,
                account_id=account_id,
                audiobook_id=audiobook_id,
                last_listened_chapter_id=chapter_id,
            )
        else:
            user_audiobook_info.last_listened_chapter_id = chapter_id

        await session.commit()

    @classmethod
    async def set_explored(
        cls,
        session: AsyncSession,
        account_id: int,
        audiobook_id: int,
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

        user_chapter = await UserChapterRepo.get_or_create(
            session, account_id=account_id, chapter_id=chapter_id
        )

        if user_chapter.listened_times is not None:
            user_chapter.listened_times += 1

        await session.commit()

        await cls.set_listened_times(
            session,
            account_id=account_id,
            audiobook_id=audiobook_id,
            chapter_id=chapter_id,
        )

        return user_chapter
