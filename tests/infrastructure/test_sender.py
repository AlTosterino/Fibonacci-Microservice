from fib_microservice.shared.settings import GeneratorSettings
from unittest.mock import patch, MagicMock, Mock
import pytest
from fib_microservice.infrastructure.database.sql_repository import SQLRepository
from fib_microservice.infrastructure.message_broker.sender import SenderRepository


@pytest.fixture
@patch("fib_microservice.infrastructure.message_broker.sender.pika")
def settings(pika_mock):
    sett = MagicMock(spec=GeneratorSettings)
    sett.delay = 0
    sett.host = "localhost"
    sett.routing_key = "fib"
    return sett


@patch("fib_microservice.infrastructure.message_broker.sender.pika")
def test_should_connect_on_init(pika_mock, settings):
    # Given settings
    # When
    sender_repo = SenderRepository(settings)
    # Then
    pika_mock.BlockingConnection.assert_called_once_with(
        pika_mock.ConnectionParameters(settings.host)
    )
    sender_repo.connection.channel.assert_called_once()
    sender_repo.channel.queue_declare.assert_called_once_with(
        queue=settings.routing_key
    )


@pytest.mark.asyncio
@patch("fib_microservice.infrastructure.message_broker.sender.pika")
async def test_send_correct_message(pika_mock, settings):
    # Given settings
    message = "Sample message"
    sender_repo = SenderRepository(settings)
    sender_repo.channel = Mock()
    sender_repo.connection = Mock()
    pika_mock.BlockingConnection = Mock()
    # When
    await sender_repo.send_message(message)
    # Then
    sender_repo.channel.basic_publish.assert_called_once_with(
        exchange="", routing_key=settings.routing_key, body=message
    )


@patch("fib_microservice.infrastructure.message_broker.sender.pika")
def test_should_close_connection(pika_mock, settings):
    # Given settings
    sender_repo = SenderRepository(settings)
    # When
    sender_repo.close()
    # Then
    sender_repo.connection.close.assert_called_once()
