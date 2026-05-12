import re

from playwright.sync_api import Page, expect

from pages.basepage import BasePage


class TransferFundsPage(BasePage):
    """Page object for the ParaBank Transfer Funds page."""

    form_container = "#showForm"
    page_heading = "#showForm h1.title"
    amount_input = "#amount"
    from_account_dropdown = "#fromAccountId"
    to_account_dropdown = "#toAccountId"
    transfer_button = "input[type='submit'][value='Transfer']"
    visible_error_message = "#showForm p.error:visible"

    result_container = "#showResult"
    result_heading = "#showResult h1.title"
    result_message = "#showResult p"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def wait_for_page_to_load(self) -> None:
        """Wait until the transfer form is ready for interaction."""
        expect(self.page.locator(self.form_container)).to_be_visible()
        expect(self.page.locator(self.page_heading)).to_have_text("Transfer Funds")
        expect(self.page.locator(self.amount_input)).to_be_visible()
        expect(self.page.locator(self.transfer_button)).to_be_enabled()

    def assert_transfer_page_displayed(self) -> None:
        """Validate that the main transfer controls are available."""
        self.wait_for_page_to_load()
        expect(self.page.locator(self.from_account_dropdown)).to_be_visible()
        expect(self.page.locator(self.to_account_dropdown)).to_be_visible()

    def enter_amount(self, amount: str) -> None:
        """Enter the transfer amount."""
        self.fill(self.amount_input, amount)

    def select_from_account(self, account_id: str) -> None:
        """Select the source account."""
        self.select_dropdown(self.from_account_dropdown, account_id)

    def select_to_account(self, account_id: str) -> None:
        """Select the destination account."""
        self.select_dropdown(self.to_account_dropdown, account_id)

    def get_account_ids(self) -> list[str]:
        """Return account ids from the source account dropdown."""
        options = self.page.locator(f"{self.from_account_dropdown} option")
        return [option.strip() for option in options.all_inner_texts() if option.strip()]

    def get_two_different_account_ids(self) -> tuple[str, str]:
        """Return two different accounts for a valid transfer scenario."""
        account_ids = self.get_account_ids()

        if len(account_ids) < 2:
            raise AssertionError("At least two accounts are required to transfer funds")

        return account_ids[0], account_ids[1]

    def click_transfer(self) -> None:
        """Submit the transfer form."""
        self.click(self.transfer_button)

    def transfer_funds(
        self, amount: str, from_account_id: str, to_account_id: str
    ) -> None:
        """Fill the form and submit a transfer."""
        self.enter_amount(amount)
        self.select_from_account(from_account_id)
        self.select_to_account(to_account_id)
        self.click_transfer()

    def assert_transfer_completed(self) -> None:
        """Validate a successful transfer result."""
        expect(self.page.locator(self.result_container)).to_be_visible()
        expect(self.page.locator(self.result_heading)).to_have_text("Transfer Complete!")
        expect(self.page.locator(self.result_message)).to_contain_text(
            "has been transferred"
        )
        expect(self.page).to_have_url(re.compile(r".*/transfer\.htm$"))

    def assert_amount_required_error_displayed(self) -> None:
        """Validate the empty-amount validation message."""
        expect(self.page.locator(self.visible_error_message)).to_have_text(
            "The amount cannot be empty."
        )
