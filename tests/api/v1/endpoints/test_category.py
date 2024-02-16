from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.repo.category import CategoryRepo


@pytest.fixture
def mock_categories():
    return [
        {
            "category_id": 1,
            "name": "Category1",
        },
        {
            "category_id": 2,
            "name": "Category2",
        },
    ]


@pytest.fixture
def mock_category():
    return {
        "category_id": 1,
        "name": "Category1",
    }


@patch("src.core.auth.authenticator")
def test_get_categories(authenticator, mock_categories):
    authenticator.validated_token_payload.return_value = {"sub": {"account_id": "1"}}

    with patch.object(CategoryRepo, "all") as mock_get_all:
        mock_get_all.return_value = mock_categories

        client = TestClient(app)
        response = client.get(
            "/api/v1/categories", headers={"Authorization": "Bearer test_api_key"}
        )
        assert response.status_code == 200
        assert response.json() == mock_categories


@patch("src.core.auth.authenticator")
def test_get_category(authenticator, mock_category):
    authenticator.validated_token_payload.return_value = {"sub": {"account_id": "1"}}

    with patch.object(CategoryRepo, "get") as mock_get:
        mock_get.return_value = mock_category

        client = TestClient(app)
        response = client.get(
            "/api/v1/categories/1", headers={"Authorization": "Bearer test_api_key"}
        )
        assert response.status_code == 200
        assert response.json() == mock_category
