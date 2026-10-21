"""
T14  |  F14 Product Review  |  Tester: Mrunal Ghag (25717430)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=40  (Write a review section on the product page)
Depends on: F7/F8 (product page)

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/mrunal/test_T14_product_review.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T14_S1_submit_valid_review(driver):
    # Input:    Name 3 to 25 chars, review 25 to 1000 chars, a star rating
    # Expected: Success message saying the review is waiting for approval (check exact text)
    pytest.skip("TODO: write T14 S1")


def test_T14_S2_submit_review_too_short(driver):
    # Input:    Review text under 25 characters
    # Expected: Review length error (check exact text)
    pytest.skip("TODO: write T14 S2")


def test_T14_S3_submit_review_without_rating(driver):
    # Input:    Valid name + review, no rating selected
    # Expected: 'Please select a review rating!' (check exact text)
    pytest.skip("TODO: write T14 S3")
