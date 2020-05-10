import asyncio
import logging

import pika

from fib_microservice.interface.message_repository.consumer import IConsumer

log = logging.getLogger(__name__)


class ConsumerRepository(IConsumer):
    """RabbitMQ consumer repository based on IConsumer"""

    def __init__(self, settings):
        super().__init__(settings)
        self.routing_key = self.settings.routing_key
        self.connection = None
        self.channel = None
        self.queue = None
        self.connect()

    def connect(self):
        """Connect to RabbitMQ and set channel"""
        log.info("Connecting to: %s", self.settings.host)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.settings.host)
        )
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=self.routing_key)

    def on_message(self, ch, method, properties, body) -> None:
        """
        On message callback

        Arguments:
            ch {[pika.adapters.blocking_connection.BlockingChannel]} -- [Channel]
            method {[pika.spec.Basic.Deliver]} -- [Method]
            properties {[pika.spec.BasicProperties]} -- [Properties]
            body {[bytes]} -- [Body of message]
        """
        number = body.decode("utf-8")
        self.settings.db_repo.save_number(number)
        log.info("SAVED %s", number)

    def listen(self) -> None:
        """Listen to new messages"""
        self.channel.basic_consume(
            queue=self.settings.routing_key,
            auto_ack=True,
            on_message_callback=self.on_message,
        )
        log.info("Listening...")
        self.channel.start_consuming()

    def close(self) -> None:
        """Close the connection"""
        self.connection.close()
