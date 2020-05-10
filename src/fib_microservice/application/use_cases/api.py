import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

DB_REPO = None


def main(settings: "Settings"):
    config = Config()
    config.bind = [f"{settings.host}:{settings.port}"]
    asyncio.run(serve(settings.api_repo.app, config))
