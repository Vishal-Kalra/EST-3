from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from helpers import (TIMEOUT, click_and_get_alert, login_via_ui, open_route, safe_click,
                     wait_for_message, wait_visible)

IPHONE_ID = "40"
HEART = f"button[onclick=\"wishlist.add('{IPHONE_ID}');\"]"
WISHLIST_ROW = f"#content table a[href*='product_id={IPHONE_ID}']"


def wait_for_route(driver, route):
    WebDriverWait(driver, TIMEOUT).until(lambda d: route in d.current_url)


def log_in(driver, user):
    login_via_ui(driver, user["email"], user["password"])
    wait_for_route(driver, "account/account")


def add_iphone_from_search(driver):
    open_route(driver, "product/search&search=iPhone")
    return click_and_get_alert(driver, wait_visible(driver, HEART))


def test_T13_S1_logged_in_customer_adds_product(driver, registered_user):
    log_in(driver, registered_user)
    alert = add_iphone_from_search(driver)
    assert "Success: You have added iPhone to your wish list!" in alert
    open_route(driver, "account/wishlist")
    wait_for_message(driver, "My Wish List")
    assert driver.find_elements(By.CSS_SELECTOR, WISHLIST_ROW)


def test_T13_S2_guest_adds_product(driver):
    alert = add_iphone_from_search(driver)
    assert "You must login or create an account to save iPhone to your wish list!" in alert
    open_route(driver, "account/wishlist")
    wait_for_route(driver, "account/login")


def test_T13_S3_customer_removes_product(driver, registered_user):
    log_in(driver, registered_user)
    add_iphone_from_search(driver)
    open_route(driver, "account/wishlist")
    remove = wait_visible(driver, f"#content a[href*='remove={IPHONE_ID}']")
    safe_click(driver, remove)
    wait_for_message(driver, "Success: You have modified your wish list!")
    assert not driver.find_elements(By.CSS_SELECTOR, WISHLIST_ROW)
