from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from unittest import mock

from src.app import app
from src.repo.audiobook import AudiobookRepo


@pytest.fixture
def mock_audiobook():
    return {
        "created_at": "2024-01-17T16:13:49.679597",
        "updated_at": "2024-01-17T16:13:49.679597",
        "audiobook_id": 16,
        "category_id": 5,
        "title": "Witcher: Last wish",
        "author": "A. Sapkowski",
        "description": "Second of popular books about Geralt of Rivia.",
        "duration": 378,
        "cover_image": "https://static.wikia.nocookie.net/witcher",
        "listened_times": 0,
        "rating": 0.0,
    }


@patch("src.core.auth.authenticator")
def test_get_audiobooks(authenticator, mock_audiobook):
    authenticator.validated_token_payload.return_value = {"sub": {"account_id": "1"}}

    with mock.patch.object(AudiobookRepo, "all") as mock_all:
        mock_all.return_value = [mock_audiobook]

        client = TestClient(app)
        response = client.get(
            "/api/v1/audiobooks/", headers={"Authorization": "Bearer test_api_key"}
        )
        assert response.status_code == 200
        assert response.json() == [mock_audiobook]


@patch("src.core.auth.authenticator")
def test_get_audiobook(authenticator, mock_audiobook):
    authenticator.validated_token_payload.return_value = {"sub": {"account_id": "1"}}

    with mock.patch("src.core.auth.settings") as mock_settings, mock.patch.object(
        AudiobookRepo, "get"
    ) as mock_get:
        mock_settings.api_key = "test_api_key"
        mock_get.return_value = mock_audiobook

        client = TestClient(app)
        response = client.get(
            "/api/v1/audiobooks/1", headers={"Authorization": "Bearer test_api_key"}
        )
        assert response.status_code == 200
        assert response.json() == mock_audiobook
