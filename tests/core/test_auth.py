from unittest.mock import patch

import pytest
from fastapi import HTTPException
from src.core.auth import is_authenticated, is_authorized


@pytest.fixture
def auth_header():
    return "Bearer jwt_token"


@patch("src.core.auth.authenticator")
def test_is_authenticated_with_valid_auth_header(mock_auth, auth_header):
    mock_auth.validated_token_payload.return_value = {"sub": {"account_id": "1"}}
    try:
        is_authenticated(auth_header)
    except HTTPException:
        pytest.fail("is_authenticated raised HTTPException unexpectedly!")


def test_is_authenticated_with_invalid_auth_header():
    with pytest.raises(HTTPException):
        is_authenticated("invalid_auth_header")


def test_is_authorized_with_valid_payload():
    payload = {"sub": {"account_id": "1"}}
    try:
        is_authorized(payload, 1)
    except HTTPException:
        pytest.fail("is_authorized raised HTTPException unexpectedly!")


def test_is_authorized_with_invalid_payload():
    payload = {"sub": {"account_id": "1"}}
    with pytest.raises(HTTPException):
        is_authorized(payload, 2)
