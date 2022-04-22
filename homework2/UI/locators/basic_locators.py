from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN = (By.XPATH, '//*[contains(@class, "responseHead-module-button")]')
    EMAIL = (By.NAME, 'email')
    PASSWORD = (By.NAME, 'password')
    LOGIN_SUBMIT = (By.XPATH, '//*[contains(@class, "authForm-module-button")]')

    ERROR_BANNER = (By.XPATH, '//div[@class="formMsg js_form_msg"]')


class BasePageLocators:
    BUTTON_MENU = (By.XPATH, '//*[contains(@class, "center-module-buttonsWrap")]')
    CAMPAIGNS = (By.XPATH, '//*[contains(@class, "center-module") and contains(@href, "/dashboard")]')
    AUDIENCE = (By.XPATH, '//*[contains(@class, "center-module") and contains(@href, "/segments")]')


class MainPageLocators(BasePageLocators):
    CREATE_CAMPAIGN = (By.XPATH, '//a[@href="/campaign/new"]')
    CREATE_NEW_CAMPAIGN = (By.XPATH, '//div[contains(@class, "button-module-textWrapper")]')
    CREATED_CAMPAIGN = (By.XPATH, '//a[contains(@class, "nameCell-module-campaignName") and @title="{}"]')
    SEGMENT_PAGE = (By.XPATH, '//a[@href="/segments"]')


class CampaignPageLocators(MainPageLocators):
    CAMPAIGN_TARGET = (By.XPATH, '//div[contains(@class, "column-list-item {}")]')
    INSERT_URL = (By.XPATH, '//input[@data-gtm-id="ad_url_text"]')
    CLEAR_CAMPAIGN_NAME = (By.XPATH, '//div[@class="input__clear js-input-clear"]')
    CAMPAIGN_NAME = (By.XPATH, '//input[@data-translated-attr="placeholder"]')
    AD_FORMAT_BANNER = (By.ID, 'patterns_banner_4')
    UPLOAD_IMAGE_BUTTON = (By.XPATH, '//div[contains(@class, "roles-module-buttonWrap")]/'
                                     'div[contains(@class, "upload-module-wrapper")]//input')
    SAVE_PHOTO = (By.XPATH, '//input[@class="image-cropper__save js-save"]')
    SUBMIT = (By.XPATH, '//div[@class="footer__button js-save-button-wrap"]')


class SegmentPageLocators(BasePageLocators):
    CREATE_SEGMENT = (By.XPATH, '//a[@href ="/segments/segments_list/new/"]')
    COUNT_SEGMENTS = (By.XPATH, '//a[@href="/segments/segments_list"]/span[contains(@class, "item-count")]')
    SEGMENT_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and contains(@class, "adding-segments-source")]')
    ADD_SEGMENT = (By.XPATH, '//div[@class="adding-segments-modal__btn-wrap js-add-button"]')

    SEGMENT_NAME = (By.XPATH, '//input[@maxlength="60" and contains(@class,"input__inp")]')
    CREATE_NEW_SEGMENT = (By.XPATH, '//button[@data-class-name="Submit"]')
    SEGMENT_LIST = (By.XPATH, '//a[contains(@href, "/segments/segments_list/") and @title="{}"]')

    ROW = (By.XPATH, '//a[@title="{}"]')
    ROW_TICK = (By.XPATH, '//*[contains(@data-test, "id-{}")]//input')

    ACTIONS = (By.XPATH, '//*[@data-test="select" and contains(@class, "segmentsTable")]')
    DELETE_SEGMENT = (By.XPATH, '//*[@data-id="remove"]')
