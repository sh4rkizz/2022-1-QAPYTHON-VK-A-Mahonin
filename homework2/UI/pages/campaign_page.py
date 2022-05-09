from allure import step

from UI.locators.basic_locators import CampaignPageLocators
from UI.pages.base_page import BasePage


class CampaignPage(BasePage):
    url = 'https://target.my.com/campaign/new'
    locators = CampaignPageLocators()

    @step('Create campaign')
    def create_campaign(self, photo_path: str, campaign_name: str,
                        promotion_url='https://github.com/sh4rkizz', target='_traffic'):
        self.logger.info('Campaign creation has started')
        self.click(
            (
                self.locators.CAMPAIGN_TARGET[0],
                self.locators.CAMPAIGN_TARGET[1].format(target)
            )
        )
        self.logger.debug(f'Choosing the main target of the campaign: {target}')

        self.insert(
            locator=self.locators.INSERT_URL,
            text=promotion_url
        )
        self.logger.debug(f'Filling the {promotion_url}')
        self.logger.debug(f'Locator {self.locators.INSERT_URL}')

        self.scroll_to(
            self.find(self.locators.CAMPAIGN_NAME)
        )
        self.click(self.locators.CLEAR_CAMPAIGN_NAME)
        self.insert(
            locator=self.locators.CAMPAIGN_NAME,
            text=campaign_name,
            is_clear=True
        )
        self.logger.debug(f'Naming future campaign: {campaign_name}')

        self.scroll_to(
            self.find(self.locators.AD_FORMAT_BANNER)
        )
        self.click(self.locators.AD_FORMAT_BANNER)
        self.logger.debug(f'Choosing AD format')

        self.scroll_to(
            self.find(self.locators.UPLOAD_IMAGE_BUTTON)
        )
        self.find(self.locators.UPLOAD_IMAGE_BUTTON).send_keys(photo_path)
        self.click(self.locators.SAVE_PHOTO)
        self.logger.debug(f'Uploading a cute cat as a campaign logo')

        self.click(self.locators.SUBMIT)

        created_campaign = (
            self.locators.CREATED_CAMPAIGN[0],
            self.locators.CREATED_CAMPAIGN[1].format(campaign_name)
        )
        self.logger.info(f'Campaign by the name of {campaign_name} was successfully created')

        return campaign_name == self.find(created_campaign).text
