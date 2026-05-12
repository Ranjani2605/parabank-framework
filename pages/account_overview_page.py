import logging
import re
from decimal import Decimal

from playwright.sync_api import Page, expect

from pages.basepage import BasePage

logger = logging.getLogger("parabank")


class AccountOverviewPage(BasePage):
    """Page object for the ParaBank Accounts Overview page."""

    overview_panel = "#showOverview"
    page_heading = "#showOverview h1.title"
    account_table = "#accountTable"
    table_headers = "#accountTable thead th"
    account_rows = "#accountTable tbody tr:has(td a[href*='activity.htm?id='])"
    account_links = "#accountTable tbody tr td:first-child a[href*='activity.htm?id=']"
    account_balances = "#accountTable tbody tr:has(td a[href*='activity.htm?id=']) td:nth-child(2)"
    available_amounts = "#accountTable tbody tr:has(td a[href*='activity.htm?id=']) td:nth-child(3)"
    total_row = "#accountTable tbody tr:has-text('Total')"
    total_balance = "#accountTable tbody tr:has-text('Total') td:nth-child(2)"
    balance_note = "#accountTable tfoot td"

    currency_pattern = re.compile(r"^-?\$\d+(?:,\d{3})*(?:\.\d{2})$")

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def wait_for_page_to_load(self) -> None:
        """Wait until the account overview table is visible and populated."""
        logger.info("Waiting for Accounts Overview page")
        expect(self.page.locator(self.overview_panel)).to_be_visible()
        expect(self.page.locator(self.account_table)).to_be_visible()
        self.page.wait_for_function(
            "document.querySelectorAll('#accountTable tbody tr td a[href*=activity]').length > 0"
        )

    def assert_accounts_overview_displayed(self) -> None:
        """Validate the page title, table, account rows, and total row."""
        self.wait_for_page_to_load()
        expect(self.page.locator(self.page_heading)).to_have_text("Accounts Overview")
        expect(self.page.locator(self.account_table)).to_be_visible()
        expect(self.page.locator(self.account_links).first).to_be_enabled()
        expect(self.page.locator(self.total_row)).to_be_visible()

    def assert_navigation_url(self) -> None:
        """Validate browser navigation to the Accounts Overview page."""
        expect(self.page).to_have_url(re.compile(r".*/overview\.htm$"))

    def assert_table_headers(self) -> None:
        """Validate account table column headers."""
        expect(self.page.locator(self.table_headers)).to_have_text(
            ["Account", "Balance*", "Available Amount"]
        )

    def assert_balance_note_displayed(self) -> None:
        """Validate the balance footnote text."""
        expect(self.page.locator(self.balance_note)).to_have_text(
            "*Balance includes deposits that may be subject to holds"
        )

    def get_total_accounts_count(self) -> int:
        """Return the number of account rows, excluding the Total row."""
        return self.page.locator(self.account_links).count()

    def get_account_number_by_index(self, index: int) -> str:
        """Return an account number by zero-based index."""
        return self.page.locator(self.account_links).nth(index).inner_text().strip()

    def get_account_balance_by_index(self, index: int) -> str:
        """Return the balance for an account by zero-based index."""
        return self.page.locator(self.account_balances).nth(index).inner_text().strip()

    def get_available_amount_by_index(self, index: int) -> str:
        """Return the available amount for an account by zero-based index."""
        return self.page.locator(self.available_amounts).nth(index).inner_text().strip()

    def get_total_balance(self) -> str:
        """Return the total balance displayed in the account table."""
        return self.page.locator(self.total_balance).inner_text().strip()

    def get_account_overview_rows(self) -> list[dict[str, str]]:
        """Return account overview table data as structured rows."""
        account_count = self.get_total_accounts_count()
        rows = []

        for index in range(account_count):
            balance = self.get_account_balance_by_index(index)
            available_amount = self.get_available_amount_by_index(index)
            rows.append(
                {
                    "account_number": self.get_account_number_by_index(index),
                    "balance": balance,
                    "available_amount": available_amount,
                    "status": self.get_account_status(balance, available_amount),
                }
            )

        return rows

    def get_account_summary(self) -> dict[str, str | int]:
        """Return summary details calculated from the account table."""
        rows = self.get_account_overview_rows()
        negative_balance_count = sum(
            1 for row in rows if self.parse_currency(row["balance"]) < 0
        )
        zero_balance_count = sum(
            1 for row in rows if self.parse_currency(row["balance"]) == 0
        )

        return {
            "Total Accounts": len(rows),
            "Displayed Total Balance": self.get_total_balance(),
            "Calculated Total Balance": self.format_currency(
                sum(self.parse_currency(row["balance"]) for row in rows)
            ),
            "Negative Balance Accounts": negative_balance_count,
            "Zero Balance Accounts": zero_balance_count,
        }

    def open_account_by_index(self, index: int) -> str:
        """Open an account activity page and return the selected account id."""
        account_link = self.page.locator(self.account_links).nth(index)
        account_id = account_link.inner_text().strip()
        logger.info("Opening account activity for account: %s", account_id)
        account_link.click()
        return account_id

    def assert_account_rows_are_valid(self) -> None:
        """Validate account ids, links, balances, and available amounts."""
        account_count = self.get_total_accounts_count()
        assert account_count > 0, "Expected at least one account row"

        for index in range(account_count):
            account_id = self.get_account_number_by_index(index)
            balance = self.get_account_balance_by_index(index)
            available_amount = self.get_available_amount_by_index(index)
            account_link = self.page.locator(self.account_links).nth(index)

            assert account_id.isdigit(), f"Account id should be numeric: {account_id}"
            expect(account_link).to_have_attribute("href", re.compile(rf"activity\.htm\?id={account_id}$"))
            assert self.currency_pattern.match(balance), f"Invalid balance format: {balance}"
            assert self.currency_pattern.match(
                available_amount
            ), f"Invalid available amount format: {available_amount}"

    def assert_total_balance_format(self) -> None:
        """Validate the total balance currency format."""
        total_balance = self.get_total_balance()
        assert self.currency_pattern.match(
            total_balance
        ), f"Invalid total balance format: {total_balance}"

    def assert_total_balance_matches_account_rows(self) -> None:
        """Validate displayed total balance against calculated row balances."""
        calculated_total = sum(
            self.parse_currency(row["balance"])
            for row in self.get_account_overview_rows()
        )
        displayed_total = self.parse_currency(self.get_total_balance())

        assert displayed_total == calculated_total, (
            f"Displayed total {displayed_total} does not match "
            f"calculated total {calculated_total}"
        )

    @staticmethod
    def parse_currency(amount: str) -> Decimal:
        """Convert a UI currency value such as -$100.00 to Decimal."""
        normalized_amount = amount.replace("$", "").replace(",", "").strip()
        return Decimal(normalized_amount)

    @staticmethod
    def format_currency(amount: Decimal) -> str:
        """Format a Decimal amount using the same style as the UI table."""
        sign = "-" if amount < 0 else ""
        return f"{sign}${abs(amount):.2f}"

    @classmethod
    def get_account_status(cls, balance: str, available_amount: str) -> str:
        """Return a readable status for exported account data."""
        parsed_balance = cls.parse_currency(balance)
        parsed_available_amount = cls.parse_currency(available_amount)

        if parsed_balance < 0:
            return "Negative Balance"

        if parsed_balance == 0 and parsed_available_amount == 0:
            return "Zero Balance"

        return "Active"
