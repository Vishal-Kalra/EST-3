"""
T12  |  F12 Guest Checkout  |  Tester: Vishal Kalra (25675962)
URLs: checkout  index.php?route=checkout/checkout   (6 step accordion on one page)
      success   index.php?route=checkout/success
Depends on F10/F11: checkout needs a non-empty cart. Payment method is Cash On Delivery (test site).
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from helpers import (TIMEOUT, add_product_to_cart, click_when_settled, open_route, type_into,
                     wait_for_message, wait_for_text, wait_page_ready, wait_visible)


def wait_country_unlocked(driver):
    """The Country list is locked while the site loads its regions by AJAX; wait until it is usable."""
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: d.find_element(By.ID, "input-payment-country").is_enabled())
    wait_page_ready(driver)


def start_guest_checkout(driver):
    """Put an iPhone in the cart, open Checkout, choose 'Guest Checkout' and press Continue (Step 1)."""
    add_product_to_cart(driver, 40, 1)
    open_route(driver, "checkout/checkout")
    click_when_settled(driver, "input[name='account'][value='guest']")   # 'Guest Checkout' radio
    click_when_settled(driver, "#button-account")                        # Step 1 Continue
    wait_visible(driver, "#input-payment-firstname")                 # Step 2 guest form is open
    wait_country_unlocked(driver)                                    # form finished loading


def test_T12_S1_checkout_with_empty_cart(driver):
    # Input: open Checkout directly with nothing in the cart
    open_route(driver, "checkout/checkout")
    # Expected: redirected back to the Shopping Cart with the empty message
    wait_for_message(driver, "Your shopping cart is empty!")
    assert "route=checkout/cart" in driver.current_url


def test_T12_S2_guest_submits_blank_form(driver):
    # Input: guest billing details left blank, click Continue in Step 2
    start_guest_checkout(driver)
    click_when_settled(driver, "#button-guest")
    # Expected: validation messages under the fields, user stays on checkout
    wait_for_message(driver, "First Name must be between 1 and 32 characters!")
    wait_for_message(driver, "E-Mail address does not appear to be valid!")
    wait_for_message(driver, "Please select a region / state!")
    assert "route=checkout/checkout" in driver.current_url


def test_T12_S3_guest_places_order_with_valid_details(driver):
    # Input: valid Australian address, Flat Rate shipping, Cash On Delivery, Terms ticked
    start_guest_checkout(driver)
    type_into(driver, "#input-payment-firstname", "Tester1")
    type_into(driver, "#input-payment-lastname", "Tester2")
    type_into(driver, "#input-payment-email", "test.guest@mailinator.com")
    type_into(driver, "#input-payment-telephone", "0412345678")
    type_into(driver, "#input-payment-address-1", "12 Test Street")
    type_into(driver, "#input-payment-city", "Sydney")
    type_into(driver, "#input-payment-postcode", "2000")
    wait_country_unlocked(driver)
    Select(driver.find_element(By.ID, "input-payment-country")).select_by_visible_text("Australia")
    # the Region list reloads by AJAX after the country changes, so wait for NSW to appear
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located(
        (By.XPATH, "//select[@id='input-payment-zone']/option[text()='New South Wales']")))
    wait_country_unlocked(driver)                                    # region list finished loading
    Select(driver.find_element(By.ID, "input-payment-zone")).select_by_visible_text("New South Wales")
    click_when_settled(driver, "#button-guest")                               # Step 2 Continue
    # Step 4: Delivery Method (Flat Shipping Rate is already selected)
    click_when_settled(driver, "#button-shipping-method")
    # Step 5: Payment Method -> Cash On Delivery and accept the Terms & Conditions
    click_when_settled(driver, "#collapse-payment-method input[value='cod']")
    agree = wait_visible(driver, "#collapse-payment-method input[name='agree']")
    if not agree.is_selected():
        click_when_settled(driver, "#collapse-payment-method input[name='agree']")
    click_when_settled(driver, "#button-payment-method")
    # Expected 1: Step 6 Confirm Order shows the order summary
    wait_for_text(driver, "#collapse-checkout-confirm", "iPhone")
    click_when_settled(driver, "#button-confirm")                             # Confirm Order
    # Expected 2: order placed page
    wait_for_text(driver, "#content h1", "Your order has been placed!")
    assert "route=checkout/success" in driver.current_url
