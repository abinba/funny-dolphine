from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db import Base


class BaseRepo:
    model: Base = None
    validation_schema: BaseModel = None

    @classmethod
    async def _get(cls, session: AsyncSession, **kwargs):
        query = select(cls.model).filter_by(**kwargs)
        result = await session.scalar(query)
        return result

    @classmethod
    async def get(cls, session: AsyncSession, **kwargs):
        result = await cls._get(session, **kwargs)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )
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
        row = await cls._get(session, **kwargs)
        if not row:
            row = await cls.create(session, **kwargs)
        return row

