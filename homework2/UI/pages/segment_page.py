import allure

from UI.pages.base_page import BasePage
from UI.locators.basic_locators import SegmentPageLocators
from selenium.webdriver.support import expected_conditions as exp_cond


class SegmentPage(BasePage):
    url = 'https://target.my.com/segments/segments_list'
    locators = SegmentPageLocators()

    @allure.step('Segment creation')
    def create_segment(self, segment_name):
        self.wait().until(exp_cond.element_to_be_clickable(self.locators.COUNT_SEGMENTS))

        locator = self.locators.CREATE_SEGMENT \
            if self.find(self.locators.COUNT_SEGMENTS, 10).text == '0' else self.locators.CREATE_NEW_SEGMENT

        self.logger.info(f'Segment creation process started')

        self.click(locator)
        self.click(self.locators.SEGMENT_CHECKBOX)
        self.click(self.locators.ADD_SEGMENT)
        self.logger.debug('New segment has been added to the pool')

        self.insert(
            locator=self.locators.SEGMENT_NAME,
            text=segment_name
        )
        self.logger.debug(f'New segment is being named as {segment_name}')

        self.click(self.locators.CREATE_NEW_SEGMENT)
        created_segment = self.find(
            (
                self.locators.SEGMENT_LIST[0],
                self.locators.SEGMENT_LIST[1].format(segment_name)
            )
        )
        self.logger.info(f'Segment by the name of {segment_name} was successfully created')

        return created_segment.text

    @allure.step('Segment deletion')
    def delete_segment(self, segment_name):
        self.logger.info(f'Starting segment {segment_name} deletion process')
        segment_id = self.find(
            (
                self.locators.ROW[0],
                self.locators.ROW[1].format(segment_name)
            )
        ).get_attribute('href')[-1:-7]

        self.click(
            (
                self.locators.ROW_TICK[0],
                self.locators.ROW_TICK[1].format(segment_id)
            )
        )
        self.click(self.locators.ACTIONS)
        self.click(self.locators.DELETE_SEGMENT)
        self.logger.info(f'Segment by the name of {segment_name} was successfully deleted')

        return exp_cond.invisibility_of_element_located(
            (
                self.locators.ROW[0],
                self.locators.ROW[1].format(segment_name)
            )
        )
