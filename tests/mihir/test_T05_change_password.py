from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from helpers import (TIMEOUT, login_via_ui, open_route, page_text, register_via_ui, type_into,
                     unique_email, wait_for_message)

CONTINUE = "#content input[type='submit'][value='Continue']"
CHANGED = "Success: Your password has been successfully updated."
OLD_PASSWORD = "Test@1234"
NEW_PASSWORD = "NewPass@2026"


def wait_for_route(driver, route):
    WebDriverWait(driver, TIMEOUT).until(lambda d: route in d.current_url)


def submit_password(driver, password, confirm):
    open_route(driver, "account/password")
    type_into(driver, "#input-password", password)
    type_into(driver, "#input-confirm", confirm)
    driver.find_element(By.CSS_SELECTOR, CONTINUE).click()


def test_T05_S1_change_to_valid_password(driver):
    email = unique_email("pwd")
    register_via_ui(driver, "Mihir", "Chauhan", email, "0412345678", OLD_PASSWORD)
    wait_for_route(driver, "account/success")
    submit_password(driver, NEW_PASSWORD, NEW_PASSWORD)
    wait_for_message(driver, CHANGED)
    open_route(driver, "account/logout")
    wait_for_message(driver, "Account Logout")
    login_via_ui(driver, email, NEW_PASSWORD)
    wait_for_route(driver, "account/account")
    assert "My Account" in page_text(driver)


def test_T05_S2_password_shorter_than_4_characters(driver, registered_user):
    login_via_ui(driver, registered_user["email"], registered_user["password"])
    wait_for_route(driver, "account/account")
    submit_password(driver, "abc", "abc")
    wait_for_message(driver, "Password must be between 4 and 20 characters!")
    assert "account/password" in driver.current_url
    assert CHANGED not in page_text(driver)


def test_T05_S3_confirmation_does_not_match(driver, registered_user):
    login_via_ui(driver, registered_user["email"], registered_user["password"])
    wait_for_route(driver, "account/account")
    submit_password(driver, "Valid@1234", "Different@1234")
    wait_for_message(driver, "Password confirmation does not match password!")
    assert "account/password" in driver.current_url
    assert CHANGED not in page_text(driver)
