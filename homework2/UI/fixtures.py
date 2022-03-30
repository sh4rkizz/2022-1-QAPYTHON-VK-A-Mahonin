import allure
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import ChromeOptions

from selenium import webdriver

from UI.pages.base_page import BasePage
from UI.pages.main_page import MainPage
from UI.pages.login_page import LoginPage

import os
import shutil
import sys
import random
import string
import pytest


@pytest.fixture(scope='function')
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']

    options = ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": temp_dir})

    capabilities = DesiredCapabilities().CHROME
    capabilities["pageLoadStrategy"] = 'eager'

    if browser == 'chrome':
        browser = webdriver.Chrome(
            desired_capabilities=capabilities,
            service=Service(ChromeDriverManager().install())
        )
        browser.maximize_window()
        browser.get(url)
    else:
        raise RuntimeError(f'Your browser {browser} is not supported right now. Sorry...')

    yield browser
    browser.quit()


def pytest_configure(config):
    base_dir = 'C:\\tests' if sys.platform.startswith('win') else '/tmp/tests'

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, temp_dir):
    failed_test_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_test_count:
        browser_logs = os.path.join(temp_dir, 'browser_log')

        with open(browser_logs, 'w') as f:
            for line in driver.get_log('browser'):
                f.write(f"{line['level']} - {line['source']}\n{line['message']}\n")

        screenshot_path = os.path.join(temp_dir, 'failed.png')
        driver.get_screenshot_as_file(screenshot_path)
        allure.attach.file(screenshot_path, 'failed.png', allure.attachment_type.PNG)

        with open(browser_logs, 'r') as f:
            allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)


@allure.step("Autologin")
@pytest.fixture(scope='function')
def autologin(driver, logger, login_page) -> MainPage:
    email = 'ewe2002ewe@mail.ru'
    password = 'Qwerty123'
    login_page.login_user(email=email, password=password)
    logger.info(f'Logged in with email: {email} and password: {password}')
    return MainPage(driver)


@pytest.fixture(scope='function')
def photo_path(repo_root):
    return os.path.join(repo_root, 'ui', 'cute_cat.jpg')


@pytest.fixture(scope='function')
def randomize_name(length=15):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@pytest.fixture()
def base_page(driver):
    return BasePage(driver)


@pytest.fixture()
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture()
def main_page(driver):
    return MainPage(driver)
