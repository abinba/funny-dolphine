from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def mock_review():
    return {
        "account_id": 1,
        "audiobook_id": 1,
        "rating_value": 5,
        "rating_date": "2021-10-01T00:00:00",
        "review_content": "Great audiobook!",
        "created_at": "2021-10-01T00:00:00",
        "updated_at": "2021-10-01T00:00:00",
    }


@patch("src.api.v1.endpoints.review.is_authenticated")
@patch("src.api.v1.endpoints.review.is_authorized")
@patch("src.repo.review.ReviewRepo.get_by_attribute")
def test_get_reviews_by_account_id(
    mock_get_by_attribute, mock_is_authorized, mock_is_authenticated, mock_review
):
    mock_is_authenticated.return_value = None
    mock_is_authorized.return_value = None
    mock_get_by_attribute.return_value = [mock_review]

    client = TestClient(app)
    response = client.get(
        "/api/v1/reviews/account/1", headers={"Authorization": "Bearer test_api_key"}
    )
    assert response.status_code == 200
    assert response.json() == [mock_review]


@patch("src.api.v1.endpoints.review.is_authenticated")
@patch("src.repo.review.ReviewRepo.get_by_attribute")
def test_get_reviews_by_audiobook_id(
    mock_get_by_attribute, mock_is_authenticated, mock_review
):
    mock_is_authenticated.return_value = None
    mock_get_by_attribute.return_value = [mock_review]

    client = TestClient(app)
    response = client.get(
        "/api/v1/reviews/audiobook/1", headers={"Authorization": "Bearer test_api_key"}
    )
    assert response.status_code == 200
    assert response.json() == [mock_review]


@patch("src.api.v1.endpoints.review.is_authenticated")
@patch("src.api.v1.endpoints.review.is_authorized")
@patch("src.repo.account.AccountRepo.exists")
@patch("src.repo.audiobook.AudiobookRepo.exists")
@patch("src.repo.review.ReviewRepo.exists")
@patch("src.repo.review.ReviewRepo.create")
def test_create_review(
    mock_create,
    mock_exists_review,
    mock_exists_audiobook,
    mock_exists_account,
    mock_is_authorized,
    mock_is_authenticated,
    mock_review,
):
    mock_is_authenticated.return_value = None
    mock_is_authorized.return_value = None
    mock_exists_account.return_value = True
    mock_exists_audiobook.return_value = True
    mock_exists_review.return_value = False
    mock_create.return_value = mock_review

    client = TestClient(app)
    response = client.post(
        "/api/v1/reviews/",
        headers={"Authorization": "Bearer test_api_key"},
        params={
            "account_id": 1,
            "audiobook_id": 1,
            "rating_value": 5,
            "rating_date": "2021-10-01T00:00:00",
            "review_content": "Great audiobook!",
        },
    )

    assert response.status_code == 200
    assert response.json() == mock_review
