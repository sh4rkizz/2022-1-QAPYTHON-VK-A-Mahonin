from allure import step
from selenium.webdriver.support import expected_conditions as exp_cond
from UI.locators.basic_locators import LoginPageLocators
from UI.pages.base_page import BasePage


class PageNotLoadedException(Exception):
    pass


class LoginPage(BasePage):
    locators = LoginPageLocators()

    @step('Login user')
    def login_user(self, email='ewe2002ewe@mail.ru', password='Qwerty123'):
        self.find(self.locators.LOGIN).click()
        self.insert(
            locator=self.locators.EMAIL,
            text=email
        )
        self.insert(
            locator=self.locators.PASSWORD,
            text=password
        )
        self.logger.info(f'Logging in with email: {email} and password: {password}')
        self.click(self.locators.LOGIN_SUBMIT)
        self.wait().until(exp_cond.url_changes)
