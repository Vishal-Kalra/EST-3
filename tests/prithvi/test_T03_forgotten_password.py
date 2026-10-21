"""
T03  |  F3 Forgotten Password  |  Tester: Prithvi Krishna Prasad (25966060)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=account/forgotten
Depends on: F1 (registered email needed for the success case)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/prithvi/test_T03_forgotten_password.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T03_S1_reset_with_registered_email(driver, registered_user):
    # Input:    registered_user email
    # Expected: Back on route=account/login with 'An email with a confirmation link has been sent your email address.'
    pytest.skip("TODO: write T03 S1")


def test_T03_S2_reset_with_unregistered_email(driver):
    # Input:    unique_email('ghost')
    # Expected: 'Warning: The E-Mail Address was not found in our records, please try again!'
    pytest.skip("TODO: write T03 S2")


def test_T03_S3_reset_with_empty_email(driver):
    # Input:    Empty email field
    # Expected: Same 'not found' warning
    pytest.skip("TODO: write T03 S3")
