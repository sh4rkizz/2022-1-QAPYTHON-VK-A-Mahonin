import allure
import pytest

from UI.pages.campaign_page import CampaignPage
from UI.pages.segment_page import SegmentPage
from base import BaseCase

@pytest.mark.ui()
class TestLogin(BaseCase):
    @allure.story('Parametrized negative login test')
    @allure.description(
        '''Test is used to test what
        happens when wrong auth data would be
        inserted in email and password fields'''
    )
    @pytest.mark.parametrize(
        'email, password',
        [
            pytest.param(
                'im_wrong_login@ya.ru',
                'im_wrong_password'
            ),
            pytest.param(
                'another_try_but_still_not_good@gmail.com',
                'sad_but_true'
            )
        ]
    )
    def test_negative_login_user(self, email, password):
        self.login_page.login_user(email, password)
        assert self.main_page.url != self.driver.current_url


@pytest.mark.ui()
class TestCampaign(BaseCase):
    @allure.story('Campaign creation test')
    @allure.description(
        '''Test is used to perform campaign creation
        tasks repeatedly to check if the campaign
        will be created with .png photo of a cute little cat 
        as an AD banner or the creation process fails'''
    )
    def test_create_campaign(self, autologin, photo_path):
        campaign_page = self.main_page.open_campaign()

        assert isinstance(campaign_page, CampaignPage)
        assert campaign_page.create_campaign(photo_path)


@pytest.mark.ui()
@allure.story('Segment creation/deletion tests')
class TestSegment(BaseCase):
    @allure.description(
        '''Test is designed to check segment creation
        capabilities of target.my service'''
    )
    def test_create_segment(self, autologin, randomize_name):
        segment_page = self.main_page.open_segment()
        assert isinstance(segment_page, SegmentPage)
        created_segment = segment_page.create_segment(randomize_name)
        assert randomize_name == created_segment

    @allure.description(
        '''Test is used to check segment deletion
        capabilities of target.my service'''
    )
    def test_delete_segment(self, autologin, randomize_name):
        segment_page = self.main_page.open_segment()
        assert isinstance(segment_page, SegmentPage)
        assert segment_page.delete_segment(randomize_name)
