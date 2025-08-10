from playwright.sync_api import Page
from pages.base_page import BasePage
from config.settings import ui_settings, credentials

class LoginPage(BasePage):
    """Login page object for SauceDemo."""

    def __init__(self, page: Page):
        super().__init__(page)
        
    @property
    def username_input(self):
        return self.locator('#user-name')

    @property
    def password_input(self):
        return self.locator('#password')

    @property
    def login_button(self):
        return self.locator('#login-button')

    @property
    def error_message(self):
        return self.locator('[data-test="error"]')

    def open(self):
        self.goto(ui_settings.base_url)
        return self

    def login(self, username: str | None = None, password: str | None = None):
        username = username or credentials.username
        password = password or credentials.password
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        return self
