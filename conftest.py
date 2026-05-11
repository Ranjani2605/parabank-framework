import pytest
from playwright.sync_api import Playwright
from utils.config_reader import ConfigReader


@pytest.fixture(scope="session")
def base_url():
    return ConfigReader.BASE_URL


@pytest.fixture(scope="session")
def browser_Instance(playwright: Playwright):
    browser = playwright.chromium.launch(headless=ConfigReader.HEADLESS)
    context = browser.new_context(base_url=ConfigReader.BASE_URL)
    context.set_default_timeout(ConfigReader.TIMEOUT)
    yield context
    context.close()
    browser.close()


@pytest.fixture()
def page(browser_Instance, base_url):
    page = browser_Instance.new_page()
    page.goto(base_url)
    yield page
    page.close()



