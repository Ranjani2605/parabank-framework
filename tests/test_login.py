from pages.login_page import LoginPage

def test_valid_login(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login_with_default_user()
    login_page.assert_login_success()
