from typing import Dict, List, Tuple

from fastapi import Depends, FastAPI
from starlette.endpoints import HTTPEndpoint, HTTPException

from fib_microservice.interface.api_repository.api import IAPIRepository

app = FastAPI()


class APIResource(HTTPEndpoint):
    """Class based API views for FastAPI"""

    def __init__(self, scope, receive, send, db_repo):
        super().__init__(scope, receive, send)
        self.db_repo = db_repo

    async def read_root(self) -> Dict[str, List[str]]:
        """
        Method for showing available endpoints

        Returns:
            Dict[str, List[str]] -- [Dictionary of available endpoints]
        """
        return {"endpoints": ("/numbers", "/numbers/<int:position>")}

    async def read_numbers(self) -> List[Dict[str, str]]:
        """
        Method to show all numbers in database

        Returns:
            List[Dict[str, str]] -- [List of all numbers]
        """
        return self.db_repo.get_all_numbers()

    async def read_number(self, position: int) -> List[Dict[str, str]]:
        """
        Method to show number at required position

        Arguments:
            position {int} -- [Position of number (id in database)]

        Raises:
            HTTPException: [When number not found]

        Returns:
            List[Dict[str, str]] -- [List of found number]
        """
        num = self.db_repo.get_number(position)
        if not num:
            raise HTTPException(
                status_code=404, detail="Requested position hasn't been generated yet"
            )
        return num


class APIRepository(IAPIRepository):
    """APIRepository based on IAPIRepository"""

    def __init__(self, settings):
        super().__init__(settings)
        self.app = app
        self.add_api_routes()

    def add_api_routes(self):
        """Method to add all api routes"""
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
