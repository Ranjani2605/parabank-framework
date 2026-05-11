import logging

from playwright.sync_api import Page

from pages.basepage import BasePage

logger = logging.getLogger(__name__)

class AccountOverviewPage(BasePage):

    """class representing account overview page."""

    page_title = "h1.title"
    account_table = "#accountTable"
    first_account_link = "#accountTable tbody tr:first-child td a"
    first_account_balance ="#accountTable tbody tr:first-child td:nth-child(2)"

    account_rows = "#accountTable tbody tr"
    account_numbers = (
        "#accountTable tbody tr td:nth-child(1) a"
    )
    account_balances = (
        "#accountTable tbody tr td:nth-child(2)"
    )
    available_amounts = (
        "#accountTable tbody tr td:nth-child(3)"
    )

    total_balance = (
        "#accountTable tfoot tr td:nth-child(2)"
    )

    def __init__(self, page:Page) -> None:
        super().__init__(page)


    def wait_for_page_to_load(self) -> None:
        """wait for page to load."""
        logger.info("Waiting for Account overview page.")
        self.wait_for_element(self.account_table)

    def get_page_heading(self) -> str:
        """Return page heading."""
        return self.get_text(self.page_title)

    def get_total_accounts_count(self) -> int:
        """Return first account balance."""
        return self.get_count(self.account_numbers)

    def get_account_number_by_index(self, index: int) -> str:
        """Return account number by index."""
        self.wait_for_page_to_load()
        accounts = self.locator(self.account_numbers)
        return self.account .nth(index).inner_text().strip()

    def get_account_balance_by_index(self, index: int) -> str:
        """Return account balance."""
        self.wait_for_page_to_load()
        account = self.account_numbers.nth(index)
        return account.inner_text().strip()

    def get_total_balance(self) -> str:
        """Return total balance."""
        self.wait_for_page_to_load()
        return self.get_text(self.total_balance)

    def open_first_account(self) -> None:
        """Open first account page."""
        self.wait_for_page_to_load()
        logger.info("Opening first account.")
        self.account_numbers.first.click()







