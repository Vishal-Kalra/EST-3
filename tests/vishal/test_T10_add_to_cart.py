"""
T10  |  F10 Add to Cart  |  Tester: Vishal Kalra (25675962)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=40  (iPhone)
Depends on F7/F8 (find the product). Each scenario starts with an empty cart (fresh browser).
"""
from helpers import add_product_to_cart, cart_badge

IPHONE_ID = 40


def test_T10_S1_add_valid_quantity(driver):
    # Input: quantity 2
    toast = add_product_to_cart(driver, IPHONE_ID, 2)
    # Expected: success pop up and header cart badge shows 2
    assert "Success: You have added iPhone to your shopping cart!" in toast
    assert cart_badge(driver) == 2


def test_T10_S2_add_zero_quantity(driver):
    # Input: quantity 0
    toast = add_product_to_cart(driver, IPHONE_ID, 0)
    # Expected (requirement): an error such as 'quantity must be at least 1', no success message
    # Observed: 'Success: You have added iPhone...' is shown although the cart stays at 0
    # -> FAILS (defect D3: misleading success message)
    assert cart_badge(driver) == 0                     # nothing was added (this part holds)
    assert "Success" not in toast, "Defect: success message shown for quantity 0"


def test_T10_S3_add_negative_quantity(driver):
    # Input: first add 2 iPhones (valid), then try quantity -3
    add_product_to_cart(driver, IPHONE_ID, 2)
    toast = add_product_to_cart(driver, IPHONE_ID, -3)
    # Expected (requirement): negative quantity rejected, cart still holds 2
    # Observed: success message shown and the cart drops to 0 items
    # -> FAILS (defect D4: negative quantity accepted and wipes the cart)
    assert "Success" not in toast, "Defect: success message shown for quantity -3"
    assert cart_badge(driver) == 2, f"Defect: cart badge changed to {cart_badge(driver)}"
