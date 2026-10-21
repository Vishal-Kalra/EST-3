"""
T02  |  F2 User Login  |  Tester: Prithvi Krishna Prasad (25966060)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=account/login
Depends on: F1 (needs a registered account, use the registered_user fixture)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/prithvi/test_T02_login.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T02_S1_login_with_valid_credentials(driver, registered_user):
    # Input:    registered_user email + password
    # Expected: URL contains route=account/account and page shows 'My Account'
    pytest.skip("TODO: write T02 S1")


def test_T02_S2_login_with_wrong_password(driver, registered_user):
    # Input:    registered_user email + 'Wrong@999'
    # Expected: 'Warning: No match for E-Mail Address and/or Password.'
    pytest.skip("TODO: write T02 S2")


def test_T02_S3_login_with_unregistered_email(driver):
    # Input:    unique_email('nobody') + 'Test@1234'
    # Expected: Same 'No match' warning
    pytest.skip("TODO: write T02 S3")
