import logging
from playwright.sync_api import Page

from pages.account_overview_page import AccountOverviewPage
from pages.basepage import BasePage

logger = logging.getLogger("parabank_")
class AccountServiceLink(BasePage):

    open_new_account_link_locator = "a[href='openaccount.htm']"
    account_Overview_link_locator = "a[href='overview.htm']"
    transfer_link_locator = "a[href='transfer.htm']"
    bill_pay_link_locator = "a[href='billpay.htm']"
    find_transaction_link_locator = "a[href='findtrans.htm']"
    update_contact_info_locator = "a[href='updateprofile.htm']"
    request_loan_link_locator = "a[href='requestloan.htm']"
    logout_locator = "a[href='logout.htm']"

    def __init__(self, page:Page) -> None:
        super().__init__(page)


    def click_open_new_account(self):
        logger.info(f"click open new account")
        self.click(self.open_new_account_link_locator)

    def click_account_overview(self) -> AccountOverviewPage:
        logger.info(f"click account overview")
        self.click(self.account_Overview_link_locator)
        return AccountOverviewPage(self.page)

    def click_transfer_account(self):
        logger.info(f"click transfer account")
        self.click(self.transfer_link_locator)

    def click_bill_pay(self):
        logger.info(f"click bill pay")
        self.click(self.bill_pay_link_locator)

    def click_find_transaction(self):
        logger.info(f"click find transaction")
        self.click(self.find_transaction_link_locator)

    def click_update_contact_info(self):
        logger.info(f"click update contact info")
        self.click(self.update_contact_info_locator)

    def click_request_loan(self):
        logger.info(f"click request loan")
        self.click(self.request_loan_link_locator)

    def click_log_out(self):
        logger.info(f"click log out")
        self.click(self.logout_locator)