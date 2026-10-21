"""
T07  |  F7 Product Search  |  Tester: Jasmine Joseph (25729738)
URL: Header search box on any page, results at https://ecommerce-playground.lambdatest.io/index.php?route=product/search&search=<keyword>
Depends on: None

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/jasmine/test_T07_product_search.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T07_S1_search_existing_keyword(driver):
    # Input:    'macbook'
    # Expected: At least one result, every name contains 'macbook' (case insensitive)
    pytest.skip("TODO: write T07 S1")


def test_T07_S2_search_keyword_with_no_match(driver):
    # Input:    'xyz123qwe'
    # Expected: 'There is no product that matches the search criteria.'
    pytest.skip("TODO: write T07 S2")


def test_T07_S3_search_with_spaces_only(driver):
    # Input:    '   ' (3 spaces)
    # Expected: Should show no results. Hint: the site lists all 75 products, so this should FAIL (real defect)
    pytest.skip("TODO: write T07 S3")
