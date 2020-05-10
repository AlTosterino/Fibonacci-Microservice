import logging

log = logging.getLogger(__name__)


def main(settings: "ConsumerSettings") -> None:
    consumer = settings.consumer
    try:
        consumer.listen()
    except KeyboardInterrupt:
        log.info("Got EXIT signal")
    finally:
        log.info("Exiting...")
        consumer.close()
