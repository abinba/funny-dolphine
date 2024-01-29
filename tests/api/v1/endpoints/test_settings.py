from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def mock_settings():
    return {
        "account_id": 1,
        "theme": "dark",
        "language": "en",
        "profile_picture": "https://example.com/profile_picture.png",
        "wifi_only": True,
        "auto_play": True,
        "notifications_enabled": True,
        "adult_content_enabled": True,
        "explicit_phrases": True,
        "created_at": "2021-10-01T00:00:00",
        "updated_at": "2021-10-01T00:00:00",
    }


@patch("src.api.v1.endpoints.settings.is_authenticated")
@patch("src.api.v1.endpoints.settings.is_authorized")
@patch("src.repo.user_settings.UserSettingsRepo.get")
def test_get_settings(mock_get, mock_is_authorized, mock_is_authenticated, mock_settings):
    mock_is_authenticated.return_value = {"sub": {"account_id": "1"}}
    mock_is_authorized.return_value = None
    mock_get.return_value = mock_settings

    client = TestClient(app)
    response = client.get(
        "/api/v1/settings/1", headers={"Authorization": "Bearer test_api_key"}
    )
    assert response.status_code == 200
    assert response.json() == mock_settings
