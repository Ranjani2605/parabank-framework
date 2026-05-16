import pytest
from playwright.sync_api import Playwright

from pages.account_overview_page import AccountOverviewPage
from pages.account_services_link import AccountServiceLink
from pages.bill_pay_page import BillPayPage
from pages.find_transactions_page import FindTransactionsPage
from pages.login_page import LoginPage
from pages.open_new_account_page import OpenNewAccountPage
from pages.request_loan_page import RequestLoanPage
from pages.transfer_funds_page import TransferFundsPage
from utils.config_reader import ConfigReader


@pytest.fixture(scope="session")
def base_url():
    """Return the ParaBank base URL from environment configuration."""
    return ConfigReader.BASE_URL


@pytest.fixture(scope="session")
def browser_instance(playwright: Playwright):
    """Launch one browser for the test session."""
    browser = playwright.chromium.launch(headless=ConfigReader.HEADLESS)
    yield browser
    browser.close()


@pytest.fixture()
def browser_context(browser_instance):
    """Create a fresh browser context for each test to avoid state leakage."""
    context = browser_instance.new_context(base_url=ConfigReader.BASE_URL)
    context.set_default_timeout(ConfigReader.TIMEOUT)
    yield context
    context.close()


@pytest.fixture()
def page(browser_context, base_url):
    """Open the application home page in a fresh tab for each test."""
    page = browser_context.new_page()
    page.goto(base_url, wait_until="domcontentloaded")
    yield page
    page.close()


@pytest.fixture()
def logged_in_page(page):
    """Return a browser page with a logged-in ParaBank user."""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_with_default_user()
    login_page.assert_login_success()
    yield page


@pytest.fixture()
def account_services(logged_in_page):
    """Return the account services navigation component after login."""
    return AccountServiceLink(logged_in_page)


@pytest.fixture()
def account_overview_page(account_services) -> AccountOverviewPage:
    """Return the Accounts Overview page after login and navigation."""
    overview_page = account_services.click_account_overview()
    overview_page.wait_for_page_to_load()
    return overview_page


@pytest.fixture()
def open_new_account_page(account_services) -> OpenNewAccountPage:
    """Return the Open New Account page after login and navigation."""
    open_account_page = account_services.click_open_new_account()
    open_account_page.wait_for_page_to_load()
    return open_account_page


@pytest.fixture()
def transfer_funds_page(account_services) -> TransferFundsPage:
    """Return the Transfer Funds page after login and navigation."""
    transfer_page = account_services.click_transfer_account()
    transfer_page.wait_for_page_to_load()
    return transfer_page


@pytest.fixture()
def bill_pay_page(account_services) -> BillPayPage:
    """Return the Bill Pay page after login and navigation."""
    bill_pay = account_services.click_bill_pay()
    bill_pay.wait_for_page_to_load()
    return bill_pay


@pytest.fixture()
def find_transactions_page(account_services) -> FindTransactionsPage:
    """Return the Find Transactions page after login and navigation."""
    find_transactions = account_services.click_find_transaction()
    find_transactions.wait_for_page_to_load()
    return find_transactions


@pytest.fixture()
def request_loan_page(account_services) -> RequestLoanPage:
    """Return the Request Loan page after login and navigation."""
    request_loan = account_services.click_request_loan()
    request_loan.wait_for_page_to_load()
    return request_loan


