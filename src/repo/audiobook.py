from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db.models import Audiobook, Category
from src.repo.base import BaseRepo
from src.repo.listening import ListeningRepo
from src.schemas import audiobook as schemas


class AudiobookRepo(BaseRepo):
    model = Audiobook

    @classmethod
    async def all(
        cls,
        session: AsyncSession,
        category_id: int = None,
        popular: bool = False,
        limit: int = 10,
        # offset: int = 0, # TODO: implement pagination
    ):
        query = select(cls.model).join(
            Category, cls.model.category_id == Category.category_id
        )

        if category_id:
            query = query.filter(cls.model.category_id == category_id)

        if popular:
            query = query.order_by(cls.model.rating.desc())

        query = query.fetch(limit).options(joinedload(cls.model.category))
        result = await session.scalars(query)
        return [schemas.AudiobookSchema.model_validate(item) for item in result]

    @classmethod
    async def search(
        cls,
        session: AsyncSession,
        search_query: str,
        limit: int = 10,
        # offset: int = 0, # TODO: implement pagination
    ):
        query = select(cls.model).join(
            Category, cls.model.category_id == Category.category_id
        )
        query = query.filter(
            or_(
                cls.model.title.ilike(f"%{search_query}%"),
                cls.model.author.ilike(f"%{search_query}%"),
            )
        )
        query = query.fetch(limit).options(joinedload(cls.model.category))
        result = await session.scalars(query)
        return [schemas.AudiobookSchema.model_validate(item) for item in result]

    @classmethod
    async def recently_listened(
        cls,
        session: AsyncSession,
        account_id: int,
        limit: int = 10,
        # offset: int = 0, # TODO: implement pagination
    ):
        listened_audiobooks = await ListeningRepo.get_audiobooks_by_account_id(
            session, account_id
        )
        if not listened_audiobooks:
            return []

        query = select(cls.model).join(
            Category, cls.model.category_id == Category.category_id
        )
        query = query.filter(cls.model.audiobook_id.in_(listened_audiobooks))
        query = query.fetch(limit).options(joinedload(cls.model.category))
        result = await session.scalars(query)
        return [schemas.AudiobookSchema.model_validate(item) for item in result]
