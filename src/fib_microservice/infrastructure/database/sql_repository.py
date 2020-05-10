from typing import List, Tuple

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    Table,
    Text,
    create_engine,
    func,
)

from fib_microservice.interface.database_repository.database import IDatabaseRepository


class SQLRepository(IDatabaseRepository):
    """SQLRespository based on IDatabaseRepository"""

    def __init__(self, settings):
        super().__init__(settings)
        self.engine = None
        self.connection = None
        self.num_table = None
        self.connect()
        self.create_table()

    def connect(self) -> None:
        """Method for connecting to SQLite database"""
        self.engine = create_engine(
            f"{self.settings.provider}://{self.settings.user}:{self.settings.password}@{self.settings.host}:{self.settings.port}/{self.settings.db}"
        )
        self.connection = self.engine.connect()

    def create_table(self) -> None:
        """Method to create numers table and save to database"""
        meta = MetaData()
        self.num_table = Table(
            "numbers",
            meta,
            Column("id", Integer, primary_key=True),
            Column("num", Text),
        )
        meta.create_all(self.engine)

    def save_number(self, number: int) -> None:
        """
        Method to save number in database

        Arguments:
            number {int} -- [Number to save]
        """
        query = self.num_table.insert().values(num=number)
        self.connection.execute(query)

    def get_last_two_numbers(self) -> List[str]:
        query = self.num_table.select().order_by(self.num_table.c.id.desc()).limit(2)
        result = self.connection.execute(query)
        return [int(row[1]) for row in result][::-1]

    def get_all_numbers(self) -> Tuple[Tuple[int, str]]:
        """
        Method to get all numbers from database

        Returns:
            Tuple[Tuple[int, str]] -- [Tuple of results]
        """
        query = self.num_table.select()
        result = self.connection.execute(query)
        return tuple(result)

    def get_number(self, position: int) -> Tuple[Tuple[int, str]]:
        """
        Method to get specified number from database

        Arguments:
            position {int} -- [Position of number to get]

        Returns:
            Tuple[Tuple[int, str]] -- [Tuple of results]
        """
        query = self.num_table.select().where(self.num_table.c.id == position)
        result = self.connection.execute(query)
        return tuple(result)
