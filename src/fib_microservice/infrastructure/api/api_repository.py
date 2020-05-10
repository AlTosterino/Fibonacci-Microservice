from fib_microservice.interface.api_repository.api import IAPIRepository
from fastapi import FastAPI, Depends
from fastapi_utils.cbv import cbv
from starlette.endpoints import HTTPEndpoint, HTTPException

from typing import Tuple, Dict

app = FastAPI()


class APIResource(HTTPEndpoint):
    def __init__(self, scope, receive, send, db_repo):
        super().__init__(scope, receive, send)
        self.db_repo = db_repo

    async def read_root(self):
        return {"endpoints": ("/numbers", "/numbers/<int:position>")}

    async def read_numbers(self):
        return self.db_repo.get_all_numbers()

    async def read_number(self, position: int):
        num = self.db_repo.get_number(position)
        if not num:
            raise HTTPException(
                status_code=404, detail="Requested position hasn't been generated yet"
            )
        return num


class APIRepository(IAPIRepository):
    def __init__(self, settings):
        super().__init__(settings)
        self.app = app
        self.add_api_routes()

    def add_api_routes(self):
        resource_root = APIResource(
            scope={"type": "http"},
            receive=None,
            send=None,
            db_repo=self.settings.db_repo,
        )
        app.add_api_route(path="/", endpoint=resource_root.read_root, methods=["GET"])
        app.add_api_route(
            path="/numbers", endpoint=resource_root.read_numbers, methods=["GET"]
        )
        app.add_api_route(
            path="/numbers/{position}",
            endpoint=resource_root.read_number,
            methods=["GET"],
        )
