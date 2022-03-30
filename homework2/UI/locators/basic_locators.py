from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN = (By.XPATH, '//*[contains(@class, "responseHead-module-button") and contains(text(), "Войти")]')
    EMAIL = (By.NAME, 'email')
    PASSWORD = (By.NAME, 'password')
    LOGIN_SUBMIT = (By.XPATH, '//*[contains(@class, "authForm-module-button") and contains(text(), "Войти")]')


class BasePageLocators:
    BUTTON_MENU = (By.XPATH, '//*[contains(@class, "center-module-buttonsWrap")]')
    CAMPAIGNS = (By.XPATH, '//*[contains(@class, "center-module") and contains(@href, "/dashboard")]')
    AUDIENCE = (By.XPATH, '//*[contains(@class, "center-module") and contains(@href, "/segments")]')


class MainPageLocators(BasePageLocators):
    CREATE_CAMPAIGN = (By.XPATH, '//a[@href = "/campaign/new"]')
    CREATE_NEW_CAMPAIGN = (
        By.XPATH, '//div[contains(@class, "button-module-textWrapper") and contains(text(), "Создать кампанию")]'
    )
    INSTRUCTION = (By.XPATH, '//div[contains(@class,"instruction-module") and contains(text(), "С чего начать")]')
    CREATED_CAMPAIGN = (By.XPATH, '//a[contains(@class, "nameCell-module-campaignName") and @title="{}"]')
    SEGMENT_PAGE = (By.XPATH, '//a[@href = "/segments"]')


class CampaignPageLocators(MainPageLocators):
    CAMPAIGN_TARGET = (By.XPATH, '//div[contains(@class, "column-list-item {}")]')
    INSERT_URL = (By.XPATH, '//input[@data-gtm-id="ad_url_text"]')
    CAMPAIGN_NAME = (By.XPATH, '//div[contains(@class, "base-settings__campaign-name-wrap")]//input')
    AD_FORMAT_BANNER = (By.XPATH, '//span[contains(text(), "Баннер")]')
    UPLOAD_IMAGE_BUTTON = (By.XPATH, '//div[contains(@class, "roles-module-buttonWrap")]/'
                                     'div[contains(@class, "upload-module-wrapper")]//input')
    SAVE_PHOTO = (By.XPATH, '//input[@class="image-cropper__save js-save"]')
    SUBMIT_LOCATOR = (By.XPATH, '//button[@data-class-name="Submit"]/div[contains(text(), "Создать кампанию")]')


class SegmentPageLocators(BasePageLocators):
    CREATE_SEGMENT = (By.XPATH, '//a[@href ="/segments/segments_list/new/"]')
    COUNT_SEGMENTS = (By.XPATH, '//a[@href="/segments/segments_list"]/span[contains(@class, "item-count")]')
    SEGMENT_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and contains(@class, "adding-segments-source")]')
    ADD_SEGMENT = (By.XPATH, '//div[@class="button__text" and contains(text(), "Добавить сегмент")]')

    SEGMENT_NAME = (By.XPATH, '//input[@maxlength="60" and contains(@class,"input__inp")]')
    CREATE_NEW_SEGMENT = (By.XPATH, '//button[@data-class-name="Submit"]')
    SEGMENT_LIST = (By.XPATH, '//a[contains(@href, "/segments/segments_list/") and @title="{}"]')
    DELETE_SEGMENT = (By.XPATH, '//div[contains(@daa-test, "remove") and @data-row-id="{}"]')
    SUBMIT_DELETION = (By.XPATH, '//div[@class="button__text" and contains(text(), "Удалить")]')
