from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.settings import settings


def build_sa_engine() -> AsyncEngine:
    return create_async_engine(
        str(settings.get_database_uri()),
        isolation_level=settings.database.isolation_level,
        pool_size=settings.database.pool_size,
        max_overflow=settings.database.max_overflow,
    )


def build_sa_session_factory(
    async_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=async_engine,
        autoflush=settings.database.auto_flush,
        expire_on_commit=settings.database.expire_on_commit,
    )
