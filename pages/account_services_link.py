import logging

from playwright.sync_api import Page

from pages.account_overview_page import AccountOverviewPage
from pages.basepage import BasePage
from pages.bill_pay_page import BillPayPage
from pages.find_transactions_page import FindTransactionsPage
from pages.open_new_account_page import OpenNewAccountPage
from pages.request_loan_page import RequestLoanPage
from pages.transfer_funds_page import TransferFundsPage

logger = logging.getLogger("parabank")


class AccountServiceLink(BasePage):
    """Page object for the left-side Account Services navigation."""

    open_new_account_link = "a[href='openaccount.htm']"
    account_overview_link = "a[href='overview.htm']"
    transfer_link = "a[href='transfer.htm']"
    bill_pay_link = "a[href='billpay.htm']"
    find_transaction_link = "a[href='findtrans.htm']"
    update_contact_info_link = "a[href='updateprofile.htm']"
    request_loan_link = "a[href='requestloan.htm']"
    logout_link = "a[href='logout.htm']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def click_open_new_account(self) -> OpenNewAccountPage:
        logger.info("Click open new account")
        self.click(self.open_new_account_link)
        return OpenNewAccountPage(self.page)

    def click_account_overview(self) -> AccountOverviewPage:
        logger.info("Click account overview")
        self.click(self.account_overview_link)
        return AccountOverviewPage(self.page)

    def click_transfer_account(self) -> TransferFundsPage:
        logger.info("Click transfer account")
        self.click(self.transfer_link)
        return TransferFundsPage(self.page)

    def click_bill_pay(self) -> BillPayPage:
        logger.info("Click bill pay")
        self.click(self.bill_pay_link)
        return BillPayPage(self.page)

    def click_find_transaction(self) -> FindTransactionsPage:
        logger.info("Click find transaction")
        self.click(self.find_transaction_link)
        return FindTransactionsPage(self.page)

    def click_update_contact_info(self) -> None:
        logger.info("Click update contact info")
        self.click(self.update_contact_info_link)

    def click_request_loan(self) -> RequestLoanPage:
        logger.info("Click request loan")
        self.click(self.request_loan_link)
        return RequestLoanPage(self.page)

    def click_log_out(self) -> None:
        logger.info("Click log out")
        self.click(self.logout_link)
