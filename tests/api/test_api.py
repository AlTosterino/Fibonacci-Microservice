from fastapi.testclient import TestClient
import pytest
from fib_microservice.infrastructure.api.api_repository import (
    APIRepository,
    APIResource,
)
from fib_microservice.shared.settings import ApiSettings

from unittest.mock import patch, Mock, call, MagicMock


@pytest.fixture
@patch("fib_microservice.infrastructure.database.sql_repository.SQLRepository")
def api_repo(sql_mock):
    sql_mock.get_all_numbers.return_value = ((1, 2), (2, 1))
    sql_mock.get_number.return_value = ((1, 2),)
    sett = MagicMock(spec=ApiSettings)
    sett.host = "samplehost"
    sett.port = 80
    sett.db_repo = sql_mock
    return APIRepository(sett)


@pytest.fixture
@patch("fib_microservice.infrastructure.database.sql_repository.SQLRepository")
def api_repo_empty(sql_mock):
    sql_mock.get_all_numbers.return_value = ()
    sql_mock.get_number.return_value = ()
    sett = MagicMock(spec=ApiSettings)
    sett.host = "samplehost"
    sett.port = 80
    sett.db_repo = sql_mock
    return APIRepository(sett)


def test_should_read_root(api_repo):
    # Given
    client = TestClient(api_repo.app)
    # When
    response = client.get("/")
    # Then
    assert response.status_code == 200
    assert response.json() == {"endpoints": ["/numbers", "/numbers/<int:position>"]}


def test_should_read_all_numbers(api_repo):
    # Given
    client = TestClient(api_repo.app)
    # When
    response = client.get("/numbers")
    # Then
    assert response.status_code == 200
    assert response.json() == [[1, 2], [2, 1]]


def test_should_read_position(api_repo):
    # Given
    client = TestClient(api_repo.app)
    # When
    response = client.get("/numbers/2")
    # Then
    assert response.status_code == 200
    assert response.json() == [
        [1, 2],
    ]
