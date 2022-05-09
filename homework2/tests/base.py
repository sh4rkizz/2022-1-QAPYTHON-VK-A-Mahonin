from _pytest.fixtures import FixtureRequest
from UI.pages.base_page import BasePage
from UI.pages.login_page import LoginPage
from UI.pages.main_page import MainPage

import pytest


class BaseCase:
    driver = config = logger = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')

        self.logger.debug('Setup was finished')
