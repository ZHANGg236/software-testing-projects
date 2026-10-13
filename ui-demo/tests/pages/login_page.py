from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-testid="login-button"]')
    LOGIN_MODAL = (By.CSS_SELECTOR, '[data-testid="login-modal"]')
    USERNAME_INPUT = (By.CSS_SELECTOR, '[data-testid="username-input"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="password-input"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[data-testid="submit-login"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-testid="login-error"]')
    USER_NAME = (By.CSS_SELECTOR, '[data-testid="user-name"]')

    def open_login(self):
        self.click(self.LOGIN_BUTTON)
        self.find(self.LOGIN_MODAL)
        return self

    def login(self, username: str, password: str):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)
        return self

    def login_as_standard_user(self):
        return self.open_login().login("student", "123456")

    def error_message(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)

    def current_user(self) -> str:
        return self.text_of(self.USER_NAME)

    def is_logged_in(self) -> bool:
        return self.is_visible(self.USER_NAME)
