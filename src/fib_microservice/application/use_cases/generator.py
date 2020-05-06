import asyncio
import logging

LOOP = asyncio.get_event_loop()

log = logging.getLogger(__name__)

from fib_microservice.infrastructure.message_broker.sender import Sender


async def main_loop(sender: "Sender", generator: "FibonacciGenerator") -> None:
    async for num in generator:
        log.info("Generated: %s", num)
        log.info("Sending...")
        sender.send_message(num)
        log.info("Sent")


def main(settings: "GeneratorSettings") -> None:
    generator = settings.generator
    sender = settings.sender
    try:
        LOOP.run_until_complete(main_loop(sender, generator))
    except KeyboardInterrupt:
        log.info("Got EXIT signal")
    finally:
        log.info("Exiting...")
        LOOP.close()
