import pytest
from allure import story, epic, description
from API.fixtures import randomize_name, photo_path

from tests.base_api import BaseApi


@pytest.mark.api
@epic('Login')
class TestLogin(BaseApi):
    @story('Post login test')
    @description(
        '''
        Test is used to test what
        happens when correct data is
        inserted in the login fields and
        also gets csrf-token to work with in
        the later stages of the program.
        '''
    )
    def test_post_login(self, credentials):
        login_attempt = self.api_client.post_login(*credentials)

        assert login_attempt.url == 'https://target.my.com/csrf'
        assert login_attempt.status_code == 200


@pytest.mark.api
@epic('Campaign')
class TestCampaign(BaseApi):
    @story('Post campaign creation and deletion test')
    @description(
        '''
        Test is used to perform creation and
        deletion of the campaign via post
        and delete methods from requests library,
        after each creation of the campaign it gets
        deleted from the list of active campaigns.
        '''
    )
    def test_create_campaign(self, randomize_name, photo_path):
        campaign_id, campaign = self.api_client.post_create_campaign(randomize_name, photo_path)

        assert campaign_id in [campaign.get('id') for campaign in self.api_client.get_all_campaigns()]
        assert campaign.status_code == 204


@pytest.mark.api
@epic('Segment')
class TestSegment(BaseApi):
    @story('Post segment creation test')
    @description(
        '''
        Test is used to perform creation of new
        segment with predetermined parameters.
        The name of segment is randomly generated
        each iteration of testing. 
        '''
    )
    def test_create_segment(self, randomize_name):
        assert self.api_client.post_create_segment(randomize_name)

    @story('Post segment deletion test')
    @description(
        '''
        Test is used to perform deletion of new
        segment with predetermined parameters.
        Firstly, segment is being created as
        it was before: randomized name and predetermined
        parameters. After the creation of the segment
        comes its deletion, which is performed
        via delete method.  
        '''
    )
    def test_delete_segment(self, randomize_name):
        assert self.api_client.post_delete_segment(randomize_name)
