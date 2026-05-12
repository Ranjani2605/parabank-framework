from playwright.sync_api import expect


def test_open_new_account_form_is_displayed(open_new_account_page):
    """Validation test: verify form visibility, navigation, and enabled controls."""
    open_new_account_page.assert_navigation_url()
    open_new_account_page.assert_open_account_page_displayed()
    open_new_account_page.assert_minimum_deposit_message_displayed()
    assert open_new_account_page.get_available_from_accounts_count() > 0


def test_user_can_select_savings_account_type(open_new_account_page):
    """UI interaction test: verify account type dropdown selection."""
    open_new_account_page.select_account_type("SAVINGS")
    assert open_new_account_page.get_selected_account_type() == "SAVINGS"


def test_user_can_select_source_account(open_new_account_page):
    """UI interaction test: verify source account dropdown selection."""
    from_account_options = open_new_account_page.page.locator(
        f"{open_new_account_page.from_account_dropdown} option"
    )
    last_account_id = from_account_options.last.inner_text()

    open_new_account_page.select_from_account_by_value(last_account_id)

    assert open_new_account_page.get_selected_from_account() == last_account_id


def test_open_checking_account_successfully(open_new_account_page):
    """Positive test: verify a checking account can be opened successfully."""
    open_new_account_page.open_new_account("CHECKING")
    open_new_account_page.assert_account_opened_successfully()


def test_open_new_account_shows_error_when_service_fails(open_new_account_page):
    """Negative test: verify error message when account creation API fails."""
    open_new_account_page.page.route(
        "**/services_proxy/bank/createAccount**",
        lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body='{"message":"Internal server error"}',
        ),
    )

    open_new_account_page.open_new_account("SAVINGS")

    open_new_account_page.assert_open_account_error_displayed()


def test_open_new_account_button_is_enabled(open_new_account_page):
    """Validation test: verify form submission button is enabled."""
    expect(
        open_new_account_page.page.locator(open_new_account_page.open_account_button)
    ).to_be_enabled()
