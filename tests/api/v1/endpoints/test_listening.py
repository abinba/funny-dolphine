from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def mock_listening():
    return [
        {
            "account_id": 1,
            "audiobook_id": 1,
            "current_chapter_id": 1,
            "created_at": "2021-10-01T00:00:00",
            "updated_at": "2021-10-01T00:00:00",
        },
    ]


class MockAudiobook:
    def __init__(self, audiobook_id: int, first_chapter_id: int, *args, **kwargs):
        self.audiobook_id = audiobook_id
        self.first_chapter_id = first_chapter_id


@pytest.fixture
def mock_audiobook():
    return {
        "audiobook_id": 1,
        "first_chapter_id": 1,
        "created_at": "2021-10-01T00:00:00",
        "updated_at": "2021-10-01T00:00:00",
    }


@patch("src.core.auth.authenticator")
@patch("src.repo.listening.ListeningRepo.get")
def test_get_listening_by_account_id_and_audiobook_id(
    mock_get, authenticator_mock, mock_listening
):
    authenticator_mock.validated_token_payload.return_value = {
        "sub": {"account_id": "1"}
    }
    mock_get.return_value = mock_listening

    client = TestClient(app)
    response = client.get(
        "/api/v1/listening?account_id=1&audiobook_id=1",
        headers={"Authorization": "Bearer test_api_key"},
    )
    assert response.status_code == 200
    assert response.json() == mock_listening


@patch("src.core.auth.authenticator")
@patch("src.repo.audiobook.AudiobookRepo.get")
@patch("src.repo.listening.ListeningRepo.create")
def test_create_listening(
    mock_create, mock_get, authenticator_mock, mock_audiobook, mock_listening
):
    authenticator_mock.validated_token_payload.return_value = {
        "sub": {"account_id": "1"}
    }
    mock_get.return_value = MockAudiobook(**mock_audiobook)
    mock_create.return_value = mock_listening

    client = TestClient(app)
    response = client.post(
        "/api/v1/listening?account_id=1&audiobook_id=1",
        headers={"Authorization": "Bearer test_api_key"},
    )
    assert response.status_code == 200
    assert response.json() == mock_listening


@patch("src.core.auth.authenticator")
@patch("src.repo.listening.ListeningRepo.update_chapter")
def test_update_chapter(mock_update_chapter, authenticator_mock, mock_listening):
    authenticator_mock.validated_token_payload.return_value = {
        "sub": {"account_id": "1"}
    }
    mock_update_chapter.return_value = mock_listening

    client = TestClient(app)
    response = client.put(
        "/api/v1/listening?account_id=1&audiobook_id=1&current_chapter_id=1",
        headers={"Authorization": "Bearer test_api_key"},
    )
    assert response.status_code == 200
    assert response.json() == mock_listening
