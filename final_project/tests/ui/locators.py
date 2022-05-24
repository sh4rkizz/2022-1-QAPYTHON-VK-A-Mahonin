from selenium.webdriver.common.by import By


class BasePageLocators:
    SUBMIT = (By.ID, 'submit')
    PASSWORD = (By.ID, 'password')
    USERNAME = (By.ID, 'username')


class LoginPageLocators(BasePageLocators):
    GREETING_MESSAGE = (By.XPATH, '[text()="Welcome to the TEST SERVER"]')
    REGISTRATION = (By.XPATH, '//a[@href="/reg"]')
    INVALID_MESSAGE = (By.ID, 'flash')


class RegistrationPageLocators(BasePageLocators):
    NAME = (By.ID, 'user_name')
    LAST_NAME = (By.ID, 'user_surname')
    MIDDLE_NAME = (By.ID, 'user_middle_name')
    EMAIL = (By.ID, 'email')
    REPEAT_PASSWORD = (By.NAME, 'confirm')

    SDET_ACCEPT = (By.NAME, 'term')
    LOGIN_PAGE = (By.XPATH, '//a[@href="/login"]')


class MainPageLocators(BasePageLocators):
    LOGOUT = (By.XPATH, '//a[@href="/logout"]')
    LOGIN_USERNAME = (By.XPATH, '//div[id="login-name"]//li[text()="Logged as"]')
    LOGIN_NAME = (By.XPATH, '//div[id="login-name"]//li[text()="User:"]')

    PYTHON = (By.XPATH, '//a[@href="https://www.python.org/"]')
    PYTHON_HISTORY = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/History_of_Python"]')
    FLASK_INFO = (By.XPATH, '//a[@href="https://flask.palletsprojects.com/en/1.1.x/#"]')

    LINUX = (By.XPATH, '//a[@href="javascript:"]')
    CENTOS = (By.LINK_TEXT, 'Download Centos7')

    NETWORK = (By.LINK_TEXT, 'Network')
    NEWS = (By.XPATH, '//a[text()="News"]')
    DOWNLOAD = (By.XPATH, '//a[text()="Download"]')
    EXAMPLES = (By.XPATH, '//a[contains(text(), "Examples")]')

    API = (By.XPATH, '//div[contains(text(),"API")]/parent::div/figure')
    FUTURE_OF_INTERNET = (By.XPATH, '//div[contains(text(),"Future")]/parent::div/figure')
    SMTP = (By.XPATH, '//div[contains(text(),"SMTP")]/parent::div/figure')

    FOOTER = (By.XPATH, '//p[contains(text(),"Powered by")]')
