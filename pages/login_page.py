import logging
import re
from typing import Optional

import allure
from playwright.sync_api import Page, expect
from pytest_base_url.plugin import base_url
from utils.config_reader import ConfigReader

from pages.basepage import BasePage

logger = logging.getLogger("parabank_")

class LoginPage(BasePage):

    #----------Locators----------------------
    username_input = "input[name='username']"
    password_input = "input[name='password']"
    login_button = "input[value='Log In']"
    forget_link = "a[href='lookup.htm']"
    register_link = "a[href='register.htm']"
    welcome_text = ".smallText"
    error_message = ".error"

    def __init__(self, page:Page):
        self.page = page

    @allure.step("Open login page")
    def open(self):
        self.goto(ConfigReader.BASE_URL)
        self.is_visible(self.username_input)

    @allure.step("Login with username: {username}")
    def login(self, username : str, password : str):
        logger.info(f"Attempting login for user: {username}")
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

        expect(self.page).to_have_url(re.compile(r".*/overview\.htm$"))

    @allure.step("Login using environment credentials")
    def login_with_default_user(self):
        logger.info("Logging in using default credentials")
        self.login(ConfigReader.USERNAME, ConfigReader.PASSWORD)

    @allure.step("Click forgot login link")
    def click_forgot_button(self):
        logger.info("Opening forgot login page")
        self.click(self.forget_link)

    @allure.step("Click register link")
    def click_register_link(self):
        logger.info("Opening registration page")
        self.click(self.register_link)

    @allure.step("Assert successful login")
    def assert_login_success(self):
        logger.info("Validating overview page URL")
        expect(self.page).to_have_url(re.compile(r".*/overview\.htm$"))

    @allure.step("Verify login successful")
    def is_login_in(self) -> bool:
        logger.info("Checking login success status")
        return self.page.locator(self.welcome_text).is_visible()

    @allure.step("Get login error message")
    def get_error_message(self) -> str:
        logger.info("Fetching login error message")
        return self.get_text(self.error_message)

