from allure import step
import logging

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as exp_cond
from selenium.webdriver.support.wait import WebDriverWait

from tests.ui.locators import BasePageLocators


class PageNotLoadedException(Exception):
    pass


class BasePage(object):
    click_retry = 5
    locators = BasePageLocators()
    logger = logging.getLogger('final_project_test')

    def __init__(self, driver):
        self.driver = driver
        self.action_chains = ActionChains(self.driver)
        self.logger.debug(f'{self.__class__.__name__} page is being opened')

    def wait(self, timeout=None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=10 if timeout is None else timeout)

    def find(self, locator: tuple, timeout=None):
        return self.wait(timeout).until(exp_cond.presence_of_element_located(locator))

    def go_by_link_slider(self, slider_locator, target_locator):
        self.action_chains.move_to_element(self.find(slider_locator)).perform()
        self.action_chains.move_to_element(self.find(target_locator)).click().perform()
        self.driver.switch_to.window(self.driver.window_handles[-1])

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
        for i in range(self.click_retry):
            try:
                self.logger.debug(f'Try #{i + 1}')
                self.find(locator, timeout)
                self.logger.debug(f'Clicking at {locator=}')
                self.wait(timeout).until(exp_cond.element_to_be_clickable(locator)).click()
                self.logger.debug(f'Click #{i + 1} was successful')
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                self.logger.debug(f'Click #{i + 1} failed')
                if i == self.click_retry - 1:
                    self.logger.error(f'Locator {locator} is unavailable by certain reasons')
                    raise
