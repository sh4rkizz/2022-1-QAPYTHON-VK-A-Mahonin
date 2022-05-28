import json

import allure
import pytest

from http_client.client import HTTPClient
from mock import flask_mock
from mock.flask_mock import DATA
from settings import MOCK_URL


class BaseTest:
    url_mock: str
    client: HTTPClient
    flask_mock: flask_mock

    @pytest.fixture(scope='function', autouse=True)
    def setup(self):
        self.url_mock = MOCK_URL
        self.client = HTTPClient()


@pytest.mark.mock
@allure.epic('Mock server')
@allure.feature(
    '''
    Data inserting, updating, retrieving amd deleting tests
    '''
)
class TestMockServer(BaseTest):
    @allure.story('POST test')
    @allure.description(
        '''
        This test happens to perform
        data insertion with the custom post method
        '''
    )
    def test_post_user(self, human_being):
        user = human_being
        DATA[user['name']] = user['surname']
        post = self.client.post(data=json.dumps(user))

        assert post['status_code'] == '201'
        assert post['body'] == user['surname']

    @allure.story('GET test')
    @allure.description(
        '''
        This test is designed to check if data
        can be reached from the mock server
        '''
    )
    def test_get_user(self, human_being):
        user = human_being
        DATA[user['name']] = user['surname']
        get = self.client.get(params=user['name'])

        assert get['status_code'] == '200'
        assert get['body'] == user['surname']

    @allure.story('PUT test')
    @allure.description(
        '''
        This test is designed to check if data
        can be changed by the unique name
        '''
    )
    def test_update_user(self, human_being):
        user = human_being
        DATA[user['name']] = user['surname']

        resp = self.client.put(params=user)

        assert resp['status_code'] == '202'
        assert resp['body'] == user['surname']

    @allure.story('DELETE test')
    @allure.description(
        '''
        This test is designed to check if data
        can be deleted from the mock server
        '''
    )
    def test_delete_user_surname(self, human_being):
        user = human_being
        DATA[user['name']] = user['surname']
        delete = self.client.delete(params=user['name'])

        assert delete['status_code'] == '204'
        assert not delete['body']

    @allure.story('GET_ALL test')
    def test_get_all_users(self):
        assert self.client.get(params='/users/all')
