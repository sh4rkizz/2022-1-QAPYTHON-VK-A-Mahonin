from allure import step

from tests.ui.locators import LoginPageLocators, RegistrationPageLocators
from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    locators = LoginPageLocators()
    url = 'http://localhost:8080/login'

    @step('Login user')
    def login_user(self, *, username: str, password: str):
        self.logger.info(f'Trying to log into the account with {username=}, {password=}')
        self.insert(locator=self.locators.USERNAME, text=username)
        self.insert(locator=self.locators.PASSWORD, text=password)
        self.click(self.locators.SUBMIT)

    @step('Migrate to the registration page')
    def migrate_to_registration_page(self):
        self.logger.debug('Trying to migrate to the registration page')
        self.click(self.locators.REGISTRATION)
        self.find(RegistrationPageLocators.SDET_ACCEPT)
