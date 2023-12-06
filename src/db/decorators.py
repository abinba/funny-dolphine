from functools import wraps

from src.db import Session


def with_session(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        async with Session() as session:
            return await func(session, *args, **kwargs)

    return inner


def with_session_cls(func):
    @wraps(func)
    async def inner(cls, *args, **kwargs):
        async with Session() as session:
            return await func(cls, session, *args, **kwargs)

    return inner
