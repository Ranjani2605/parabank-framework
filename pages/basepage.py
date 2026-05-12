import logging

from playwright.sync_api import Locator, Page, expect

from utils.stabilities import Stability

logger = logging.getLogger("parabank")


class BasePage:
    """Base page containing common reusable Playwright actions."""

    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        """Navigate to a URL and wait for the page to finish loading."""
        logger.info("Navigating to: %s", url)
        self.page.goto(url, wait_until="domcontentloaded")
        Stability.wait_for_page_load(self.page)

    def refresh_page(self) -> None:
        """Refresh the current page."""
        logger.info("Refreshing page")
        self.page.reload()
        Stability.wait_for_page_load(self.page)

    def get_locator(self, locator: str) -> Locator:
        """Return a Playwright locator."""
        return self.page.locator(locator)

    def locator(self, locator: str) -> Locator:
        """Short alias for creating locators."""
        return self.get_locator(locator)

    def click(self, locator: str) -> None:
        """Click an element."""
        logger.info("Clicking element: %s", locator)
        Stability.safe_click(self.get_locator(locator), timeout=self.DEFAULT_TIMEOUT)

    def fill(self, locator: str, value: str) -> None:
        """Fill an input field."""
        logger.info("Entering value into: %s", locator)
        Stability.safe_fill(
            self.get_locator(locator), value, timeout=self.DEFAULT_TIMEOUT
        )

    def get_text(self, locator: str) -> str:
        """Return visible text from an element."""
        text = self.get_locator(locator).inner_text().strip()
        logger.info("Captured text from %s: %s", locator, text)
        return text

    def wait_for_element(self, locator: str | Locator) -> None:
        """Wait for an element to be visible."""
        element = self.get_locator(locator) if isinstance(locator, str) else locator
        expect(element).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def is_visible(self, locator: str) -> bool:
        """Return whether an element is visible."""
        return self.get_locator(locator).is_visible()

    def get_page_title(self) -> str:
        """Return the browser page title."""
        return self.page.title()

    def get_count(self, selector: str) -> int:
        """Return the number of matching elements."""
        return self.get_locator(selector).count()

    def select_dropdown(self, locator: str, value: str) -> None:
        """Select a dropdown option by value."""
        logger.info("Selecting dropdown %s value: %s", locator, value)
        dropdown = self.get_locator(locator)
        Stability.wait_for_dropdown_options(dropdown, timeout=self.DEFAULT_TIMEOUT)
        expect(dropdown).to_be_enabled(timeout=self.DEFAULT_TIMEOUT)
        dropdown.select_option(value=value)
