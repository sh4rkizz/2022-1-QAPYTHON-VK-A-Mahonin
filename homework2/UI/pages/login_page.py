import allure
from selenium.webdriver.support import expected_conditions as exp_cond
from UI.locators.basic_locators import LoginPageLocators
from UI.pages.base_page import BasePage


class PageNotLoadedException(Exception):
    pass


class LoginPage(BasePage):
    locators = LoginPageLocators()

    @allure.step('Trying logging')
    def login_user(self, email='ewe2002ewe@mail.ru', password='Qwerty123'):
        self.find(self.locators.LOGIN).click()
        self.insert(self.locators.EMAIL, email)
        self.insert(self.locators.PASSWORD, password)
        self.click(self.locators.LOGIN_SUBMIT)
        self.wait().until(exp_cond.url_changes)
