import os
import pytest

from mysql.client import Client


@pytest.fixture(scope='session')
def mysql_client() -> Client:
    client = Client(
        database='TEST_SQL',
        login='root',
        password='1111'
    )
    client.connect()
    yield client
    client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        client = Client(
            database='TEST_SQL',
            login='root',
            password='1111'
        )

        client.create_new_database()
        client.connect()

        client.create_tables(
            'all_requests',
            'requests_by_type',
            'the_most_frequent_requests',
            'client_based_errors',
            'server_based_errors'
        )
        client.connection.close()


def repo_root() -> str:
    return os.path.abspath(os.path.join(__file__, os.pardir))
