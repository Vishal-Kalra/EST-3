
"""
T15  |  Newsletter Subscription  |  Tester: Mrunal
URL: https://opencart.abstracta.us/index.php?route=account/newsletter
"""

from selenium.webdriver.common.by import By

from helpers import open_route, login_via_ui, page_text

NEWSLETTER_ROUTE = "account/newsletter"


def login_and_open_newsletter(driver, registered_user):
    login_via_ui(
        driver,
        registered_user["email"],
        registered_user["password"]
    )
    open_route(driver, NEWSLETTER_ROUTE)


def choose_newsletter_option(driver, value):
    option = driver.find_element(
        By.CSS_SELECTOR,
        f"input[name='newsletter'][value='{value}']"
    )
    if not option.is_selected():
        option.click()

    driver.find_element(
        By.CSS_SELECTOR,
        "#content input[type='submit'][value='Continue']"
    ).click()


def test_T15_S1_subscribe_to_newsletter(driver, registered_user):
    # Input: Log in and select Yes for newsletter subscription
    login_and_open_newsletter(driver, registered_user)
    choose_newsletter_option(driver, "1")

    # Expected: NSusbcription settings are updated as successful.
    result = page_text(driver).lower()
    assert "successfully updated" in result


def test_T15_S2_unsubscribe_from_newsletter(driver, registered_user):
    # Input: Log in and select No, unsubscribe for newsletter subscription
    login_and_open_newsletter(driver, registered_user)
    choose_newsletter_option(driver, "0")

    # Expected: Susbcription settings are updated as successful.
    result = page_text(driver).lower()
    assert "successfully updated" in result


def test_T15_S3_newsletter_page_without_login(driver):
    # Input: User tries to access newsletter without logging in
    open_route(driver, NEWSLETTER_ROUTE)

    # Expected: Unauthenticated user is redirected to login
    result = page_text(driver).lower()
    assert (
        "route=account/login" in driver.current_url
        or "returning customer" in result
        or "login" in result
    )
