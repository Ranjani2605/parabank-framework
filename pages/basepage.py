import logging
from tkinter.tix import Select
from xml.sax.xmlreader import Locator

from playwright.sync_api import Page, expect

logger = logging.getLogger("parabank")

class BasePage:

    DEFAULT_TIMEOUT = 10000

    """Base page containing common reusable methods"""

    def init_page(self, page:Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to URL"""
        logger.info("Navigating to: %s", url)
        self.page.goto(url, timeout=self.DEFAULT_TIMEOUT)

    def click(self, locator: str) -> None:
        """click on element."""
        logger.info(f"Clicking element: {locator}")
        self.page.locator(locator).click()

    def fill(self, locator, value: str) -> None:
        """Fill input field."""
        logger.info(f"Entering value: %s", value)
        self.page.locator(locator).fill(value)

    def get_text(self, locator) -> str:
        """Get text from locator."""
        text = self.page.locator(locator).inner_text()
        logger.info("Captured text: %s", text)
        return text

    def wait_for_element(self, locator)-> None:
        """Wait for element visibility."""
        expect(locator).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def is_visible(self, locator) -> bool:
        """check whether element is visible."""
        return self.page.locator(locator).is_visible()

    def get_page_title(self) -> str:
        """Return page title."""
        return self.page.title()

    def get_count(self, selector: str) -> int:
        """Return locator count."""
        return self.page.locator(selector).count()

    def get_select(self, value: str) -> Select:
        return self.page.locator(value).select()



