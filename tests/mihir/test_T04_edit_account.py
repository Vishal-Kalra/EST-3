from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from helpers import TIMEOUT, login_via_ui, open_route, page_text, type_into, wait_for_message

CONTINUE = "#content input[type='submit'][value='Continue']"
SAVED = "Success: Your account has been successfully updated."


def open_edit_account(driver, user):
    login_via_ui(driver, user["email"], user["password"])
    WebDriverWait(driver, TIMEOUT).until(lambda d: "account/account" in d.current_url)
    open_route(driver, "account/edit")


def test_T04_S1_update_name_and_telephone(driver, registered_user):
    open_edit_account(driver, registered_user)
    type_into(driver, "#input-firstname", "Mihir")
    type_into(driver, "#input-lastname", "Chauhan")
    type_into(driver, "#input-telephone", "0498765432")
    driver.find_element(By.CSS_SELECTOR, CONTINUE).click()
    wait_for_message(driver, SAVED)
    assert "account/account" in driver.current_url
    open_route(driver, "account/edit")
    assert driver.find_element(By.ID, "input-firstname").get_attribute("value") == "Mihir"
    assert driver.find_element(By.ID, "input-lastname").get_attribute("value") == "Chauhan"
    assert driver.find_element(By.ID, "input-telephone").get_attribute("value") == "0498765432"


def test_T04_S2_empty_first_name(driver, registered_user):
    open_edit_account(driver, registered_user)
    type_into(driver, "#input-firstname", "")
    driver.find_element(By.CSS_SELECTOR, CONTINUE).click()
    wait_for_message(driver, "First Name must be between 1 and 32 characters!")
    assert "account/edit" in driver.current_url
    assert SAVED not in page_text(driver)


def test_T04_S3_last_name_over_32_characters(driver, registered_user):
    open_edit_account(driver, registered_user)
    type_into(driver, "#input-firstname", "Mihir")
    type_into(driver, "#input-lastname", "A" * 33)
    driver.find_element(By.CSS_SELECTOR, CONTINUE).click()
    wait_for_message(driver, "Last Name must be between 1 and 32 characters!")
    assert "account/edit" in driver.current_url
    assert SAVED not in page_text(driver)
