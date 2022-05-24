from os import path

from allure import attach, attachment_type, step
from pytest import fixture
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.main_page import MainPage
from tests.ui.pages.registration_page import RegistrationPage


class UnsupportedBrowserType(Exception):
    pass


@fixture(scope='function')
def driver(config, temp_dir, logger):
    browser = config['browser']
    url = config['url']

    options = ChromeOptions()
    options.add_experimental_option('prefs', {'download.default_directory': temp_dir})

    capabilities = DesiredCapabilities().CHROME
    capabilities['pageLoadStrategy'] = 'eager'

    if browser == 'chrome':
        browser = webdriver.Chrome(
            desired_capabilities=capabilities,
            service=Service(ChromeDriverManager().install())
        )
        browser.maximize_window()
        browser.get(url)
    else:
        logger.error(f'Usage of unsupported {browser=} detected')
        raise UnsupportedBrowserType(f'Your browser {browser} is not supported right now. Sorry...')

    logger.info(f'Browser {config["browser"]} is being used for the application testing')

    yield browser
    browser.quit()


@fixture(scope='function', autouse=True)
def ui_report(driver, request, temp_dir):
    failed_test_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_test_count:
        browser_logs = path.join(temp_dir, 'browser_log')

        with open(browser_logs, 'w') as f:
            for line in driver.get_log('browser'):
                f.write(f"{line['level']} - {line['source']}\n{line['message']}\n")

        screenshot_path = path.join(temp_dir, 'failed.png')
        driver.get_screenshot_as_file(screenshot_path)
        attach.file(screenshot_path, 'failed.png', attachment_type.PNG)

        with open(browser_logs, 'r') as f:
            attach(f.read(), 'test.log', attachment_type.TEXT)


@step('Auto login')
@fixture(scope='function')
def autologin(driver, login_page, logger, username='sharkizz', password='123'):
    logger.debug('Autologin process started')
    login_page.insert(locator=login_page.locators.USERNAME, text=username)
    login_page.insert(locator=login_page.locators.PASSWORD, text=password)
    login_page.click(login_page.locators.SUBMIT)

    return MainPage(driver=driver)


@fixture
def main_page(driver):
    return MainPage(driver=driver)


@fixture
def login_page(driver):
    return LoginPage(driver=driver)


@fixture
def registration_page(driver):
    return RegistrationPage(driver=driver)
