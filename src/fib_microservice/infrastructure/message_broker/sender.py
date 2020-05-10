import asyncio
import logging

import pika

from fib_microservice.interface.message_repository.sender import ISender

log = logging.getLogger(__name__)


class SenderRepository(ISender):
    def __init__(self, settings):
        super().__init__(settings)
        self.routing_key = self.settings.routing_key
        self.connection = None
        self.channel = None
        self.queue = None
        self.connect()

    def connect(self) -> None:
        """Connect to RabbitMQ and set channel"""
        log.info("Connecting to: %s", self.settings.host)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.settings.host)
        )
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=self.routing_key)

    async def send_message(self, message: str) -> None:
        """
        Send message to queue

        Arguments:
            message {str} -- [Message]
        """
        log.debug("Sending: %s", message)
        self.channel.basic_publish(
            exchange="", routing_key=self.routing_key, body=str(message)
        )

    def close(self) -> None:
        """Close the connection"""
        self.connection.close()
