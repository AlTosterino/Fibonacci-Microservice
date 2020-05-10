from fib_microservice.shared.settings import ConsumerSettings
from unittest.mock import patch, MagicMock, Mock
import pytest
from fib_microservice.infrastructure.database.sql_repository import SQLRepository
from fib_microservice.infrastructure.message_broker.consumer import ConsumerRepository


@pytest.fixture
@patch("fib_microservice.infrastructure.message_broker.consumer.pika")
def settings(pika_mock):
    return ConsumerSettings(
        host="localhost", db_repo=MagicMock(spec=SQLRepository), routing_key="fib",
    )


@patch("fib_microservice.infrastructure.message_broker.consumer.pika")
def test_should_connect_on_init(pika_mock, settings):
    # Given settings
    # When
    consumer_repo = ConsumerRepository(settings)
    # Then
    pika_mock.BlockingConnection.assert_called_once_with(
        pika_mock.ConnectionParameters(settings.host)
    )
    consumer_repo.connection.channel.assert_called_once()
    consumer_repo.channel.queue_declare.assert_called_once_with(
        queue=settings.routing_key
    )


@patch("fib_microservice.infrastructure.message_broker.consumer.pika")
def test_should_save_message_to_db(pika_mock, settings):
    # Given settings
    consumer_repo = ConsumerRepository(settings)
    # When
    consumer_repo.on_message(None, None, None, b"message")
    # Then
    settings.db_repo.save_number.assert_called_once_with("message")


@patch("fib_microservice.infrastructure.message_broker.consumer.pika")
def test_should_listen(pika_mock, settings):
    # Given settings
    consumer_repo = ConsumerRepository(settings)
    # When
    consumer_repo.listen()
    # Then
    consumer_repo.channel.basic_consume.assert_called_once_with(
        queue=settings.routing_key,
        auto_ack=True,
        on_message_callback=consumer_repo.on_message,
    )


@patch("fib_microservice.infrastructure.message_broker.consumer.pika")
def test_should_close_connection(pika_mock, settings):
    # Given settings
    consumer_repo = ConsumerRepository(settings)
    # When
    consumer_repo.close()
    # Then
    consumer_repo.connection.close.assert_called_once()
