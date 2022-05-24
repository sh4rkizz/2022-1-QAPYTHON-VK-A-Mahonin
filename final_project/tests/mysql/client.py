import logging

from allure import step
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from tests.mysql.models import UserTestDatabase
from tests.user_builder import User
from settings import StatusCode


class MysqlClient:
    def __init__(self, login, password, database):
        self.database = database
        self.login = login
        self.password = password
        self.logger = logging.getLogger('final_project_test')

        self.host = '127.0.0.1'
        self.port = 3306

        self.engine = self.connection = self.session = None

    def connect(self):
        self.engine = create_engine(
            f'mysql+pymysql://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}',
            encoding='utf8'
        )

        self.connection = self.engine.connect()
        self.session = sessionmaker(
            bind=self.connection.engine,
            autocommit=True,
            expire_on_commit=False
        )()
        self.logger.info('MySQL Client was successfully connected')

    @step('Add user to database')
    def add_user(self, user: User, access=StatusCode.UNBLOCKED):
        record = UserTestDatabase(
            name=user.name,
            surname=user.surname,
            middle_name=user.middle_name,
            username=user.username,
            password=user.password,
            email=user.email,
            access=access,
            active=StatusCode.ACTIVE
        )
        self.session.add(record)
        self.logger.debug(f'Add {record} in database')
        return record

    @step('Find user in database')
    def find_user(self, username):
        if username:
            self.logger.debug(f'Trying to find {username} in database')
            return (
                self.session
                    .query(UserTestDatabase)
                    .filter(UserTestDatabase.username == username)
                    .first()
            )
        else:
            self.logger.error(f'Username was not specified for database search')
            raise

    @step('Delete user from database')
    def delete_user(self, username=None):
        if username:
            self.session.query(UserTestDatabase).filter(UserTestDatabase.username == username).delete()
            self.logger.debug(f'User {username} was deleted from database')
