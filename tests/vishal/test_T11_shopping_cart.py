"""
T11  |  F11 Shopping Cart Management (update quantity / remove)  |  Tester: Vishal Kalra (25675962)
URL: https://opencart.abstracta.us/index.php?route=checkout/cart
Depends on F10: the cart must already contain an item.
"""
import re

from selenium.webdriver.common.by import By

from helpers import add_product_to_cart, open_route, safe_click, wait_for_message, wait_visible

MACBOOK_ID = 43
EMPTY = "Your shopping cart is empty!"
ROW = "#content form table tbody tr"                     # the product row in the cart table
UPDATE_BTN = ROW + " button.btn-primary"                 # blue Update (refresh) button
REMOVE_BTN = ROW + " button.btn-danger"                  # red Remove (X) button


def open_cart_with_macbook(driver):
    """Add one MacBook (F10) and open the Shopping Cart page."""
    add_product_to_cart(driver, MACBOOK_ID, 1)
    open_route(driver, "checkout/cart")
    return wait_visible(driver, ROW + " input[name^='quantity']")  # qty box of the MacBook row


def money(text):
    """'$1,806.00' -> 1806.0"""
    return float(re.sub(r"[^0-9.]", "", text))


def test_T11_S1_update_quantity_to_three(driver):
    # Input: change quantity 1 -> 3 and click the Update button
    qty = open_cart_with_macbook(driver)
    qty.clear()
    qty.send_keys("3")
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, UPDATE_BTN))
    # Expected: success banner, quantity 3, row total = 3 x unit price
    wait_for_message(driver, "Success: You have modified your shopping cart!")
    row = driver.find_element(By.CSS_SELECTOR, ROW)
    cells = row.find_elements(By.TAG_NAME, "td")
    unit, total = money(cells[-2].text), money(cells[-1].text)   # Unit Price, Total columns
    assert row.find_element(By.CSS_SELECTOR, "input[name^='quantity']").get_attribute("value") == "3"
    assert abs(total - unit * 3) < 0.01


def test_T11_S2_remove_item_with_remove_button(driver):
    # Input: click the red Remove (X) button on the only row
    open_cart_with_macbook(driver)
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, REMOVE_BTN))
    # Expected: the cart becomes empty
    wait_for_message(driver, EMPTY)


def test_T11_S3_update_quantity_to_zero(driver):
    # Input: change quantity to 0 and click Update
    qty = open_cart_with_macbook(driver)
    qty.clear()
    qty.send_keys("0")
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, UPDATE_BTN))
    # Expected: a zero quantity removes the line, cart is empty
    wait_for_message(driver, EMPTY)
