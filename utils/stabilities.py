import logging
import time
from typing import Any, Callable, Optional

from playwright.sync_api import Page, Locator
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


class Stability:
    """Shared waiting helpers used by page objects."""

    DEFAULT_TIMEOUT = 10000

    @staticmethod
    def safe_click(locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Stable click implementation."""
        logger.info("Performing safe click")
        locator.wait_for(state="visible", timeout=timeout)
        locator.scroll_into_view_if_needed()
        locator.click(timeout=timeout)

    @staticmethod
    def safe_fill(locator: Locator, value: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Stable input fill."""
        logger.info("Performing safe fill")
        locator.wait_for(state="visible", timeout=timeout)
        locator.clear()
        locator.fill(value, timeout=timeout)

    @staticmethod
    def retry_with_reload(
        page: Page, action: Callable[[], Any], max_retries: int = 1
    ) -> Optional[Any]:
        """Retry a failed UI action after a page reload."""
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                return action()
            except PlaywrightTimeoutError as error:
                last_error = error

                logger.warning(f"Retry attempt: {attempt + 1}")

                if attempt < max_retries:
                    page.reload(wait_until="domcontentloaded")
                    page.wait_for_timeout(1000)
                    continue

                logger.error("Action failed after retries")

        if last_error:
            raise last_error

        return None

    @staticmethod
    def wait_for_dropdown_options(
        locator: Locator, min_options: int = 1, timeout: int = 15000
    ) -> None:
        """Wait until dropdown options load."""
        logger.info("waiting for dropdown options")

        start_time = time.time()
        while time.time() - start_time < timeout / 1000:
            options = locator.locator("option").all_inner_texts()

            valid_options = [option for option in options if option.strip()]

            if len(valid_options) >= min_options:
                return

            time.sleep(0.5)

        raise PlaywrightTimeoutError("Dropdown options failed to load")

    @staticmethod
    def wait_for_page_load(page: Page) -> None:
        """Wait until the page has reached DOM content loaded."""
        logger.info("waiting for page load")
        page.wait_for_load_state("domcontentloaded")

    @staticmethod
    def wait_for_element(locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Wait until an element is visible."""
        locator.wait_for(state="visible", timeout=timeout)

