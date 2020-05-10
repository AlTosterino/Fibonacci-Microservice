import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config


def main(settings: "Settings"):
    """
    Entrypoint for fib_api command
    
    Arguments:
        settings {[Settings]} -- [Settings object]
    """
    config = Config()
    config.bind = [f"{settings.host}:{settings.port}"]
    asyncio.run(serve(settings.api_repo.app, config))
