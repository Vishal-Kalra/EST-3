"""
T04  |  F4 Edit Account Information  |  Tester: Mihir Chauhan (25620699)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=account/edit
Depends on: F1 + F2 (log in first with login_via_ui)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/mihir/test_T04_edit_account.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T04_S1_update_with_valid_details(driver, registered_user):
    # Input:    First Name 'Alexander', Telephone '0498765432'
    # Expected: 'Success: Your account has been successfully updated.'
    pytest.skip("TODO: write T04 S1")


def test_T04_S2_update_with_empty_first_name(driver, registered_user):
    # Input:    First Name cleared
    # Expected: 'First Name must be between 1 and 32 characters!'
    pytest.skip("TODO: write T04 S2")


def test_T04_S3_update_with_alphabetic_telephone(driver, registered_user):
    # Input:    Telephone 'abcdefg'
    # Expected: Should be rejected. Hint: the site actually ACCEPTS it, so this scenario should FAIL (real defect, write it up!)
    pytest.skip("TODO: write T04 S3")
