from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from starlette import status

from src.core.errors import INVALID_JWT_TOKEN_ERROR, MISSING_JWT_TOKEN_ERROR
from src.settings import settings
from src.core.exceptions import ExpiredAccessToken, InvalidAccessToken


class Authenticator:
    _algorithm = "HS256"
    _access_token_expires_minutes = 60 * 24  # TODO: decrease this value

    auth_scheme = HTTPBearer()
    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
    _secret_key = settings.jwt_secret_key

    def validated_token_payload(self, access_token: str):
        try:
            payload = jwt.decode(
                access_token, key=self._secret_key, algorithms=[self._algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ExpiredAccessToken
        except jwt.InvalidSignatureError:
            raise InvalidAccessToken
        except jwt.exceptions.DecodeError:
            raise InvalidAccessToken

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self, account_id: int) -> str:
        to_encode = {
            "sub": {"account_id": str(account_id)},
            "exp": datetime.utcnow()
            + timedelta(minutes=self._access_token_expires_minutes),
        }
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    async def authenticate_user(self, username: str, password: str):
        if not self.verify_password(password, settings.admin_password):
            return
        return {"username": username}


authenticator = Authenticator()


def is_authenticated(auth_header: Optional[str]) -> dict:
    """
    Authenticate the user by JWT token.

    :param auth_header: "Bearer" and the JWT token

    :raise HTTPException: If the JWT token is missing or invalid or has expired
    """
    if auth_header:
        try:
            _, token = auth_header.split()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_JWT_TOKEN_ERROR
            )

        try:
            payload = authenticator.validated_token_payload(token)
            return payload
        except ExpiredAccessToken:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired. Please log in again.",
            )
        except InvalidAccessToken:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_JWT_TOKEN_ERROR
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=MISSING_JWT_TOKEN_ERROR
        )


def is_authorized(payload: dict, account_id: int):
    """
    Check if the user is authorized.

    :param payload: The payload of the JWT token
    :param account_id: The account ID of the user

    :raise HTTPException: If the user is not authorized
    """
    if payload["sub"]["account_id"] != str(account_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this resource.",
        )
