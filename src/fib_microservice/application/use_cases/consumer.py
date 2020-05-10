import logging

log = logging.getLogger(__name__)


def main(settings: "ConsumerSettings") -> None:
    """
    Entrypoint for fib_consumer command
    
    Arguments:
        settings {[Settings]} -- [Settings object]
    """
    consumer = settings.consumer
    try:
        consumer.listen()
    except KeyboardInterrupt:
        log.info("Got EXIT signal")
    finally:
        log.info("Exiting...")
        consumer.close()
