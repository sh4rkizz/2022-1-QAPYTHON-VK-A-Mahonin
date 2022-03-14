import string

import random
from UI.locators import basic_locators

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp_cond
from selenium.common.exceptions import StaleElementReferenceException, \
    ElementClickInterceptedException, \
    TimeoutException

import pytest

CLICK_RETRY = 5


class BaseCase:
    driver = None
    email = None
    password = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.password = 'Qwerty123'
        self.email = 'ewe2002ewe@mail.ru'
        self.driver = driver

    def user_migrations(self, button: str):
        self.wait().until(exp_cond.presence_of_element_located(basic_locators.PROFILE))
        self.click(basic_locators.MIGRATION_BUTTON[button])
        self.wait().until(exp_cond.url_changes)

    def profile_edit(self):
        self.click(basic_locators.PROFILE)
        self.wait().until(exp_cond.presence_of_element_located(basic_locators.PROFILE_FULLNAME))

        generator = lambda alphabet, s: ''.join([random.choice(alphabet) for _ in range(random.randint(s[0], s[1]))])

        self.insert(
            basic_locators.PROFILE_FULLNAME,
            ' '.join([generator(string.ascii_lowercase, [4, 9]) for _ in range(3)])
        )
        self.insert(
            basic_locators.PROFILE_PHONE,
            f'8{generator("1234567890", [10, 10])}'
        )
        self.click(basic_locators.PROFILE_ADD_EMAIL_BUTTON)
        self.insert(
            basic_locators.PROFILE_EMAIL,
            f'{generator(string.ascii_lowercase, [4, 15])}@mail.ru'
        )
        self.click(basic_locators.PROFILE_SAVE)
        notification = self.wait().until(exp_cond.visibility_of_any_elements_located(
            basic_locators.PROFILE_EDIT_RESPONSE))[0]
        return notification.find_element_by_xpath('//div').text

    def wait(self, timeout=None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=5 if timeout is None else timeout)

    @pytest.fixture(scope='function')
    def login(self, setup):
        self.find(basic_locators.LOGIN).click()
        self.insert(basic_locators.EMAIL, self.email)
        self.insert(basic_locators.PASSWORD, self.password)
        self.click(basic_locators.LOGIN_SUBMIT)
        self.wait().until(exp_cond.url_changes)

    def insert(self, locator: tuple, text: str):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def find(self, locator: tuple, timeout=None):
        return self.wait(timeout).until(exp_cond.presence_of_element_located(locator))

    def user_logout(self):
        self.wait(10).until(exp_cond.visibility_of_element_located(basic_locators.USER_MENU_WRAP))
        self.click(basic_locators.USER_MENU)
        self.wait().until(exp_cond.presence_of_element_located(basic_locators.SLIDING_USER_MENU))
        self.click(basic_locators.LOGOUT)

    def click(self, locator: tuple, timeout=None):
        for i in range(CLICK_RETRY):
            try:
                self.find(locator, timeout)
                self.wait(timeout).until(exp_cond.element_to_be_clickable(locator)).click()
                return
            except TimeoutException:
                self.driver.refresh()
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if i == CLICK_RETRY - 1:
                    raise
