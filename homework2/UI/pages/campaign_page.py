import allure

from UI.locators.basic_locators import CampaignPageLocators
from UI.pages.base_page import BasePage


class CampaignPage(BasePage):
    url = 'https://target.my.com/campaign/new'
    locators = CampaignPageLocators()

    @allure.step('Campaign creation')
    def create_campaign(self, photo_path, promotion_url='https://github.com/sh4rkizz', target='_traffic'):
        # Choose the goal and insert link for promotion
        self.click(
            (
                self.locators.CAMPAIGN_TARGET[0],
                self.locators.CAMPAIGN_TARGET[1].format(target)
            )
        )
        self.insert(self.locators.INSERT_URL, promotion_url)

        # Get campaign name
        campaign_name = self.find(self.locators.CAMPAIGN_NAME)
        self.scroll_to(campaign_name)
        campaign_name = campaign_name.get_attribute('value')

        # Choose AD format
        self.scroll_to(self.find(self.locators.AD_FORMAT_BANNER))
        self.click(self.locators.AD_FORMAT_BANNER)

        # Upload and save the logo
        self.scroll_to(self.find(self.locators.UPLOAD_IMAGE_BUTTON))
        self.find(self.locators.UPLOAD_IMAGE_BUTTON).send_keys(photo_path)
        self.click(self.locators.SAVE_PHOTO)

        # Create the campaign
        self.click(self.locators.SUBMIT_LOCATOR)

        created_campaign = (
            self.locators.CREATED_CAMPAIGN[0],
            self.locators.CREATED_CAMPAIGN[1].format(campaign_name)
        )

        return campaign_name == self.find(created_campaign).text
