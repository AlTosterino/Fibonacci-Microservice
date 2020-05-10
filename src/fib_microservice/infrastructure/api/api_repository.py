from fib_microservice.interface.api_repository.api import IAPIRepository
from fastapi import FastAPI, Depends
from fastapi_utils.cbv import cbv
from starlette.endpoints import HTTPEndpoint

app = FastAPI()


class APIResource(HTTPEndpoint):
    def __init__(self, scope, receive, send, db_repo):
        super().__init__(scope, receive, send)
        self.db_repo = db_repo

    def read_root(self):
        return {"endpoints": ("/numbers", "/numbers/<int:position>")}

    def read_numbers(self):
        return {"lala": "lala"}


class APIRepository(IAPIRepository):
    def __init__(self, settings):
        super().__init__(settings)
        self.app = app
        DB_REPO = self.settings.db_repo
        self.check()

    def check(self):
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
