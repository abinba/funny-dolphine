from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Base


class BaseRepo:
    model: Base = None
    validation_schema: BaseModel = None

    @classmethod
    async def get(cls, session: AsyncSession, **kwargs):
        query = select(cls.model).filter_by(**kwargs)
        result = await session.scalar(query)
        if cls.validation_schema:
            return cls.validation_schema.model_validate(result)
        return result

    @classmethod
    async def all(
        cls,
        session: AsyncSession,
    ):
        query = select(cls.model)
        result = await session.scalars(query)
        if cls.validation_schema:
            return [cls.validation_schema.model_validate(item) for item in result]
        return result

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        row = cls.model(**kwargs)
        session.add(row)
        if cls.validation_schema:
            return cls.validation_schema.model_validate(row)
        return row

    @classmethod
    async def exists(cls, session: AsyncSession, **kwargs) -> bool:
        query = select(cls.model).filter_by(**kwargs)
        result = await session.scalar(query)
        if result:
            return True
        return False

    @classmethod
    async def get_or_create(cls, session: AsyncSession, **kwargs):
        row = await cls.get(session, **kwargs)
        if not row:
            row = await cls.create(session, **kwargs)
        if cls.validation_schema:
            return cls.validation_schema.model_validate(row)
        return row
