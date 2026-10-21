"""
T06  |  F6 Contact Us  |  Tester: Mrunal Ghag (25717430)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=information/contact
Depends on: None (independent)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/mrunal/test_T06_contact_us.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T06_S1_send_valid_enquiry(driver):
    # Input:    Name 'Alex Tester', valid email, enquiry 10+ chars
    # Expected: 'Your enquiry has been successfully sent to the store owner!'
    pytest.skip("TODO: write T06 S1")


def test_T06_S2_send_with_too_short_name_and_enquiry(driver):
    # Input:    Name 'A', enquiry 'Short'
    # Expected: 'Name must be between 3 and 32 characters!' and 'Enquiry must be between 10 and 3000 characters!'
    pytest.skip("TODO: write T06 S2")


def test_T06_S3_send_with_invalid_email(driver):
    # Input:    Email 'alex.tester.mailinator.com' (no @)
    # Expected: 'E-Mail Address does not appear to be valid!'
    pytest.skip("TODO: write T06 S3")
