import logging
import re

import allure
from playwright.sync_api import Page, expect

from pages.basepage import BasePage
from utils.config_reader import ConfigReader

logger = logging.getLogger("parabank")


class LoginPage(BasePage):
    """Page object for the ParaBank login page."""

    username_input = "input[name='username']"
    password_input = "input[name='password']"
    login_button = "input[value='Log In']"
    forget_link = "a[href='lookup.htm']"
    register_link = "a[href='register.htm']"
    welcome_text = ".smallText"
    error_message = ".error"
    login_success_url = re.compile(r".*/overview\.htm$")

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Open login page")
    def open(self) -> None:
        self.goto(ConfigReader.BASE_URL)
        self.wait_for_element(self.username_input)

    @allure.step("Login with username: {username}")
    def login(self, username: str, password: str) -> None:
        logger.info("Attempting login for user: %s", username)
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        expect(self.page).to_have_url(self.login_success_url)

    @allure.step("Login using environment credentials")
    def login_with_default_user(self) -> None:
        ConfigReader.validate_login_config()
        logger.info("Logging in using default credentials")
        self.login(ConfigReader.USERNAME, ConfigReader.PASSWORD)

    @allure.step("Click forgot login link")
    def click_forgot_button(self) -> None:
        logger.info("Opening forgot login page")
        self.click(self.forget_link)

    @allure.step("Click register link")
    def click_register_link(self) -> None:
        logger.info("Opening registration page")
        self.click(self.register_link)

    @allure.step("Assert successful login")
    def assert_login_success(self) -> None:
        logger.info("Validating overview page URL")
        expect(self.page).to_have_url(self.login_success_url)

    @allure.step("Verify login successful")
    def is_logged_in(self) -> bool:
        logger.info("Checking login success status")
        return bool(self.login_success_url.search(self.page.url))

    def is_login_in(self) -> bool:
        """Backward-compatible alias for older tests."""
        return self.is_logged_in()

    @allure.step("Get login error message")
    def get_error_message(self) -> str:
        logger.info("Fetching login error message")
        return self.get_text(self.error_message)

