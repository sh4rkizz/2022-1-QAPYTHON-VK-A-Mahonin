from allure import step

from selenium.common.exceptions import TimeoutException

from UI.locators.basic_locators import MainPageLocators
from UI.pages.base_page import BasePage
from UI.pages.campaign_page import CampaignPage
from UI.pages.segment_page import SegmentPage


class MainPage(BasePage):
    url = 'https://target.my.com/dashboard'
    locators = MainPageLocators()

    @step('Open campaign page')
    def open_campaign(self) -> CampaignPage:
        try:
            locator = self.locators.CREATE_CAMPAIGN
            self.find(locator)
        except TimeoutException:
            locator = self.locators.CREATE_NEW_CAMPAIGN
        finally:
            self.logger.info('Migrating to the campaign creation page')

        self.click(locator)
        return CampaignPage(self.driver)

    @step('Open segment page')
    def open_segment(self) -> SegmentPage:
        self.click(self.locators.SEGMENT_PAGE)
        self.logger.info('Migrating to the segment creation page')
        return SegmentPage(self.driver)
