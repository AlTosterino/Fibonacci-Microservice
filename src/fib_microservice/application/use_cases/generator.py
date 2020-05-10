import asyncio
import logging

LOOP = asyncio.get_event_loop()

log = logging.getLogger(__name__)


async def main_loop(
    sender: "SenderRepository", generator: "FibonacciGenerator"
) -> None:
    async for num in generator:
        log.info("Generated: %s", num)
        log.info("Sending...")
        await sender.send_message(num)
        log.info("Sent")


def main(settings: "GeneratorSettings") -> None:
    """
    Entrypoint for fib_generator command
    
    Arguments:
        settings {[Settings]} -- [Settings object]
    """
    generator = settings.generator
    sender = settings.sender
    try:
        LOOP.run_until_complete(main_loop(sender, generator))
    except KeyboardInterrupt:
        log.info("Got EXIT signal")
    finally:
        log.info("Exiting...")
        LOOP.close()
