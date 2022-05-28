from logging import getLogger
from urllib.parse import urljoin

import requests
from allure import step
from requests import Response


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:
    def __init__(self, base_url: str, login: str, password: str):
        self.logger = getLogger('test_api')
        self.base_url = base_url
        self.login = login
        self.password = password
        self.csrf_token = None

        self.session = requests.Session()

    @step('Create the request with predetermined method and params')
    def _request(self, *, method: str, url: str, headers: dict = None, data: dict = None, exp_status: int = 200,
                 jsonify: bool = True, params: dict = None, json: dict = None, files: dict = None):

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

        if jsonify:
            return resp.json()

        return resp

    @step('Get headers for the HTTP request')
    def _post_headers(self) -> dict:
        return {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'X-CSRFToken': self.csrf_token,
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                ' AppleWebKit/537.36 (KHTML, like Gecko)'
                ' Chrome/100.0.4896.75 Safari/537.36',
        }

    @step('Get csrf-token')
    def _get_token(self, login: str, password: str):
        url = 'https://auth-ac.my.com/auth'

        headers = self._post_headers()
        headers.update({'Referer': 'https://target.my.com/'})

        data = {
            'email': login,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        self.logger.info(f'Authorizing with credentials {login=}, {password=}')
        self.session.request('POST', url, headers=headers, data=data, allow_redirects=False)

    @step('Target.my authorization')
    def post_login(self, login, password) -> Response:
        url = '/csrf'
        self._get_token(login, password)

        resp = self._request(method='GET', url=url, jsonify=False)
        self.csrf_token = resp.headers.get('set-cookie').split(';')[0].split('=')[-1]

        self.logger.info(f'Receiving {self.csrf_token=}')

        return resp

    @step('Segment creation process')
    def post_create_segment(self, segment_name: str) -> bool:
        self.logger.info(f'Starting segment by the name of {segment_name} creation process')
        segment_id, segment_list = self._create_segment(segment_name)
        self.logger.info(f'Segment {segment_name} was created successfully')

        return segment_id in [segment.get('id') for segment in segment_list.get('items')]

    @step('Segment parameters preparation process')
    def _create_segment(self, segment_name: str) -> tuple[id, dict]:
        url = '/api/v2/remarketing/segments.json'

        headers = self._post_headers()
        self.logger.debug('Setting up headers for the HTTP request')

        segment = {
            'name': segment_name,
            'pass_condition': 1,
            'relations': [
                {
                    'object_type': 'remarketing_player',
                    'params': {
                        'type': 'positive',
                        'left': 365,
                        'right': 0
                    }
                }
            ]
        }

        self.logger.debug(f'Creating segment {segment_name}')
        return (
            self._request(method='POST', url=url, headers=headers, json=segment).get('id'),
            self._request(method='GET', url=url, params={'limit': 100})
        )

    @step('Segment creation process')
    def post_delete_segment(self, segment_name: str) -> bool:
        segment_id, _ = self._create_segment(segment_name)
        url = f'/api/v2/remarketing/segments/{segment_id}.json'

        headers = self._post_headers()
        self.logger.info('Starting segment deletion process')

        self._request(method='DELETE', url=url, headers=headers, jsonify=False, exp_status=204)
        segment_list_after = self._request(method='GET', url='/api/v2/remarketing/segments.json')

        self.logger.info(f'Segment {segment_name} was deleted successfully')

        return segment_id not in [segment.get('id') for segment in segment_list_after.get('items')]

    @step('Campaign creation process')
    def post_create_campaign(self, campaign_name: str, photo_path: str) -> id:
        self.logger.info(f'Starting campaign by the name of {campaign_name} creation process')

        headers = self._post_headers()
        promo_url = '/api/v1/urls/'

        self.logger.debug('Getting promotion url id')
        url_id = self._request(
            method='GET',
            url=promo_url,
            headers=headers,
            params={'url': 'https://github.com/sh4rkizz'},
            jsonify=True
        ).get('id')

        photo = {'file': open(photo_path, 'rb'), }
        photo_url = '/api/v2/content/static.json'

        self.logger.debug('Getting photo id')
        photo_id = self._request(
            method='POST',
            url=photo_url,
            headers=headers,
            files=photo
        ).get('id')

        campaign_id = self._create_campaign(
            campaign_name=campaign_name,
            prom_url_id=url_id,
            photo_id=photo_id
        )
        self.logger.info(f'Campaign {campaign_name} was created successfully')

        return (
            campaign_id,
            self._request(
                method='DELETE',
                url=f'/api/v2/campaigns/{campaign_id}.json',
                headers=headers,
                exp_status=204,
                jsonify=False
            )
        )

    @step('Campaign parameters preparation process')
    def _create_campaign(self, campaign_name: str, prom_url_id: int, photo_id: int) -> id:
        url = '/api/v2/campaigns.json'

        headers = self._post_headers()
        self.logger.debug('Setting up headers for the HTTP request')

        campaign = {
            'name': campaign_name,
            'package_id': 961,
            'objective': 'traffic',
            'banners': [
                {
                    'urls': {
                        'primary': {
                            'id': prom_url_id
                        }
                    },
                    'textblocks': {},
                    'content': {
                        'image_240x400': {
                            'id': photo_id
                        }
                    },
                    'name': 'very cute photo'
                }
            ]
        }
        self.logger.debug(f'Creating campaign {campaign_name}')
        return self._request(method='POST', url=url, headers=headers, json=campaign).get('id')

    @step('Get each created campaign (limit 200)')
    def get_all_campaigns(self):
        self.logger.debug('Receiving campaign list')
        return self._request(
            method='GET',
            url='/api/v2/campaigns.json',
            params={'limit': 200}
        )['items']
