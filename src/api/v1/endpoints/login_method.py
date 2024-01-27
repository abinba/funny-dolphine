import os
from base64 import b64encode

import bcrypt
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.account import AccountRepo, AccountRepoWithoutId
from src.repo.login_method import LoginMethodRepo
from src.repo.salt import SaltRepo
from src.schemas.login_method import LoginMethodSchema

router = APIRouter()


@router.get("/", response_model=list[LoginMethodSchema])
async def get_login_method(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await LoginMethodRepo.all(session)


@router.get("/login")
async def login(
    request: Request,
    login_email: str,
    login_password: str,
    session: AsyncSession = Depends(get_async_session),
):
    # auth_header = request.headers.get("Authorization")
    # authorize_user(auth_header)

    if not await LoginMethodRepo.exists(session, login_email=login_email):
        raise HTTPException(
            status_code=409,
            detail=f"User with email '{login_email}' doesn't exist.",
        )

    login_method_db = await LoginMethodRepo.get(session, login_email=login_email)
    salt_db = await SaltRepo.get(session, account_id=login_method_db.account_id)

    test_password = bcrypt.hashpw(
        password=login_password.encode("utf-8"), salt=salt_db.salt.encode("utf-8")
    )

    if login_method_db.login_password == test_password.decode("utf-8"):
        account = await AccountRepo.get(session, account_id=login_method_db.account_id)
        return {"message": "success", "account": account}
    else:
        return {"message": "fail"}


@router.post("/", response_model=LoginMethodSchema)
async def register(
    request: Request,
    username: str,
    login_email: str,
    login_password: str,
    session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)

    if await LoginMethodRepo.exists(session, login_email=login_email):
        raise HTTPException(
            status_code=409,
            detail=f"User with email '{login_email}' already exists.",
        )

    if await AccountRepo.exists(session, username=username):
        raise HTTPException(
            status_code=409,
            detail=f"User with username '{username}' already exists.",
        )

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password=login_password.encode("utf-8"), salt=salt)

    account = await AccountRepoWithoutId.create(
        session, username=username, is_active=True
    )

    await SaltRepo.create(
        session, salt=salt.decode("utf-8"), account_id=account.account_id
    )

    account_login_method = await LoginMethodRepo.create(
        session,
        account_id=account.account_id,
        login_email=login_email,
        login_password=hashed_password.decode("utf-8"),
    )

    return account_login_method
