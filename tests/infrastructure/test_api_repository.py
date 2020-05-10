from unittest.mock import Mock, call, patch

import pytest
from starlette.endpoints import HTTPException

from fib_microservice.infrastructure.api.api_repository import (
    APIRepository,
    APIResource,
)
from fib_microservice.shared.settings import ApiSettings


@pytest.fixture
@patch("fib_microservice.infrastructure.database.sql_repository.SQLRepository")
def settings(sql_mock):
    return ApiSettings(host="samplehost", port="80", db_repo=sql_mock)


@patch("fib_microservice.infrastructure.api.api_repository.app")
@patch("fib_microservice.infrastructure.api.api_repository.APIResource")
def test_should_create_api_routes_on_init(api_res_mock, app_mock, settings):
    # Given settings api_res_mock app_mock
    # When
    api_repo = APIRepository(settings)
    app_calls = (
        call.add_api_route(
            path="/", endpoint=api_res_mock().read_root, methods=["GET"]
        ),
        call.add_api_route(
            path="/numbers", endpoint=api_res_mock().read_numbers, methods=["GET"]
        ),
        call.add_api_route(
            path="/numbers/{position}",
            endpoint=api_res_mock().read_number,
            methods=["GET"],
        ),
    )
    api_calls = (
        call(scope={"type": "http"}, receive=None, send=None, db_repo=settings.db_repo),
        call(),
        call(),
        call(),
    )
    # Then
    api_res_mock.assert_has_calls(api_calls)
    app_mock.assert_has_calls(app_calls)


@pytest.mark.asyncio
@patch("fib_microservice.infrastructure.api.api_repository.HTTPEndpoint")
async def test_should_return_available_endpoints(settings):
    with patch("fib_microservice.infrastructure.api.api_repository.HTTPEndpoint"):
        # given http_mock
        api_res = APIResource(
            scope={"type": "http"}, receive=None, send=None, db_repo=settings.db_repo
        )
        # When
        res = await api_res.read_root()
        # Then
        assert res == {"endpoints": ("/numbers", "/numbers/<int:position>")}


@pytest.mark.asyncio
@patch("fib_microservice.infrastructure.api.api_repository.HTTPEndpoint")
async def test_should_return_numbers(settings):
    with patch("fib_microservice.infrastructure.api.api_repository.HTTPEndpoint"):
        # given http_mock
        settings.db_repo.get_all_numbers.return_value = ((1, 2), (2, 3))
        api_res = APIResource(
            scope={"type": "http"}, receive=None, send=None, db_repo=settings.db_repo
        )
        # When
        res = await api_res.read_numbers()
        # Then
        settings.db_repo.get_all_numbers.assert_called_once()
        assert res == ((1, 2), (2, 3))


@pytest.mark.asyncio
@patch("fib_microservice.infrastructure.api.api_repository.HTTPEndpoint")
async def test_should_return_number_from_position(settings):
    with patch("fib_microservice.infrastructure.api.api_repository.HTTPEndpoint"):
        # given http_mock
        settings.db_repo.get_number.return_value = ((1, 2),)
        api_res = APIResource(
            scope={"type": "http"}, receive=None, send=None, db_repo=settings.db_repo
        )
        # When
        res = await api_res.read_number(2)
        # Then
        settings.db_repo.get_number.assert_called_once_with(2)
        assert res == ((1, 2),)


@pytest.mark.asyncio
@patch("fib_microservice.infrastructure.api.api_repository.HTTPEndpoint")
async def test_should_raise_when_number_not_generated(settings):
    with patch("fib_microservice.infrastructure.api.api_repository.HTTPEndpoint"):
        # given http_mock
        settings.db_repo.get_number.return_value = ()
        api_res = APIResource(
            scope={"type": "http"}, receive=None, send=None, db_repo=settings.db_repo
        )
        # Then
        with pytest.raises(HTTPException):
            # When
            await api_res.read_number(2)
