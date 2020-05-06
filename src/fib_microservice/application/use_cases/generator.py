import asyncio
import logging

LOOP = asyncio.get_event_loop()

log = logging.getLogger(__name__)


async def main_loop(generator: "FibonacciGenerator") -> None:
    async for s in generator:
        print(s)


def main(settings: "GeneratorSettings") -> None:
    generator = settings.generator
    try:
        LOOP.run_until_complete(main_loop(generator))
    except KeyboardInterrupt:
        log.info("Got EXIT signal")
    finally:
        log.info("Exiting...")
        LOOP.close()
