from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

from src.db.builder import build_sa_session_factory, build_sa_engine


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session


Base = declarative_base()
engine = build_sa_engine()
Session = build_sa_session_factory(engine)
