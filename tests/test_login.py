from pages.login_page import LoginPage
from utils.config_reader import ConfigReader



def test_valid_login(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(ConfigReader.USERNAME, ConfigReader.PASSWORD)
    login_page.assert_login_success()
    
