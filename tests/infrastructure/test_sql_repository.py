import pytest
from fib_microservice.shared.settings import DatabaseSettings
from fib_microservice.infrastructure.database.sql_repository import SQLRepository
from unittest.mock import patch, Mock

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    func,
)


@pytest.fixture
@patch("fib_microservice.infrastructure.database.sql_repository.SQLRepository")
def settings(sql_mock):
    return DatabaseSettings(
        provider="postgresql",
        host="localhost",
        user="sampleuser",
        db="sampledb",
        password="samplepassword",
        port="5432",
        db_repo=sql_mock,
    )


@patch("fib_microservice.infrastructure.database.sql_repository.create_engine")
def test_should_connect_to_database_on_init(engine_mock, settings):
    # Given settings
    engine_mock.connect().return_value = Mock()
    # When
    db_repo = SQLRepository(settings)
    # Then
    engine_mock.assert_called_once_with(
        f"{settings.provider}://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db}"
    )
    engine_mock.connect.assert_called_once()


@patch("fib_microservice.infrastructure.database.sql_repository.Column")
@patch("fib_microservice.infrastructure.database.sql_repository.MetaData")
@patch("fib_microservice.infrastructure.database.sql_repository.Table")
@patch("fib_microservice.infrastructure.database.sql_repository.create_engine")
def test_should_create_correct_table_on_init(
    engine_mock, table_mock, metadata_mock, column_mock, settings
):
    # Given
    metadata_mock.return_value = Mock()
    # When
    db_repo = SQLRepository(settings)
    # Then
    metadata_mock.assert_called_once()
    table_mock.assert_called_once_with(
        "numbers",
        metadata_mock(),
        column_mock("id", Integer, primary_key=True),
        column_mock("num", BigInteger),
    )
    metadata_mock().create_all.assert_called_once()


@patch("fib_microservice.infrastructure.database.sql_repository.MetaData")
@patch("fib_microservice.infrastructure.database.sql_repository.Table")
@patch("fib_microservice.infrastructure.database.sql_repository.create_engine")
def test_should_save_correct_number(engine_mock, table_mock, metadata_mock, settings):
    # Given
    metadata_mock.return_value = Mock()
    table_mock().insert.return_value = Mock()
    table_mock().insert.values = Mock()
    repo = SQLRepository(settings)
    # When
    repo.save_number(1234)
    # Then
    table_mock().insert().values.assert_called_once_with(num=1234)
    engine_mock().connect().execute.assert_called_once_with(
        table_mock().insert().values()
    )


@patch("fib_microservice.infrastructure.database.sql_repository.MetaData")
@patch("fib_microservice.infrastructure.database.sql_repository.Table")
@patch("fib_microservice.infrastructure.database.sql_repository.create_engine")
def test_should_return_last_two_numbers(
    engine_mock, table_mock, metadata_mock, settings
):
    # Given
    repo = SQLRepository(settings)
    metadata_mock.return_value = Mock()
    table_mock().select = Mock()
    table_mock().select.order_by = Mock()
    table_mock().select.order_by.limit = Mock()
    repo.connection.execute.return_value = ((2, 123), (1, 12))
    # When
    res = repo.get_last_two_numbers()
    # Then
    table_mock().select().order_by.assert_called_once()
    engine_mock().connect().execute.assert_called_once_with(
        table_mock().select().order_by().limit()
    )
    assert res == [12, 123]
