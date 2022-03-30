import logging

import allure

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.support import expected_conditions as exp_cond
from UI.locators.basic_locators import BasePageLocators
from selenium.webdriver.support.wait import WebDriverWait

CLICK_RETRY = 5
TIMEOUT = 3


class PageNotLoadedException(Exception):
    pass


class BasePage(object):
    url = 'https://target.my.com/'
    locators = BasePageLocators()

    def __init__(self, driver):
        self.logger = logging.getLogger('Start test')
        self.logger.info(f'{self.__class__.__name__} page is being opened')
        self.driver = driver

    def wait(self, timeout=None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=10 if timeout is None else timeout)

    def find(self, locator: tuple, timeout=None):
        return self.wait(timeout).until(exp_cond.presence_of_element_located(locator))

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def insert(self, locator: tuple, text: str):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)
        self.logger.info(f'Insert \'{text}\' at \'{locator}\'')

    @allure.step('Clicking {locator}')
    def click(self, locator: tuple, timeout=10):
        for i in range(CLICK_RETRY):
            try:
                self.find(locator, timeout)
                self.wait(timeout).until(exp_cond.element_to_be_clickable(locator)).click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if i == CLICK_RETRY - 1:
                    raise
