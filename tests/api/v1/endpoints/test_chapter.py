from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def mock_chapters():
    return [
        {
            "chapter_id": 1,
            "chapter_ordered_id": 1,
            "audiobook_id": 1,
            "parent_id": None,
            "sub_title": "Do that",
            "full_text": "1313132",
            "duration": 30,
            "audio_file_url": "https://google.com",
            "children_ids": [4],
        },
        {
            "chapter_id": 4,
            "chapter_ordered_id": 11,
            "audiobook_id": 1,
            "parent_id": 1,
            "sub_title": "asdasd",
            "full_text": "asdad",
            "duration": 200,
            "audio_file_url": "audio/sherlock_1.mp3",
            "children_ids": [],
        },
    ]


@patch("src.core.auth.authenticator")
@patch("src.repo.chapter.ChapterRepo.all")
def test_get_chapters(mock_all, authenticator_mock, mock_chapters):
    authenticator_mock.validate_token_payload.return_value = {
        "sub": {"account_id": "1"}
    }
    mock_all.return_value = mock_chapters

    client = TestClient(app)
    response = client.get(
        "/api/v1/chapters/1", headers={"Authorization": "Bearer test_api_key"}
    )
    assert response.status_code == 200
    assert response.json() == mock_chapters
