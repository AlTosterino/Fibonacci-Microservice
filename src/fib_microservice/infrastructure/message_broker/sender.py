import asyncio
import pika
from fib_microservice.interface.message_broker.sender import ISender


class Sender(ISender):
    def __init__(self, settings):
        super().__init__(settings)
        self.routing_key = "fibonacci"
        self.connection = None
        self.channel = None
        self.queue = None
        self.connect()

    def connect(self) -> None:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.settings.host)
        )
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=self.routing_key)

    def send_message(self, message: str) -> None:
        self.channel.basic_publish(
            exchange="", routing_key=self.routing_key, body=str(message)
        )

    def close(self) -> None:
        self.connection.close()
