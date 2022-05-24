from allure import epic, description, story
from pytest import mark, fixture
from api_client import ApiClient
from tests.mysql.client import MysqlClient
from tests.user_builder import create_user, bad_field, User
from settings import StatusCode


class BaseApi:
    authorize = True
    mysql_client = api_client = logger = None

    @fixture(scope='function', autouse=True)
    def setup(self, api_client, mysql_client, logger):
        self.logger = logger
        self.api_client: ApiClient = api_client
        self.mysql_client: MysqlClient = mysql_client

        if self.authorize:
            user = create_user(username='sharkizz', password='123')
            self.api_client.post_login_user(
                username=user.username,
                password=user.password,
            )

    @fixture(scope='function')
    def auto_user(self) -> User:
        user = create_user()
        self.api_client.post_add_user(user=user, expected_status=StatusCode.BUGGED_CREATED)
        assert self.mysql_client.find_user(user.username)

        return user


@epic('Status')
class TestSmoke(BaseApi):
    authorize = False

    @story('Get application status test')
    @description(
        '''Via sending GET request application
        status is being received'''
    )
    def test_status(self):
        response = self.api_client.get_status()

        assert response.status_code == StatusCode.SUCCESS
        assert response.json()['status'] == 'ok'


@epic('Add user')
class TestAddUser(BaseApi):
    @story('Post valid user')
    @description(
        '''Performing POST request to create
        a new user, who will be added to the database
        after his creation'''
    )
    def test_post_add_user(self):
        user = create_user()
        self.api_client.post_add_user(user=user, expected_status=StatusCode.BUGGED_CREATED)
        assert self.mysql_client.find_user(user.username)

        self.mysql_client.delete_user(user.username)
        assert not self.mysql_client.find_user(user.username)

    @story('Post clone username user')
    @description(
        '''Test is designed to research behaviour
         of the application when clone username
        user is being requested to be created'''
    )
    def test_post_add_user_clone_username(self, auto_user):
        user2 = create_user(username=auto_user.username)
        self.api_client.post_add_user(user=user2, expected_status=StatusCode.BAD_REQUEST)
        assert self.mysql_client.find_user(auto_user.username).email == auto_user.email

    @mark.BUG
    @story('Post clone email user')
    @description(
        '''Test is designed to research
        behaviour of the application when clone email
        user is being requested to be created'''
    )
    def test_post_add_user_clone_email(self, auto_user):
        user2 = create_user(email=auto_user.email)
        self.api_client.post_add_user(user=user2, expected_status=StatusCode.INTERNAL_ERROR)
        assert self.mysql_client.find_user(user2.username) is None

    @mark.BUG
    @story('Post incorrect username user')
    @description(
        '''Test is designed to research
        behaviour of the application when
        the wrong username is being used
        to post add a new user'''
    )
    def test_post_add_user_incorrect_username(self):
        user = create_user(username=bad_field())
        self.api_client.post_add_user(user=user, expected_status=StatusCode.BUGGED_CREATED)
        assert self.mysql_client.find_user(user.username)

    @mark.BUG
    @story('Post incorrect email user')
    @description(
        '''Test is designed to research
        behaviour of the application when
        the wrong email is being used
        to post add a new user'''
    )
    def test_post_add_user_incorrect_email(self):
        user = create_user(email=bad_field())
        self.api_client.post_add_user(user=user, expected_status=StatusCode.BUGGED_CREATED)
        assert self.mysql_client.find_user(user.username)

    @mark.BUG
    @story('Post blank user')
    @description(
        '''Test is designed to research
        behaviour of the application when
        none of the required user fields are
        filled'''
    )
    def test_post_add_user_empty(self):
        user = create_user(name='', surname='', middle_name='', username=bad_field(), email=bad_field(), password='')
        self.api_client.post_add_user(user=user, expected_status=StatusCode.BUGGED_CREATED)
        assert self.mysql_client.find_user(user.username)

    @mark.BUG
    @story('Post user with incorrect headers')
    @description(
        '''Test is designed to research
        behaviour of the application when
        the required header to create a user is absent'''
    )
    def test_post_add_user_bad_headers(self):
        user = create_user()
        self.api_client.post_add_user(user=user, expected_status=StatusCode.BUGGED_CREATED, headers={})
        assert self.mysql_client.find_user(user.username)


