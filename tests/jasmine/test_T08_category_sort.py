"""
T08  |  F8 Category Browsing and Sorting  |  Tester: Jasmine Joseph (25729738)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=57  (Tablets)
Depends on: None

HOW TO USE THIS FILE
  1. Read the README first (setup + how the helpers work).
  2. Look at tests/vishal/ for finished examples of the same style.
  3. Replace each pytest.skip(...) line with your steps and asserts.
  4. Run only your file:  pytest tests/jasmine/test_T08_category_sort.py
  5. The suggested inputs/outputs are a starting point. Always open the page
     yourself and copy the exact message text before asserting it.
"""
import pytest
from selenium.webdriver.common.by import By

from helpers import (open_route, type_into, wait_visible, first_visible, js_click,
                     wait_for_message, page_text, unique_email, login_via_ui,
                     register_via_ui, click_and_get_toast)  # remove the ones you don't use


def test_T08_S1_open_category_page(driver):
    # Input:    Open Tablets category
    # Expected: Heading 'Tablets', 15 product cards, 'Showing 1 to 15 of 75'
    pytest.skip("TODO: write T08 S1")


def test_T08_S2_sort_by_price_low_to_high(driver):
    # Input:    Sort By 'Price (Low > High)'
    # Expected: Prices never go down; URL has sort=p.price&order=ASC
    pytest.skip("TODO: write T08 S2")


def test_T08_S3_sort_by_name_a_to_z(driver):
    # Input:    Sort By 'Name (A - Z)'
    # Expected: Names alphabetical; URL has sort=pd.name
    pytest.skip("TODO: write T08 S3")
