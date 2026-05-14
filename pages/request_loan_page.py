from playwright.sync_api import Page, expect

from pages.basepage import BasePage

import logging

logger = logging.getLogger(__name__)

class RequestLoanPage(BasePage):

    loan_form = "#requestLoanForm"
    header_loan_form_title = "#requestLoanForm h1.title"
    loan_amount_input = "#amount"
    down_payment_input = "#downPayment"
    from_account_dropdown = "#fromAccountId"
    apply_now_button = "input.button[value='Apply Now']"


    # Main section
    loan_result = "#requestLoanResult"

    # Header
    loan_result_title = "h1.title"

    #Loan details
    loan_provider_name = "#loanProviderName"
    response_date = "#responseDate"
    loan_status = "#loanStatus"

    #Approval section
    loan_approved_section = "#loanRequestApproved"
    approval_message = "#loanRequestApproved p"
    new_account_id = "#newAccountId"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page = page

    # Loan form validation methods

    def validate_loan_form_displayed(self) -> None:
        """validate loan application form is displayed"""

        logger.info("Validating Loan Application form")
        expect(self.page.is_visible(self.loan_form))
        expect(self.header_loan_form_title).to_have_text("Apply for a Loan")
        logger.info("Loan Application form validated successfully")

    # Loan form action methods

    def enter_loan_amount(self, amount: str) -> None:
        """Enter loan amount input"""
        logger.info(f"Entering loan amount: {amount}")
        self.page.fill(self.loan_amount_input, amount)

    def enter_down_payment(self, amount: str) -> None:
        """Enter down payment input"""
        logger.info(f"Selecting account number: {amount}")
        self.page.fill(self.down_payment_input, amount)

    def select_from_account(self, account_number: str) -> None:
        """Select account from dropdown"""
        logger.info(f"Selecting account number: {account_number}")
        self.page.select_option(self. from_account_dropdown)

    def click_apply_now(self) -> None:
        logger.info(f"Clicking apply now button")
        self.click(self.apply_now_button)

    def apply_for_loan(self, loan_amount, down_payment, account_number) -> None:
        """Complete loan application process"""
        logger.info(f"Starting loan application process")
        self.enter_loan_amount(loan_amount)
        self.enter_down_payment(down_payment)
        self.select_from_account(account_number)
        self.click_apply_now()
        logger.info("Loan application submitted successfully")

    # Loan result validation methods

    def validate_loan_request_processed(self) -> None:
        """Validate Loan request processed section"""
        logger.info("Validating loan request processed page")
        except(self.page.is_visible(self.loan_result))
        expect(self.loan_result_title).to_have_text("Loan Request Processed")
        logger.info("Loan request processed validated successfully")

    def validate_loan_provider(self, expected_provider: str) -> None:
        """Validating loan provider section"""
        logger.info("Validating loan provider section")
        expect(self.loan_provider_name).to_have_text(expected_provider)

    def validate_loan_status(self, expected_status: str) -> None:
        """Validate loan status section"""
        logger.info("Validating loan status section")
        expect(self.loan_status).to_have_text(expected_status)
        logger.info(f"Loan status validated successfully: {expected_status}")


    def validate_approval_message(self) -> None:
        """Validate approval message section"""
        logger.info("Validating approval message section")
        pop_message = self.get_text(self.approval_message)
        except(pop_message.to_contain_text("Congratulations, your loan has been approved"))
        logger.info("Approval message validated successfully")

    def validate_new_account_created(self) -> None:
        """Validate new account is created"""
        logger.info("validate newly created account")
        expect(self.page.is_visible(self.new_account_id))
        account_number = self.get_text(self.new_account_id)
        assert account_number is not None, "Account number is None"
        assert account_number.strip() != "", "Account number is empty"
        assert (account_number.strip().isdigit()), "Account number is not numeric"
        logger.info(f"New account created validated successfully: {account_number}")


    def validate_new_account_link(self) -> None:
        """Validate new account hyperlink"""
        logger.info("Validating account hyperlink")
        href_value = (self.new_account_id).__getattribute__("href")

        assert href_value is not None
        assert "id=" in href_value

        logger.info(f"Account hyperlink validated: {href_value}")




