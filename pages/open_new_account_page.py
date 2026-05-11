from playwright.sync_api import Page

from pages.basepage import BasePage


class OpenNewAccountPage(BasePage):

    def __init__(self, page:Page):
        self.page = page

        self.page = page.select_option("select#type")
        self.page = page.select_option("select#fromAccountId")

    def select_account_type(self, account_type : str) -> None:
        """Select account type."""


