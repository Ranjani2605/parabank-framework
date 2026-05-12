import logging
import re

from playwright.sync_api import Page, expect

from pages.basepage import BasePage

logger = logging.getLogger("parabank")


class OpenNewAccountPage(BasePage):
    """Page object for the ParaBank Open New Account page."""

    page_heading = "#openAccountForm h1.title"
    form = "#openAccountForm"
    result_panel = "#openAccountResult"
    error_panel = "#openAccountError"
    error_message = "#openAccountError .error"

    account_type_dropdown = "#type"
    from_account_dropdown = "#fromAccountId"
    minimum_deposit_message = "#openAccountForm p"
    new_account_link = "#newAccountId"

    # The button has no id/name/data-testid in the HTML, so value text is the
    # most stable available selector without using XPath.
    open_account_button = "input[type='button'][value='Open New Account']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def wait_for_page_to_load(self) -> None:
        """Wait until the open account form is ready for interaction."""
        logger.info("Waiting for Open New Account page")
        expect(self.page.locator(self.form)).to_be_visible()
        expect(self.page.locator(self.account_type_dropdown)).to_be_visible()
        expect(self.page.locator(self.from_account_dropdown)).to_be_visible()
        self.page.wait_for_function(
            "document.querySelectorAll('#fromAccountId option').length > 0"
        )
        expect(self.page.locator(self.open_account_button)).to_be_enabled()

    def assert_open_account_page_displayed(self) -> None:
        """Validate that the form and main controls are visible."""
        self.wait_for_page_to_load()
        expect(self.page.locator(self.page_heading)).to_have_text("Open New Account")
        expect(self.page.locator(self.account_type_dropdown)).to_be_enabled()
        expect(self.page.locator(self.from_account_dropdown)).to_be_enabled()
        expect(self.page.locator(self.open_account_button)).to_be_visible()

    def select_account_type(self, account_type: str) -> None:
        """Select CHECKING or SAVINGS account type."""
        account_type_values = {"CHECKING": "0", "SAVINGS": "1"}
        normalized_type = account_type.upper()

        if normalized_type not in account_type_values:
            raise ValueError("Account type must be CHECKING or SAVINGS")

        self.page.locator(self.account_type_dropdown).select_option(
            value=account_type_values[normalized_type]
        )

    def select_from_account_by_value(self, account_id: str) -> None:
        """Select the source account used to fund the new account."""
        self.page.locator(self.from_account_dropdown).select_option(value=account_id)

    def get_selected_account_type(self) -> str:
        """Return the selected account type label."""
        return self.page.locator(f"{self.account_type_dropdown} option:checked").inner_text()

    def get_selected_from_account(self) -> str:
        """Return the selected source account id."""
        return self.page.locator(self.from_account_dropdown).input_value()

    def get_available_from_accounts_count(self) -> int:
        """Return the number of source accounts available in the dropdown."""
        return self.page.locator(f"{self.from_account_dropdown} option").count()

    def click_open_new_account(self) -> None:
        """Submit the Open New Account form."""
        logger.info("Submitting Open New Account form")
        self.page.locator(self.open_account_button).click()

    def open_new_account(self, account_type: str = "CHECKING") -> None:
        """Select an account type and submit the form."""
        self.select_account_type(account_type)
        self.click_open_new_account()

    def assert_account_opened_successfully(self) -> None:
        """Validate successful account creation result."""
        expect(self.page.locator(self.result_panel)).to_be_visible()
        expect(self.page.locator(f"{self.result_panel} h1.title")).to_have_text(
            "Account Opened!"
        )
        expect(self.page.locator(self.result_panel)).to_contain_text(
            "Congratulations, your account is now open."
        )
        expect(self.page.locator(self.new_account_link)).to_be_visible()
        expect(self.page.locator(self.new_account_link)).to_have_text(re.compile(r"\d+"))
        expect(self.page.locator(self.new_account_link)).to_have_attribute(
            "href", re.compile(r"activity\.htm\?id=\d+")
        )

    def assert_open_account_error_displayed(self) -> None:
        """Validate error state when account creation fails."""
        expect(self.page.locator(self.error_panel)).to_be_visible()
        expect(self.page.locator(f"{self.error_panel} h1.title")).to_have_text("Error!")
        expect(self.page.locator(self.error_message)).to_have_text(
            "An internal error has occurred and has been logged."
        )

    def assert_minimum_deposit_message_displayed(self) -> None:
        """Validate the minimum deposit instruction text."""
        expect(self.page.locator(self.form)).to_contain_text(
            "A minimum of $100.00 must be deposited into this account"
        )

    def assert_navigation_url(self) -> None:
        """Validate browser navigation to the Open New Account page."""
        expect(self.page).to_have_url(re.compile(r".*/openaccount\.htm$"))
