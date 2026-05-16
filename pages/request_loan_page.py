import logging
import re

from playwright.sync_api import Page, expect

from pages.basepage import BasePage

logger = logging.getLogger("parabank")


class RequestLoanPage(BasePage):
    """Page object for the ParaBank Request Loan page."""

    form_container = "#requestLoanForm"
    page_heading = "#requestLoanForm h1.title"
    loan_amount_input = "#amount"
    down_payment_input = "#downPayment"
    from_account_dropdown = "#fromAccountId"
    apply_now_button = "input.button[value='Apply Now']"

    result_container = "#requestLoanResult"
    result_heading = "#requestLoanResult h1.title"
    loan_provider_name = "#loanProviderName"
    response_date = "#responseDate"
    loan_status = "#loanStatus"

    approved_container = "#loanRequestApproved"
    approved_message = "#loanRequestApproved p"
    new_account_link = "#newAccountId"

    denied_container = "#loanRequestDenied"
    denied_message = "#loanRequestDenied p"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def wait_for_page_to_load(self) -> None:
        """Wait until the request loan form is ready for interaction."""
        logger.info("Waiting for Request Loan page")
        expect(self.page.locator(self.form_container)).to_be_visible()
        expect(self.page.locator(self.page_heading)).to_have_text("Apply for a Loan")
        expect(self.page.locator(self.loan_amount_input)).to_be_visible()
        expect(self.page.locator(self.down_payment_input)).to_be_visible()
        self.page.wait_for_function(
            "document.querySelectorAll('#fromAccountId option').length > 0"
        )
        expect(self.page.locator(self.apply_now_button)).to_be_enabled()

    def assert_request_loan_page_displayed(self) -> None:
        """Validate the page heading, controls, and navigation."""
        self.wait_for_page_to_load()
        expect(self.page.locator(self.from_account_dropdown)).to_be_visible()
        expect(self.page).to_have_url(re.compile(r".*/requestloan\.htm$"))

    def get_from_account_ids(self) -> list[str]:
        """Return the available funding account ids."""
        options = self.page.locator(f"{self.from_account_dropdown} option")
        return [option.strip() for option in options.all_inner_texts() if option.strip()]

    def enter_loan_amount(self, amount: str) -> None:
        """Enter the requested loan amount."""
        self.fill(self.loan_amount_input, amount)

    def enter_down_payment(self, amount: str) -> None:
        """Enter the down payment amount."""
        self.fill(self.down_payment_input, amount)

    def select_from_account(self, account_id: str) -> None:
        """Select the funding account."""
        self.select_dropdown(self.from_account_dropdown, account_id)

    def click_apply_now(self) -> None:
        """Submit the loan request form."""
        self.click(self.apply_now_button)

    def submit_loan_request(
        self, loan_amount: str, down_payment: str, from_account_id: str
    ) -> None:
        """Fill and submit a loan request."""
        logger.info(
            "Submitting loan request with amount %s and down payment %s",
            loan_amount,
            down_payment,
        )
        self.enter_loan_amount(loan_amount)
        self.enter_down_payment(down_payment)
        self.select_from_account(from_account_id)
        self.click_apply_now()

    def assert_loan_request_processed(
        self, expected_provider: str, expected_status: str
    ) -> None:
        """Validate the common loan result details."""
        expect(self.page.locator(self.result_container)).to_be_visible()
        expect(self.page.locator(self.result_heading)).to_have_text(
            "Loan Request Processed"
        )
        expect(self.page.locator(self.loan_provider_name)).to_have_text(
            expected_provider
        )
        expect(self.page.locator(self.loan_status)).to_have_text(expected_status)
        expect(self.page.locator(self.response_date)).to_have_text(
            re.compile(r"\d{2}-\d{2}-\d{4}")
        )

    def assert_loan_approved(self) -> None:
        """Validate the approved loan state and new account details."""
        expect(self.page.locator(self.approved_container)).to_be_visible()
        expect(self.page.locator(self.approved_container)).to_contain_text(
            "Congratulations, your loan has been approved."
        )
        expect(self.page.locator(self.new_account_link)).to_be_visible()
        expect(self.page.locator(self.new_account_link)).to_have_text(
            re.compile(r"\d+")
        )
        expect(self.page.locator(self.new_account_link)).to_have_attribute(
            "href", re.compile(r"activity\.htm\?id=\d+")
        )

    def assert_loan_denied(self, expected_message: str) -> None:
        """Validate the denied loan state and denial message."""
        expect(self.page.locator(self.denied_container)).to_be_visible()
        expect(self.page.locator(self.denied_message)).to_have_text(expected_message)
