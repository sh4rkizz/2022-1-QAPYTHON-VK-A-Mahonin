from allure import step
import logging

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as exp_cond
from selenium.webdriver.support.wait import WebDriverWait

from UI.locators.basic_locators import BasePageLocators

CLICK_RETRY = 5
TIMEOUT = 3


class PageNotLoadedException(Exception):
    pass


class BasePage(object):
    url = 'https://target.my.com/'
    locators = BasePageLocators()

    def __init__(self, driver):
        self.logger = logging.getLogger('test')
        self.logger.debug(f'{self.__class__.__name__} page is being opened')
        self.driver = driver

    def wait(self, timeout=None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=10 if timeout is None else timeout)

    def find(self, locator: tuple, timeout=None):
        return self.wait(timeout).until(exp_cond.presence_of_element_located(locator))

    @step('Scrolling into view')
    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    @step('Inserting values')
    def insert(self, *, locator: tuple, text: str, is_clear=False):
        field = self.find(locator)
        if not is_clear:
            field.clear()
        field.send_keys(text)
        self.logger.debug(f'Inserting {text=} at {locator=}')

    @step('Clicking on a locator')
    def click(self, locator: tuple, timeout=10):
        for i in range(CLICK_RETRY):
            try:
                self.logger.debug(f'Try #{i + 1}')
                self.find(locator, timeout)
                self.logger.debug(f'Clicking at {locator=}')
                self.wait(timeout).until(exp_cond.element_to_be_clickable(locator)).click()
                self.logger.debug(f'Click #{i + 1} was successful')
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                self.logger.debug(f'Click #{i + 1} failed')
                if i == CLICK_RETRY - 1:
                    self.logger.error(f'Locator {locator} is unavailable by certain reasons')
                    raise
