from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from mysql.models import Base


class Client:
    def __init__(self, *, database: str, login: str, password: str):
        self.database = database
        self.login = login
        self.password = password

        self.host = '127.0.0.1'
        self.port = 3306

        self.engine = self.connection = self.session = None

    def connect(self, is_created=True):
        database = self.database if is_created else ''

        self.engine = create_engine(
            f'mysql+pymysql://{self.login}:{self.password}@{self.host}:{self.port}/{database}',
            encoding='utf8'
        )

        self.connection = self.engine.connect()
        self.session = sessionmaker(
            bind=self.connection.engine,
            autocommit=True,
            expire_on_commit=False
        )()

    def exec_query(self, *, query: str, fetch: bool = False):
        result = self.connection.execute(query)
        if fetch:
            return result.fethall()

    def create_tables(self, *args):
        for table in args:
            if not inspect(self.engine).has_table(table):
                Base.metadata.tables[table].create(self.engine)

    def create_new_database(self):
        self.connect(is_created=False)
        self.exec_query(query=f'DROP database if EXISTS {self.database}')
        self.exec_query(query=f'CREATE database {self.database}')
