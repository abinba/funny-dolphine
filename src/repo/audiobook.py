from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db.models import Audiobook, Category
from src.repo.base import BaseRepo
from src.schemas import audiobook as schemas


class AudiobookRepo(BaseRepo):
    model = Audiobook

    @classmethod
    async def all(
        cls,
        session: AsyncSession,
        category_id: int = None,
    ):
        query = select(cls.model).join(
            Category, cls.model.category_id == Category.category_id
        )
        if category_id:
            query = query.filter(cls.model.category_id == category_id)

        query = query.options(joinedload(cls.model.category))
        result = await session.scalars(query)
        return [schemas.AudiobookSchema.model_validate(item) for item in result]
