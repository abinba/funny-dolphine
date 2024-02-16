from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, Request, HTTPException, Query
from pydantic import EmailStr, BaseModel, field_validator
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.auth import Authenticator
from src.db import get_async_session
from src.repo.account import AccountRepo, AccountRepoWithoutId
from src.repo.login_method import LoginMethodRepo
from src.repo.salt import SaltRepo
from src.repo.user_settings import UserSettingsRepo

router = APIRouter()


class LoginUserCredentials(BaseModel):
    email: EmailStr
    password: Annotated[str, Query(min_length=8, max_length=60)]


class RegisterUserCredentials(LoginUserCredentials):
    username: Annotated[str, Query(min_length=3, max_length=35)]

    @field_validator("username")
    @classmethod
    def username_isalnum(cls, v):
        if not v.isalnum():
            raise ValueError(
                "Username must not contain special characters, spaces nor symbols."
            )
        return v

    @field_validator("password")
    @classmethod
    def login_password_contains_special_characters(cls, v):
        if not any(char in "!@#$%^&*()-_=+[]{};:,./<>?`~" for char in v):
            raise ValueError("Password must contain at least one special character.")
        return v

    @field_validator("password")
    @classmethod
    def login_password_contains_number(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number.")
        return v

    @field_validator("password")
    @classmethod
    def login_password_contains_uppercase(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter.")
        return v

    @field_validator("password")
    @classmethod
    def login_password_contains_lowercase(cls, v):
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter.")
        return v


@router.post("/login")
async def login(
    request: Request,  # noqa
    user_credentials: LoginUserCredentials,
    session: AsyncSession = Depends(get_async_session),
):
    login_email = user_credentials.email
    login_password = user_credentials.password

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
        return {
            "message": "success",
            "account": account,
            "token": Authenticator().create_access_token(account.account_id),
        }
    else:
        return {"message": "fail"}


@router.post("/")
async def register(
    request: Request,  # noqa
    user_credentials: RegisterUserCredentials,
    session: AsyncSession = Depends(get_async_session),
):
    username = user_credentials.username
    login_email = user_credentials.email
    login_password = user_credentials.password

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

    await LoginMethodRepo.create(
        session,
        account_id=account.account_id,
        login_email=login_email,
        login_password=hashed_password.decode("utf-8"),
    )

    await UserSettingsRepo.create(
        session,
        account_id=account.account_id,
    )

    return {"message": "success"}
