import allure

from UI.pages.base_page import BasePage
from UI.locators.basic_locators import SegmentPageLocators
from selenium.webdriver.support import expected_conditions as exp_cond


class SegmentPage(BasePage):
    url = 'https://target.my.com/segments/segments_list'
    locators = SegmentPageLocators()

    @allure.step('Segment creation')
    def create_segment(self, name):
        self.wait().until(exp_cond.element_to_be_clickable(self.locators.COUNT_SEGMENTS))

        locator = self.locators.CREATE_SEGMENT \
            if self.find(self.locators.COUNT_SEGMENTS, 10).text == '0' else self.locators.CREATE_NEW_SEGMENT

        self.click(locator)
        self.click(self.locators.SEGMENT_CHECKBOX)
        self.click(self.locators.ADD_SEGMENT)
        self.insert(self.locators.SEGMENT_NAME, name)
        self.click(self.locators.CREATE_NEW_SEGMENT)
        created_segment = self.find(
            (
                self.locators.SEGMENT_LIST[0],
                self.locators.SEGMENT_LIST[1].format(name)
            )
        )

        return created_segment.text

    @allure.step('Segment deletion')
    def delete_segment(self, name):
        segment_name = self.create_segment(name)

        if name != segment_name:
            raise

        segment_locator = (
            self.locators.SEGMENT_LIST[0],
            self.locators.SEGMENT_LIST[1].format(name)
        )
        segment = self.find(segment_locator)

        row = segment.find_element_by_xpath('../..')
        row_id = row.get_attribute('data-row-id')

        delete_locator = (
            self.locators.DELETE_SEGMENT[0],
            self.locators.DELETE_SEGMENT[1].format(row_id)
        )

        self.click(delete_locator)
        self.click(self.locators.SUBMIT_DELETION)

        return exp_cond.invisibility_of_element_located(segment_locator)
