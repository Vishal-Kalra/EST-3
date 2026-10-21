"""
T11  |  F11 Shopping Cart Management (update quantity / remove)  |  Tester: Vishal Kalra (25675962)
URL: https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart
Depends on F10: the cart must already contain an item.
"""
import re

from selenium.webdriver.common.by import By

from helpers import add_product_to_cart, open_route, wait_for_message, wait_visible

MACBOOK_ID = 43
EMPTY = "Your shopping cart is empty!"


def open_cart_with_macbook(driver):
    """Add one MacBook (F10) and open the Shopping Cart page."""
    add_product_to_cart(driver, MACBOOK_ID, 1)
    open_route(driver, "checkout/cart")
    return wait_visible(driver, "#content input[name^='quantity']")  # qty box of the MacBook row


def money(text):
    """'$602.00' -> 602.0"""
    return float(re.sub(r"[^0-9.]", "", text))


def test_T11_S1_update_quantity_to_three(driver):
    # Input: change quantity 1 -> 3 and click the Update (refresh) button
    qty = open_cart_with_macbook(driver)
    qty.clear()
    qty.send_keys("3")
    driver.find_element(By.CSS_SELECTOR, "#content button[title='Update']").click()
    # Expected: success banner, quantity 3, row total = 3 x unit price
    wait_for_message(driver, "Success: You have modified your shopping cart!")
    row = driver.find_element(By.CSS_SELECTOR, "#content form table tbody tr")
    cells = row.find_elements(By.TAG_NAME, "td")
    unit, total = money(cells[-2].text), money(cells[-1].text)   # Unit Price, Total columns
    assert row.find_element(By.CSS_SELECTOR, "input[name^='quantity']").get_attribute("value") == "3"
    assert abs(total - unit * 3) < 0.01


def test_T11_S2_remove_item_with_remove_button(driver):
    # Input: click the red Remove (X) button on the only row
    open_cart_with_macbook(driver)
    driver.find_element(By.CSS_SELECTOR, "#content button[title='Remove']").click()
    # Expected: the cart becomes empty
    wait_for_message(driver, EMPTY)


def test_T11_S3_update_quantity_to_zero(driver):
    # Input: change quantity to 0 and click Update
    qty = open_cart_with_macbook(driver)
    qty.clear()
    qty.send_keys("0")
    driver.find_element(By.CSS_SELECTOR, "#content button[title='Update']").click()
    # Expected: a zero quantity removes the line, cart is empty
    wait_for_message(driver, EMPTY)
