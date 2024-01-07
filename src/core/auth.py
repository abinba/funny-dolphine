from typing import Optional

from fastapi import HTTPException
from starlette import status

from src.core.errors import INVALID_API_KEY_ERROR, MISSING_API_KEY_ERROR
from src.settings import settings


def authorize_user(auth_header: Optional[str]) -> None:
    """
    Authorize the user by comparing the Authorization header to the API Key.

    :param auth_header: Authorization header with "Bearer" and the API key

    :raise HTTPException: If the API key is missing or invalid
    """
    if auth_header:
        try:
            _, token = auth_header.split()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_API_KEY_ERROR
            )

        if token != settings.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_API_KEY_ERROR
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=MISSING_API_KEY_ERROR
        )
    return None
