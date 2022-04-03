from selenium.webdriver.common.by import By

LOGIN = (By.XPATH, '//*[contains(@class, "responseHead-module-button")]')

EMAIL = (By.NAME, 'email')
PASSWORD = (By.NAME, 'password')

LOGIN_SUBMIT = (By.XPATH, '//*[contains(@class, "authForm-module-button")]')

BUTTON_MENU = (By.XPATH, '//*[contains(@class, "center-module-buttonsWrap")]')

MIGRATION_BUTTON = {
    'Аудитории': (By.XPATH, '//*[contains(@class, "center-module") and contains(@href, "/segments")]'),
    'Профиль': (By.XPATH, '//*[contains(@class, "center-module") and contains(@href, "/profile")]')
}

PROFILE = (By.XPATH, '//*[contains(@class, "center-module") and contains(@href, "/profile")]')

USER_MENU = (By.XPATH, '//*[contains(@class, "right-module-rightButton")]')
USER_MENU_WRAP = (By.XPATH, '//*[contains(@class, "right-module-rightWrap")]')
SLIDING_USER_MENU = (By.XPATH, '//*[contains(@class, "rightMenu-module-visibleRightMenu")]')
LOGOUT = (By.XPATH, '//*[contains(@class, "rightMenu-module") and contains(@href, "/logout")]')

PROFILE_FULLNAME = (By.XPATH, '//div[contains(@data-name, "fio")]//input')
PROFILE_PHONE = (By.XPATH, '//div[contains(@data-name, "phone")]//input')
PROFILE_ADD_EMAIL_BUTTON = (By.XPATH, '//div[contains(@class, "clickable-button__container")]')
PROFILE_EMAIL = (By.XPATH, '//div[contains(@class, "js-additional-email profile")]//input')
PROFILE_SAVE = (By.XPATH, '//div[@class = "button__text"]')
PROFILE_EDIT_RESPONSE = (By.XPATH, '//div[contains(@cid, "view") and contains(@class, "_notification")]')
