from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver

import pytest


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='https://target.my.com')


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    return {'browser': browser, 'url': url}


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    url = config['url']

    capabilities = DesiredCapabilities().CHROME
    capabilities["pageLoadStrategy"] = "eager"

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
