from logging import getLogger
from urllib.parse import urljoin

import requests
from allure import step

from settings import StatusCode
from tests.user_builder import User


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:
    def __init__(self, base_url: str):
        self.logger = getLogger('test_final_project')
        self.base_url = base_url

        self.session = requests.Session()

    @step('Create the request with predetermined method and params')
    def _request(self, *, method: str, url: str, headers=None, data=None, exp_status: int = StatusCode.SUCCESS,
                 jsonify=False, params=None, json=None, files: dict = None):
        url = urljoin(self.base_url, url)

        self.logger.debug(f'Performing {method}, {url=}, {headers=} are used, {data=} is being transmitted')

        resp = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            data=data,
            params=params,
            files=files
        )

        self.logger.debug(f'Method={method}, {url=}, collected_status={resp.status_code}')

        if resp.status_code != exp_status:
            self.logger.error(f'Got {resp.status_code} {resp.reason} ({method}) for URL \'{url}\'')
            raise ResponseStatusCodeException(f'Got {resp.status_code} {resp.reason} ({method}) for URL \'{url}\'')

        return resp.json() if jsonify else resp

    @step('Get headers for the HTTP request')
    def _post_headers(self) -> dict:
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }

    @step('Get app status')
    def get_status(self):
        url = '/status'
        headers = self._post_headers()

        return self._request(method='GET', url=url, headers=headers)

    @step('Post auth request')
    def post_login_user(self, username, password):
        url = '/login'
        headers = self._post_headers()
        data = {
            'username': f'{username}',
            'password': f'{password}',
            'submit': 'Login'
        }
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        self._request(
            method='POST',
            url=url,
            headers=headers,
            data=data,
        )

    @step('Post user creation request')
    def post_add_user(self, user: User, expected_status=StatusCode.CREATED, headers=None):
        url = '/api/user'
        headers = self._post_headers() if headers is None else headers
        data = {
            'name': user.name,
            'surname': user.surname,
            'middlename': user.middle_name,
            'username': user.username,
            'password': user.password,
            'email': user.email,
        }

        return self._request(
            method='POST',
            url=url,
            headers=headers,
            json=data,
            exp_status=expected_status
        )

    @step('Delete user request')
    def delete_user(self, username, expected_status=StatusCode.NO_CONTENT):
        url = f'/api/user/{username}'

        return self._request(
            method='DELETE',
            url=url,
            exp_status=expected_status,
            jsonify=False
        )

    def put_change_password(self, username, new_password, expected_status=StatusCode.SUCCESS):
        url = f'/api/user/{username}/change-password'

        return self._request(
            method='PUT',
            url=url,
            headers=self._post_headers(),
            json={'password': new_password},
            exp_status=expected_status)

    @step('Block user')
    def post_block_user(self, username, expected_status=StatusCode.SUCCESS):
        url = f'/api/user/{username}/block'

        self._request(method='POST', url=url, headers=self._post_headers(), exp_status=expected_status)

    @step('Unblock user')
    def post_unblock_user(self, username, expected_status=StatusCode.SUCCESS):
        url = f'/api/user/{username}/accept'

        self._request(method='POST', url=url, headers=self._post_headers(), exp_status=expected_status)