@epic('Delete user')
class TestDeleteUser(BaseApi):
    @story('Delete user')
    @description(
        '''Test shows the correct deletion
        process handled by the application'''
    )
    def test_delete_user(self, auto_user):
        self.api_client.delete_user(auto_user.username, StatusCode.NO_CONTENT)
        assert self.mysql_client.find_user(auto_user.username) is None

    @story('Delete nonexistent user')
    @description(
        '''Test shows how the handling of
        NOT_FOUND deletion process is being performed'''
    )
    def test_delete_user_nonexistent(self):
        response = self.api_client.delete_user(
            username='This is nonexistent username',
            expected_status=StatusCode.NOT_FOUND
        )
        assert response.status_code == StatusCode.NOT_FOUND


@epic('Put user')
class TestPutUser(BaseApi):
    @story('Update user password')
    @description(
        '''Test shows the correct response of
        the application to the PUT change_password request'''
    )
    def test_put_change_password(self, auto_user):
        self.api_client.put_change_password(
            username=auto_user.username,
            new_password=bad_field(7),
            expected_status=StatusCode.NO_CONTENT
        )
        assert self.mysql_client.find_user(auto_user.username).password != auto_user.password

    @story('Not actually trying to change a password')
    @description(
        '''Test shows what happens when we are not
        actually trying to change a password, but
        leaving it the same in the request body as it was before'''
    )
    def test_put_change_password_same(self, auto_user):
        self.api_client.put_change_password(
            username=auto_user.username,
            new_password=auto_user.password,
            expected_status=StatusCode.BAD_REQUEST
        )
        assert self.mysql_client.find_user(auto_user.username).password == auto_user.password


@epic('Block user')
class TestBlockUser(BaseApi):
    @story('Valid attempt to block the user')
    @description(
        '''Test shows what happens when we are
        requesting to block a user via api'''
    )
    def test_post_block_user(self, auto_user):
        self.api_client.post_block_user(username=auto_user.username)
        assert self.mysql_client.find_user(auto_user.username).access == StatusCode.BLOCKED

    @story('Trying to block a blocked account')
    @description(
        '''Test shows what happens when we are
        requesting to block a blocked user'''
    )
    def test_post_block_blocked(self, auto_user):
        self.api_client.post_block_user(username=auto_user.username)
        assert self.mysql_client.find_user(auto_user.username).access == StatusCode.BLOCKED

        self.api_client.post_block_user(username=auto_user.username, expected_status=StatusCode.BAD_REQUEST)
        assert self.mysql_client.find_user(auto_user.username).access == StatusCode.BLOCKED

    @story('Trying to block a nonexistent account')
    @description(
        '''Test shows what happens when we dont appreciate
        our own sight and tryna ban a person who never existed'''
    )
    def test_post_block_user_nonexistent(self):
        self.api_client.post_block_user(username=bad_field(10), expected_status=StatusCode.NOT_FOUND)


@epic('Unblock user test')
class TestUnblockUser(BaseApi):
    @story('Valid attempt to unblock the user')
    @description(
        '''Test shows what happens when we are
        requesting to unblock a user via api'''
    )
    def test_post_block_user(self, auto_user):
        self.api_client.post_block_user(username=auto_user.username)
        assert self.mysql_client.find_user(auto_user.username).access == StatusCode.BLOCKED

        self.api_client.post_unblock_user(username=auto_user.username)
        assert self.mysql_client.find_user(auto_user.username).access == StatusCode.UNBLOCKED

    @story('Trying to unblock an accepted account')
    @description(
        '''Test shows what happens when we are
        requesting to unblock a user via api'''
    )
    def test_post_unblock_user_unblocked(self, auto_user):
        self.api_client.post_unblock_user(username=auto_user.username, expected_status=StatusCode.BAD_REQUEST)
        assert self.mysql_client.find_user(auto_user.username).access == StatusCode.UNBLOCKED

    @story('Trying to unban nonexistent account')
    @description(
        '''Trying to make sense with
        this nonsense ghost acceptation'''
    )
    def test_post_unblock_user_nonexistent(self):
        self.api_client.post_unblock_user(username=bad_field(10), expected_status=StatusCode.NOT_FOUND)
