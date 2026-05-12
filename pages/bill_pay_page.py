import re

from playwright.sync_api import Page, expect

from pages.basepage import BasePage


class BillPayPage(BasePage):
    """Page object for the ParaBank Bill Payment Service page."""

    form_container = "#billpayForm"
    result_container = "#billpayResult"
    error_container = "#billpayError"

    page_heading = "#billpayForm h1.title"
    result_heading = "#billpayResult h1.title"
    error_heading = "#billpayError h1.title"

    payee_name_input = "[name='payee.name']"
    address_input = "[name='payee.address.street']"
    city_input = "[name='payee.address.city']"
    state_input = "[name='payee.address.state']"
    zip_code_input = "[name='payee.address.zipCode']"
    phone_number_input = "[name='payee.phoneNumber']"
    account_number_input = "[name='payee.accountNumber']"
    verify_account_input = "[name='verifyAccount']"
    amount_input = "[name='amount']"
    from_account_dropdown = "[name='fromAccountId']"
    send_payment_button = "input[type='button'][value='Send Payment']"

    payee_name_result = "#billpayResult #payeeName"
    amount_result = "#billpayResult #amount"
    from_account_result = "#billpayResult #fromAccountId"

    payee_name_required_error = "#validationModel-name"
    amount_required_error = "#validationModel-amount-empty"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def wait_for_page_to_load(self) -> None:
        """Wait until the bill payment form is ready."""
        expect(self.page.locator(self.form_container)).to_be_visible()
        expect(self.page.locator(self.page_heading)).to_have_text("Bill Payment Service")
        expect(self.page.locator(self.payee_name_input)).to_be_visible()
        expect(self.page.locator(self.send_payment_button)).to_be_enabled()

    def assert_bill_pay_page_displayed(self) -> None:
        """Validate the page heading and main controls."""
        self.wait_for_page_to_load()
        expect(self.page.locator(self.from_account_dropdown)).to_be_visible()
        expect(self.page).to_have_url(re.compile(r".*/billpay\.htm$"))

    def fill_payee_name(self, value: str) -> None:
        self.fill(self.payee_name_input, value)

    def fill_address(self, value: str) -> None:
        self.fill(self.address_input, value)

    def fill_city(self, value: str) -> None:
        self.fill(self.city_input, value)

    def fill_state(self, value: str) -> None:
        self.fill(self.state_input, value)

    def fill_zip_code(self, value: str) -> None:
        self.fill(self.zip_code_input, value)

    def fill_phone_number(self, value: str) -> None:
        self.fill(self.phone_number_input, value)

    def fill_account_number(self, value: str) -> None:
        self.fill(self.account_number_input, value)

    def fill_verify_account(self, value: str) -> None:
        self.fill(self.verify_account_input, value)

    def fill_amount(self, value: str) -> None:
        self.fill(self.amount_input, value)

    def select_from_account(self, account_id: str) -> None:
        self.select_dropdown(self.from_account_dropdown, account_id)

    def get_from_account_ids(self) -> list[str]:
        """Return available source account ids."""
        options = self.page.locator(f"{self.from_account_dropdown} option")
        return [option.strip() for option in options.all_inner_texts() if option.strip()]

    def fill_bill_payment_form(
        self,
        payee_name: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        phone_number: str,
        account_number: str,
        amount: str,
        from_account_id: str,
    ) -> None:
        """Fill the bill payment form with valid data."""
        self.fill_payee_name(payee_name)
        self.fill_address(address)
        self.fill_city(city)
        self.fill_state(state)
        self.fill_zip_code(zip_code)
        self.fill_phone_number(phone_number)
        self.fill_account_number(account_number)
        self.fill_verify_account(account_number)
        self.fill_amount(amount)
        self.select_from_account(from_account_id)

    def click_send_payment(self) -> None:
        """Submit the bill payment form."""
        self.click(self.send_payment_button)

    def submit_bill_payment(
        self,
        payee_name: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        phone_number: str,
        account_number: str,
        amount: str,
        from_account_id: str,
    ) -> None:
        """Fill and submit a bill payment."""
        self.fill_bill_payment_form(
            payee_name=payee_name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone_number=phone_number,
            account_number=account_number,
            amount=amount,
            from_account_id=from_account_id,
        )
        self.click_send_payment()

    def assert_bill_payment_completed(
        self, payee_name: str, amount: str, from_account_id: str
    ) -> None:
        """Validate a successful bill payment result."""
        expect(self.page.locator(self.result_container)).to_be_visible()
        expect(self.page.locator(self.result_heading)).to_have_text(
            "Bill Payment Complete"
        )
        expect(self.page.locator(self.payee_name_result)).to_have_text(payee_name)
        expect(self.page.locator(self.amount_result)).to_have_text(f"${float(amount):.2f}")
        expect(self.page.locator(self.from_account_result)).to_have_text(
            from_account_id
        )

    def assert_bill_payment_error_displayed(self) -> None:
        """Validate server-side error message."""
        expect(self.page.locator(self.error_container)).to_be_visible()
        expect(self.page.locator(self.error_heading)).to_have_text("Error!")
        expect(self.page.locator(f"{self.error_container} p.error")).to_have_text(
            "An internal error has occurred and has been logged."
        )

    def assert_required_validation_messages_displayed(self) -> None:
        """Validate basic client-side required field messages."""
        expect(self.page.locator(self.payee_name_required_error)).to_be_visible()
        expect(self.page.locator(self.payee_name_required_error)).to_have_text(
            "Payee name is required."
        )
        expect(self.page.locator(self.amount_required_error)).to_be_visible()
        expect(self.page.locator(self.amount_required_error)).to_have_text(
            "The amount cannot be empty."
        )
