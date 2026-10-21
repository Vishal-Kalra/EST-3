"""
T15  |  F15 Newsletter Subscription  |  Tester: Mrunal Ghag (25717430)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=account/newsletter
Depends on: F1 + F2 (log in first)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/mrunal/test_T15_newsletter.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T15_S1_subscribe_to_newsletter(driver, registered_user):
    # Input:    Log in, choose Subscribe 'Yes', Continue
    # Expected: Success message (check exact text) and 'Yes' still selected when reopening the page
    pytest.skip("TODO: write T15 S1")


def test_T15_S2_unsubscribe_from_newsletter(driver, registered_user):
    # Input:    Log in, choose 'No', Continue
    # Expected: Success message and 'No' selected when reopening
    pytest.skip("TODO: write T15 S2")


def test_T15_S3_guest_cannot_open_newsletter_page(driver):
    # Input:    Not logged in, open account/newsletter directly
    # Expected: Redirected to route=account/login
    pytest.skip("TODO: write T15 S3")
