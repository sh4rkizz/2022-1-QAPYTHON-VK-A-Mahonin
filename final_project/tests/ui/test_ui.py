from pytest import mark, fixture
from _pytest.fixtures import FixtureRequest
from allure import epic, story, description
from tests.mysql.client import MysqlClient
from tests.ui.pages.main_page import MainPage
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.registration_page import RegistrationPage
from tests.user_builder import create_user, bad_field
from tests.ui.locators import MainPageLocators, LoginPageLocators, RegistrationPageLocators
from settings import StatusCode


class BaseTest:
    config = logger = main_page = login_page = registration_page = mysql_client = None
    test_username = 'sharkizz'
    test_password = '123'
    is_authorized = True

    @fixture(scope='function', autouse=True)
    def setup(self, config, driver, mysql_client, request: FixtureRequest, logger):
        self.config = config
        self.logger = logger

        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')
        self.mysql_client: MysqlClient = mysql_client

        if self.is_authorized:
            user = create_user(username=self.test_username, password=self.test_password)

            if self.mysql_client.find_user(user.username) is None:
                self.mysql_client.delete_user(user)
                self.logger.debug(f'Creating test user {user.username}:{user.password}')
                self.mysql_client.add_user(user)

            assert self.mysql_client.find_user(user.username)
            self.main_page: MainPage = request.getfixturevalue('autologin')

        self.logger.info('UI tests setup was finished')

    @fixture(scope='function')
    def new_user(self):
        return create_user()


@epic('Login page tests')
class TestLogin(BaseTest):
    is_authorized = False

    @story('Login test')
    @description(
        '''Test is used to show what
        happens when correct data is
        inserted in the login UI fields'''
    )
    def test_login_user(self):
        self.login_page.login_user(username=self.test_username, password=self.test_password)
        assert self.main_page.find(MainPageLocators.FOOTER)

    @story('Login test')
    @description(
        '''Test is used to show what
        happens when wrong, but syntactically
        correct data is inserted in the login UI fields'''
    )
    def test_login_user_negative(self, new_user):
        self.login_page.login_user(username=new_user.username, password=new_user.password)
        assert self.login_page.find(LoginPageLocators.INVALID_MESSAGE)

    @story('Login with short username')
    @description(
        '''Test is used to show what
        will happen if your username is too short :c'''
    )
    def test_login_user_short_username(self, new_user, username_length=4):
        self.login_page.login_user(username=bad_field(username_length), password=new_user.password)

        assert (
                self.login_page
                .find(self.login_page.locators.USERNAME)
                .get_attribute('validationMessage') ==
                f'Минимально допустимое количество символов: 6. Длина текста сейчас: {username_length}.'
        )

    @story('Trying to login without a password')
    @description(
        '''Test is trying to show you what
        will you do if you forget your password'''
    )
    def test_login_user_empty_password(self, new_user):
        self.login_page.login_user(
            username=new_user.username,
            password=''
        )

        assert (
                self.login_page
                .find(self.login_page.locators.PASSWORD)
                .get_attribute('validationMessage') == f'Заполните это поле.'
        )

    @story('Trying to login without a username')
    @description(
        '''Test is trying to show you what
        will you do if you forget your username'''
    )
    def test_login_user_empty_username(self, new_user):
        self.login_page.login_user(
            username='',
            password=new_user.password
        )

        assert (
                self.login_page
                .find(self.login_page.locators.USERNAME)
                .get_attribute('validationMessage') == f'Заполните это поле.'
        )

    @story('Trying to enter blocked account')
    @description(
        '''Test will show what will happen if you forgot
        that you were banned, but still tried to log in'''
    )
    def test_blocked_user_login(self, new_user):
        self.mysql_client.add_user(user=new_user, access=StatusCode.BLOCKED)
        assert self.mysql_client.find_user(username=new_user.username)

        self.login_page.login_user(username=new_user.username, password=new_user.password)
        assert 'Ваша учетная запись заблокирована' in self.login_page.driver.page_source

        self.mysql_client.delete_user(new_user.username)
        assert self.mysql_client.find_user(username=new_user.username) is None

    @story('Migration test')
    @description(
        '''Test is used to check if the migration
        to the registration page from the login
        page via link is performed correctly'''
    )
    def test_migrate_to_registration_page(self):
        self.login_page.migrate_to_registration_page()


