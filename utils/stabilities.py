import logging
import time
from typing import Any, Callable, Optional
from playwright.sync_api import Page, Locator
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

class Stability:

    DEFAULT_TIMEOUT = 10000

    def safe_click(locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Stable click implementation."""

        logger.info("Performing safe click")
        locator.wait_for(state="visible", timeout=timeout)

        locator.scroll_into_view_if_needed()
        locator.click(timeout=timeout)


    def safe_fill(locator: Locator, value: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Stable input fill"""
        logger.info("Performing safe fill")
        locator.wait_for(state="visible", timeout=timeout)
        locator.clear()
        locator.fill(value, timeout=timeout)

    def retry_with_reload(page: Page, action: Callable[[], Any], max_retries: int = 1) -> Optional[Any]:
        """Retry failed UI action after page rload"""
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

                else:
                    logger.error("Action failed after retries")

                raise

        if last_error:
            raise last_error

        return None


    def wait_for_dropdown_options(locator: Locator, min_options: int =1, timeout: int = 15000) -> None:
        """wait until dropdown options load"""
        logger.info("waiting for dropdown options")

        start_time = time.time()
        while time.time() - start_time < timeout / 1000:
            options = locator.locator("options").all_inner_texts()

            valid_options = [option for option in options if option.strip()]

            if len(valid_options) >= min_options:
                return
            time.sleep(0.5)

        raise PlaywrightTimeoutError("Dropdown options failed to load")

    def wait_for_page_load(page: Page) -> None:
        """wait until page load"""
        logger.info("waiting for page load")
        page.wait_for_load_state("domcontentloaded")


    def wait_for_elements(locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        """wait for visible element"""
        logger.wait_for(state="visible", timeout=timeout)







