"""
T13  |  F13 Change Password  |  Tester: Mihir Chauhan (25620699)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=account/password
Depends on: F1 + F2 (log in first)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/mihir/test_T13_change_password.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T13_S1_change_with_matching_passwords(driver):
    # Input:    New Password + matching Confirm (4 to 20 chars)
    # Expected: Success message on My Account (check exact text on the site). Tip: use a NEW unique account here, not registered_user, or other tests break
    pytest.skip("TODO: write T13 S1")


def test_T13_S2_change_with_mismatched_confirm(driver, registered_user):
    # Input:    Password 'New@1234', Confirm 'Other@5678'
    # Expected: Password confirmation error (check exact text)
    pytest.skip("TODO: write T13 S2")


def test_T13_S3_change_with_too_short_password(driver, registered_user):
    # Input:    Password '12' (below 4 chars)
    # Expected: 'Password must be between 4 and 20 characters!' (check exact text)
    pytest.skip("TODO: write T13 S3")
