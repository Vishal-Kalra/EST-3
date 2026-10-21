"""
T12  |  F12 Guest Checkout  |  Tester: Vishal Kalra (25675962)
URLs: checkout  index.php?route=checkout/checkout
      confirm   index.php?route=extension/maza/checkout/confirm
      success   index.php?route=checkout/success
Depends on F10/F11: checkout needs a non-empty cart. Payment method is Cash On Delivery (test site).
"""
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from helpers import (TIMEOUT, add_product_to_cart, js_click, open_route, safe_click,
                     type_into, wait_for_message, wait_for_text, wait_visible)


def start_guest_checkout(driver):
    """Put an iPhone in the cart, open Checkout and choose 'Guest Checkout'."""
    add_product_to_cart(driver, 40, 1)
    open_route(driver, "checkout/checkout")
    js_click(driver, driver.find_element(By.ID, "input-account-guest"))  # 'Guest Checkout' radio
    # choosing Guest reloads the form and disables its fields for ~0.5 s,
    # so wait until the Country list is enabled again before touching anything
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: d.find_element(By.ID, "input-payment-country").is_enabled())
    wait_visible(driver, "#input-payment-firstname")                 # guest form is shown


def wait_form_unlocked(driver):
    """Country/Region changes reload the shipping section and lock the form for a moment.
    Wait until the fields and the Continue button are enabled again."""
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: d.find_element(By.ID, "input-payment-country").is_enabled()
        and d.find_element(By.ID, "input-payment-zone").is_enabled()
        and d.find_element(By.ID, "button-save").is_enabled())
    time.sleep(1)  # small buffer for the shipping/payment methods to finish redrawing


def test_T12_S1_checkout_with_empty_cart(driver):
    # Input: open Checkout directly with nothing in the cart
    open_route(driver, "checkout/checkout")
    # Expected: redirected back to the Shopping Cart with the empty message
    wait_for_message(driver, "Your shopping cart is empty!")
    assert "route=checkout/cart" in driver.current_url


def test_T12_S2_guest_submits_blank_form(driver):
    # Input: guest details left blank, Terms not ticked, click Continue
    start_guest_checkout(driver)
    safe_click(driver, driver.find_element(By.ID, "button-save"))    # Continue
    # Expected: validation messages, user stays on checkout
    wait_for_message(driver, "First Name must be between 1 and 32 characters!")
    wait_for_message(driver, "E-Mail address does not appear to be valid!")
    wait_for_message(driver, "Warning: You must agree to the Terms & Conditions!")
    assert "route=checkout/checkout" in driver.current_url


def test_T12_S3_guest_places_order_with_valid_details(driver):
    # Input: valid Australian address, Cash On Delivery, Terms ticked
    start_guest_checkout(driver)
    type_into(driver, "#input-payment-firstname", "Alex")
    type_into(driver, "#input-payment-lastname", "Tester")
    type_into(driver, "#input-payment-email", "alex.guest@mailinator.com")
    type_into(driver, "#input-payment-telephone", "0412345678")
    type_into(driver, "#input-payment-address-1", "15 Broadway")
    type_into(driver, "#input-payment-city", "Sydney")
    type_into(driver, "#input-payment-postcode", "2007")
    Select(driver.find_element(By.ID, "input-payment-country")).select_by_value("13")  # 13 = Australia
    # the Region list reloads by AJAX after the country changes, so wait for NSW to appear
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located(
        (By.XPATH, "//select[@id='input-payment-zone']/option[text()='New South Wales']")))
    Select(driver.find_element(By.ID, "input-payment-zone")).select_by_visible_text("New South Wales")
    wait_form_unlocked(driver)                                       # shipping section reloads here
    agree = driver.find_element(By.ID, "input-agree")
    if not agree.is_selected():
        js_click(driver, agree)                                      # Terms & Conditions
    safe_click(driver, driver.find_element(By.ID, "button-save"))    # Continue
    # if the form was still busy the click is ignored, so click once more if we did not move on
    try:
        WebDriverWait(driver, 10).until(EC.url_contains("checkout/confirm"))
    except TimeoutException:
        wait_form_unlocked(driver)
        safe_click(driver, driver.find_element(By.ID, "button-save"))
    # Expected 1: Confirm Order page summarising the order
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("checkout/confirm"))
    wait_for_text(driver, "#content h1", "Confirm Order")
    safe_click(driver, wait_visible(driver, "#button-confirm"))      # Confirm Order
    # Expected 2: order placed page
    wait_for_text(driver, "#content h1", "Your order has been placed!")
    assert "route=checkout/success" in driver.current_url
