def test_find_transactions_page_is_displayed(find_transactions_page):
    """Validation test: verify search controls are displayed."""
    find_transactions_page.assert_find_transactions_page_displayed()


def test_user_can_find_transaction_by_id(find_transactions_page):
    """Positive test: verify one transaction can be found by id."""
    find_transactions_page.page.route(
        "**/services_proxy/bank/transactions/7777",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=(
                '{"id":7777,"description":"Funds Transfer Received",'
                '"type":"Credit","amount":150.0,"date":"2024-03-10T00:00:00"}'
            ),
        ),
    )

    find_transactions_page.search_by_transaction_id("7777")

    find_transactions_page.assert_results_displayed(expected_row_count=1)
    find_transactions_page.assert_result_row_contains(
        row_index=0,
        expected_date="03-10-2024",
        expected_description="Funds Transfer Received",
        expected_debit="",
        expected_credit="$150.00",
    )


def test_user_can_find_transactions_by_amount(find_transactions_page):
    """Positive test: verify multiple transactions can be found by amount."""
    account_id = find_transactions_page.get_account_ids()[0]
    find_transactions_page.page.route(
        f"**/services_proxy/bank/accounts/{account_id}/transactions/amount/25",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=(
                '[{"id":9001,"description":"Grocery Store","type":"Debit",'
                '"amount":25.0,"date":"2024-03-11T00:00:00"},'
                '{"id":9002,"description":"Refund","type":"Credit",'
                '"amount":25.0,"date":"2024-03-12T00:00:00"}]'
            ),
        ),
    )

    find_transactions_page.select_account(account_id)
    find_transactions_page.search_by_amount("25")

    find_transactions_page.assert_results_displayed(expected_row_count=2)
    find_transactions_page.assert_result_row_contains(
        row_index=0,
        expected_date="03-11-2024",
        expected_description="Grocery Store",
        expected_debit="$25.00",
        expected_credit="",
    )
    find_transactions_page.assert_result_row_contains(
        row_index=1,
        expected_date="03-12-2024",
        expected_description="Refund",
        expected_debit="",
        expected_credit="$25.00",
    )


def test_find_transactions_shows_empty_results_for_not_found(find_transactions_page):
    """Negative test: verify not-found responses still show an empty results table."""
    account_id = find_transactions_page.get_account_ids()[0]
    find_transactions_page.page.route(
        f"**/services_proxy/bank/accounts/{account_id}/transactions/onDate/01-01-1999",
        lambda route: route.fulfill(status=404, content_type="application/json", body="[]"),
    )

    find_transactions_page.select_account(account_id)
    find_transactions_page.search_by_date("01-01-1999")

    find_transactions_page.assert_no_results_displayed()


def test_find_transactions_shows_validation_for_invalid_amount(find_transactions_page):
    """Validation test: verify amount input rejects non-numeric values."""
    find_transactions_page.search_by_amount("abc")
    find_transactions_page.assert_invalid_amount_error()
