from allure import step

from tests.ui.locators import RegistrationPageLocators
from tests.ui.pages.base_page import BasePage
from tests.user_builder import User


class RegistrationPage(BasePage):
    locators = RegistrationPageLocators()
    url = 'http://localhost:8080/reg'

    @step('Performing new account registration')
    def register_new_account(self, user: User) -> User:
        self.logger.info('Trying to perform new account registration')
        self.insert(locator=self.locators.NAME, text=user.name)
        self.insert(locator=self.locators.LAST_NAME, text=user.surname)

        # BUG PRONE
        self.insert(locator=self.locators.MIDDLE_NAME, text=user.middle_name)
        # BUG PRONE

        self.insert(locator=self.locators.USERNAME, text=user.username)
        self.insert(locator=self.locators.EMAIL, text=user.email)
        self.insert(locator=self.locators.PASSWORD, text=user.password)
        self.insert(locator=self.locators.REPEAT_PASSWORD, text=user.confirm)
        self.click(self.locators.SDET_ACCEPT)
        self.click(self.locators.SUBMIT)

        return user

    def migrate_to_login_page(self):
        self.logger.debug('Trying to migrate to the login page')
        self.click(self.locators.LOGIN_PAGE)
