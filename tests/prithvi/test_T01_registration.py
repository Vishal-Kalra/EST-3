"""
T01  |  F1 User Registration  |  Tester: Prithvi Krishna Prasad (25966060)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=account/register
Depends on: None (root function, everyone else's account tests need this)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/prithvi/test_T01_registration.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T01_S1_register_with_valid_new_details(driver):
    # Input:    All fields valid, a brand new email (use unique_email('reg')), Privacy Policy ticked
    # Expected: Heading 'Your Account Has Been Created!' and URL contains route=account/success
    pytest.skip("TODO: write T01 S1")


def test_T01_S2_register_with_mismatched_confirm_password(driver):
    # Input:    Valid details but Password 'Test@1234' and Confirm 'Other@5678'
    # Expected: 'Password confirmation does not match password!' and still on route=account/register
    pytest.skip("TODO: write T01 S2")


def test_T01_S3_register_with_already_registered_email(driver, registered_user):
    # Input:    Same email as registered_user['email'] (fixture)
    # Expected: 'Warning: E-Mail Address is already registered!'
    pytest.skip("TODO: write T01 S3")
