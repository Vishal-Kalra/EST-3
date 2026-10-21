"""
T05  |  F5 Wish List  |  Tester: Mihir Chauhan (25620699)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=account/wishlist  (heart button on https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=40)
Depends on: F2 (must be logged in) + F8 (product pages)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/mihir/test_T05_wishlist.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T05_S1_guest_cannot_save_to_wishlist(driver):
    # Input:    Not logged in, click Add to Wish List on the iPhone page
    # Expected: Pop up 'You must login or create an account to save iPhone to your wish list!'
    pytest.skip("TODO: write T05 S1")


def test_T05_S2_logged_in_user_adds_product(driver, registered_user):
    # Input:    Log in, click Add to Wish List on iPhone
    # Expected: Pop up 'Success: You have added iPhone to your wish list!' and iPhone listed on account/wishlist
    pytest.skip("TODO: write T05 S2")


def test_T05_S3_logged_in_user_removes_product(driver, registered_user):
    # Input:    Log in, open wish list, click Remove on iPhone
    # Expected: 'Success: You have modified your wish list!' and 'No results!'
    pytest.skip("TODO: write T05 S3")
