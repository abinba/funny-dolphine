from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models import Review
from src.repo.base import BaseRepo
from src.schemas.review import ReviewSchema


class ReviewRepo(BaseRepo):
    model = Review
    validation_schema = ReviewSchema

    @classmethod
    async def get_by_attribute(cls, session: AsyncSession, **kwargs):
        query = select(cls.model).filter_by(**kwargs)
        result = await session.scalars(query)
        if cls.validation_schema:
            return [cls.validation_schema.model_validate(item) for item in result]
        return result
