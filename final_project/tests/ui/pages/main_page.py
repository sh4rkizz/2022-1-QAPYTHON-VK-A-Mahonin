from allure import step

from tests.ui.locators import MainPageLocators
from tests.ui.pages.base_page import BasePage


class MainPage(BasePage):
    url = 'http://localhost:8080/welcome/'
    locators = MainPageLocators()

    @step('Logout')
    def logout(self):
        self.click(self.locators.LOGOUT)

    @step('Migrate to the python page')
    def migrate_to_python_page(self):
        self.click(self.locators.PYTHON)

    @step('Migrate to the python history page')
    def migrate_to_python_history_page(self):
        self.go_by_link_slider(self.locators.PYTHON, self.locators.PYTHON_HISTORY)

    @step('Migrate to the flask description page')
    def migrate_to_flask_page(self):
        self.go_by_link_slider(self.locators.PYTHON, self.locators.FLASK_INFO)

    @step('Migrate to the Centos7 page')
    def migrate_to_centos_page(self):
        self.go_by_link_slider(self.locators.LINUX, self.locators.CENTOS)

    @step('Migrate to the news page')
    def migrate_to_news_page(self):
        self.go_by_link_slider(self.locators.NETWORK, self.locators.NEWS)

    @step('Migrate to the wireshark download page')
    def migrate_to_download_page(self):
        self.go_by_link_slider(self.locators.NETWORK, self.locators.DOWNLOAD)

    @step('Migrate to the TCPDUMP examples page')
    def migrate_to_examples_page(self):
        self.go_by_link_slider(self.locators.NETWORK, self.locators.EXAMPLES)

    @step('Migrate to the API description page')
    def migrate_to_api_page(self):
        self.click(self.locators.API)
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])

    @step('Migrate to the future of the Internet description page')
    def migrate_to_internet_future_page(self):
        self.click(self.locators.FUTURE_OF_INTERNET)
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])

    @step('Migrate to the SMTP description page')
    def migrate_to_smtp_page(self):
        self.click(self.locators.SMTP)
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
