def test_transfer_funds_page_is_displayed(transfer_funds_page):
    """Validation test: verify transfer form controls are displayed."""
    transfer_funds_page.assert_transfer_page_displayed()


def test_user_can_transfer_funds_between_accounts(transfer_funds_page):
    """Positive test: verify funds can be transferred between two accounts."""
    from_account_id, to_account_id = transfer_funds_page.get_two_different_account_ids()

    transfer_funds_page.transfer_funds(
        amount="100",
        from_account_id=from_account_id,
        to_account_id=to_account_id,
    )

    transfer_funds_page.assert_transfer_completed()