@epic('Registration page tests')
class TestRegistrationPage(BaseTest):
    is_authorized = False

    @story('Registration test')
    @description(
        '''This test is used to check the process
        of the new account being registered'''
    )
    def test_register_user(self, new_user):
        self.login_page.migrate_to_registration_page()
        self.registration_page.register_new_account(user=new_user)
        assert self.mysql_client.find_user(new_user.username)

        self.mysql_client.delete_user(new_user.username)
        assert self.mysql_client.find_user(new_user.username) is None

    @story('Trying to register without password confirmation')
    @description(
        '''Test will show what will happen if
        you will not confirm your password in
        the register fields'''
    )
    def test_register_user_incorrect_confirm_password(self, new_user):
        new_user.confirm = ''
        self.login_page.migrate_to_registration_page()
        self.registration_page.register_new_account(user=new_user)
        assert 'Passwords must match' in self.registration_page.driver.page_source

    @mark.negative
    @story('Strange behaviour behind the scenes')
    @description(
        '''Test will show that will happen if
        two or more fields are incorrect'''
    )
    def test_register_user_incorrect_password_and_email(self, new_user):
        new_user.confirm = ''
        new_user.email = ''
        self.login_page.migrate_to_registration_page()
        self.registration_page.register_new_account(user=new_user)
        assert '{\'email\': [\'Incorrect email length\', \'Invalid email address\'], \'password\': [\'Passwords must match\']}' \
               in self.registration_page.driver.page_source

    @story('Trying to register with very short username')
    @description(
        '''Test will show what will happen if
        you will try to create an account with very short username'''
    )
    def test_register_user_incorrect_username_length(self, new_user, username_length=4):
        new_user.username = bad_field(username_length)
        self.login_page.migrate_to_registration_page()
        self.registration_page.register_new_account(user=new_user)

        assert (
                self.registration_page
                .find(self.registration_page.locators.USERNAME)
                .get_attribute('validationMessage') ==
                f'Минимально допустимое количество символов: 6. Длина текста сейчас: {username_length}.'
        )

    @mark.negative
    @mark.parametrize('email', ['+++++++@mail.ru', 'плохой_мейл@mail.ru'])
    @story('Trying to register with obviously wrong email')
    @description(
        '''Test uses parametrization, '''
    )
    def test_register_user_incorrect_email(self, new_user, email):
        new_user.email = email
        self.login_page.migrate_to_registration_page()
        self.registration_page.register_new_account(user=new_user)

        assert self.mysql_client.find_user(new_user.username)

        self.mysql_client.delete_user(new_user.username)
        assert self.mysql_client.find_user(new_user.username) is None

    def test_register_user_existing_username(self, new_user):
        self.mysql_client.add_user(new_user)
        assert self.mysql_client.find_user(username=new_user.username)

        user = create_user(username=new_user.username)
        self.login_page.migrate_to_registration_page()
        self.registration_page.register_new_account(user=user)
        assert 'User already exist' in self.registration_page.driver.page_source

        self.mysql_client.delete_user(new_user.username)
        assert self.mysql_client.find_user(new_user.username) is None

    @story('Migration test')
    @description(
        '''Test is used to check if the migration
        to the registration page from the login
        page via link is performed correctly.
        Since start page is the login page,
        test migrates to the registration page first'''
    )
    def test_migrate_to_registration_page(self):
        self.login_page.migrate_to_registration_page()
        assert self.registration_page.find(RegistrationPageLocators.SDET_ACCEPT)


class TestMainPage(BaseTest):
    def test_logout(self, autologin):
        self.main_page.logout()
        user = self.mysql_client.find_user(self.test_username)

        assert user.active == StatusCode.INACTIVE
        assert 'Welcome to the TEST SERVER' in self.login_page.driver.page_source

    def test_migrate_to_python_page(self, autologin):
        self.main_page.migrate_to_python_page()
        assert self.main_page.driver.current_url == 'https://www.python.org/'

    def test_migrate_to_python_history_page(self, autologin):
        self.main_page.migrate_to_python_history_page()
        assert 'History of Python' in self.main_page.driver.page_source

    def test_migrate_to_flask_page(self, autologin):
        self.main_page.migrate_to_flask_page()
        assert 'User’s Guide' in self.main_page.driver.page_source

    def test_migrate_to_centos_page(self, autologin):
        self.main_page.migrate_to_centos_page()
        assert 'Мы рады, что вы решили попробовать Fedora Workstation' in self.main_page.driver.page_source

    def test_migrate_to_news(self, autologin):
        self.main_page.migrate_to_news_page()
        assert 'What’s New' in self.main_page.driver.page_source

    def test_migrate_to_download_page(self, autologin):
        self.main_page.migrate_to_download_page()
        assert 'Download Wireshark' in self.main_page.driver.page_source

    def test_migrate_to_examples_page(self, autologin):
        self.main_page.migrate_to_examples_page()
        assert 'Tcpdump Examples' in self.main_page.driver.page_source

    def test_migrate_to_api_page(self, autologin):
        self.main_page.migrate_to_api_page()
        assert '<title>API - Wikipedia</title>' in self.main_page.driver.page_source

    def test_migrate_to_internet_future_page(self):
        self.main_page.migrate_to_internet_future_page()
        assert 'What Will the Future of the Internet Look Like?' in self.main_page.driver.page_source

    def test_migrate_to_smtp_page(self):
        self.main_page.migrate_to_smtp_page()
        assert 'Simple Mail Transfer Protocol' in self.main_page.driver.page_source
