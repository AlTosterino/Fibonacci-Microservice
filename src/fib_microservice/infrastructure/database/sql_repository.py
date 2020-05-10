from fib_microservice.interface.database_repository.database import IDatabaseRepository

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    func,
)


class SQLRepository(IDatabaseRepository):
    def __init__(self, settings):
        super().__init__(settings)
        self.engine = None
        self.connection = None
        self.num_table = None
        self.connect()
        self.create_table()

    def connect(self):
        """Method for connecting to SQLite database"""
        self.engine = create_engine(
            f"{self.settings.provider}://{self.settings.user}:{self.settings.password}@{self.settings.host}:{self.settings.port}/{self.settings.db}"
        )
        self.connection = self.engine.connect()

    def create_table(self):
        """Method to create numers table and save to database"""
        meta = MetaData()
        self.num_table = Table(
            "numbers",
            meta,
            Column("id", Integer, primary_key=True),
            Column("num", BigInteger),
        )
        meta.create_all(self.engine)

    def save_number(self, number: int):
        query = self.num_table.insert().values(num=number)
        self.connection.execute(query)

    def get_last_two_numbers(self):
        query = self.num_table.select().order_by(self.num_table.c.id.desc()).limit(2)
        result = self.connection.execute(query)
        temp = []
        for row in result:
            temp.append(row[1])
        return temp[::-1]

    def get_all_numbers(self) -> tuple:
        query = self.num_table.select()
        result = self.connection.execute(query)
        return tuple(result)

    def get_number(self, position: int) -> tuple:
        query = self.num_table.select().where(self.num_table.c.id == position)
        result = self.connection.execute(query)
        return tuple(result)
