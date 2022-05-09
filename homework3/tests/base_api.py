import pytest


class BaseApi:
    authorize = True
    api_client = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, credentials):
        self.api_client = api_client

        if self.authorize:
            self.api_client.post_login(*credentials)
