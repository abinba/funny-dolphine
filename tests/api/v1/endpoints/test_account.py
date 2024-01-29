from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from unittest import mock

from src.app import app
from src.repo.account import AccountRepo


@pytest.fixture
def mock_account():
    return {
        "account_id": 1,
        "username": "test",
        "is_active": True,
        "created_at": "2021-10-01T00:00:00",
        "updated_at": "2021-10-01T00:00:00",
    }


@patch("src.core.auth.authenticator")
def test_get_user(authenticator, mock_account):
    authenticator.validated_token_payload.return_value = {"sub": {"account_id": "1"}}

    with mock.patch.object(AccountRepo, "get") as mock_get:
        mock_get.return_value = mock_account

        client = TestClient(app)
        response = client.get(
            "/api/v1/accounts/1", headers={"Authorization": "Bearer test_api_key"}
        )
        assert response.status_code == 200
        assert response.json() == mock_account
