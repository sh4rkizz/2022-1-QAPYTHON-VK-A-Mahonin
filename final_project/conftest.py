from logging import Logger, FileHandler, Formatter, getLogger, INFO, DEBUG
from os import makedirs
from os.path import exists, join, pardir, abspath
from shutil import rmtree

from tests.api.api_client import ApiClient
from tests.mysql.client import MysqlClient
from tests.ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='http://localhost:8080')
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')


def pytest_configure(config):
    base_dir = '/tmp/tests'

    if not hasattr(config, 'workerinput'):
        if exists(base_dir):
            rmtree(base_dir)
        makedirs(base_dir)

    config.base_temp_dir = base_dir


@fixture(scope='session')
def base_temp_dir() -> str:
    base_dir = '/tmp/tests'
    if exists(base_dir):
        rmtree(base_dir)
    return base_dir


@fixture(scope='function')
def temp_dir(request):
    test_dir = join(
        request.config.base_temp_dir,
        request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    )
    makedirs(test_dir)
    return test_dir


@fixture(scope='function')
def logger(temp_dir, config) -> Logger:
    log_formatter = Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = join(temp_dir, 'test.log')

    log_level = DEBUG if config['debug_log'] else INFO

    file_handler = FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = getLogger('final_project_test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()


@fixture(scope='session')
def repo_root():
    return abspath(join(__file__, pardir))


@fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    debug_log = request.config.getoption('--debug_log')

    if request.config.getoption('--selenoid'):
        vnc = bool(request.config.getoption('--vnc'))
        selenoid = 'http://127.0.0.1:4444/'
    else:
        selenoid, vnc = None, False

    return {
        'browser': browser,
        'url': url,
        'debug_log': debug_log,
        'selenoid': selenoid,
        'vnc': vnc
    }


@fixture(scope='function')
def mysql_client():
    mysql_client = MysqlClient(
        login='test_qa',
        password='qa_test',
        database='vkeducation'
    )
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


@fixture(scope='function')
def api_client(config):
    return ApiClient(config['url'])
