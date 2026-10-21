"""
T09  |  F9 Product Comparison  |  Tester: Jasmine Joseph (25729738)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=product/compare  (Compare button on product pages)
Depends on: F7/F8 (products are found first)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/jasmine/test_T09_product_compare.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T09_S1_add_one_product_to_compare(driver):
    # Input:    Compare iPhone (product_id 40)
    # Expected: Pop up 'Success: You have added iPhone to your product comparison!' and iPhone in the table
    pytest.skip("TODO: write T09 S1")


def test_T09_S2_compare_keeps_only_four_products(driver):
    # Input:    Compare 5 products: ids 40, 43, 28, 29, 33
    # Expected: Only 4 shown, the first one (iPhone) dropped
    pytest.skip("TODO: write T09 S2")


def test_T09_S3_remove_product_from_compare(driver):
    # Input:    Compare MacBook (43) + HTC (28), click Remove under MacBook
    # Expected: 'Success: You have modified your product comparison!'
    pytest.skip("TODO: write T09 S3")
