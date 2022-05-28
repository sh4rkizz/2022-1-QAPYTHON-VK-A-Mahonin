import os
import shutil
import sys
import time
from logging import Logger, Formatter, DEBUG, INFO, FileHandler, getLogger

import faker
import pytest
import requests

from mock import flask_mock
from settings import MOCK_URL

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


def pytest_addoption(parser):
    parser.addoption('--debug_log', action='store_true')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        mock_run(config)


def wait_ready(method, timeout=5, **kwargs):
    started = False
    st = time.time()
    while time.time() - st <= timeout:
        try:
            method(**kwargs)
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'Server did not started in {timeout}s!')


@pytest.fixture(scope='function')
def human_being():
    fake = faker.Faker()

    return {
        'name': fake.first_name(),
        'surname': fake.last_name()
    }


@pytest.fixture(scope='session')
def base_temp_dir() -> str:
    base_dir = 'C:\\tests' if sys.platform.startswith('win') else '/tmp/tests'
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    return base_dir


@pytest.fixture(scope='function')
def temp_dir(request) -> str:
    test_dir = os.path.join(
        request.config.base_temp_dir,
        request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    )
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function')
def logger(temp_dir, config) -> Logger:
    log_formatter = Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = DEBUG if config['debug_log'] else INFO

    file_handler = FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = getLogger('test_mock')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()


@pytest.fixture(scope='session')
def config(request):
    debug_log = request.config.getoption('--debug_log')

    return {'debug_log': debug_log}


def mock_run(config):
    flask_mock.mock_run()

    wait_ready(
        requests.get,
        url=f'{MOCK_URL}'
    )

    config.flask_mock = flask_mock


def pytest_unconfigure(config):
    config.flask_mock.mock_stop()
