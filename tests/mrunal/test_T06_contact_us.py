
"""
T6  |  Contact Us  |  Tester: Mrunal
URL: https://opencart.abstracta.us/index.php?route=information/contact
"""

from helpers import open_route, type_into, page_text

CONTACT_ROUTE = "information/contact"


def test_T6_S1_valid_contact_enquiry(driver):
    # Input: Valid name, email and enquiry message
    open_route(driver, CONTACT_ROUTE)
    type_into(driver, "#input-name", "Test Student 5")
    type_into(driver, "#input-email", "student2@example.com")
    type_into(
        driver,
        "#input-enquiry",
        "I would like to check about some of the products available on the website."
    )
    driver.find_element(
        "css selector", "#content input[type='submit']"
    ).click()

    # Expected: contact enquiry is successfully submitted
    result = page_text(driver).lower()
    assert (
        "route=information/contact/success" in driver.current_url
        or "successfully sent" in result
    )


def test_T6_S2_invalid_email(driver):
    # Input: valid name and enquiry, but invalid email address
    open_route(driver, CONTACT_ROUTE)
    type_into(driver, "#input-name", "Testing Name field")
    type_into(driver, "#input-email", "invalid-email address entry")
    type_into(
        driver,
        "#input-enquiry",
        "This scenario is used to test email validation."
    )
    driver.find_element(
        "css selector", "#content input[type='submit']"
    ).click()

    # Expected: Invalid email entry will not be submitted
    result = page_text(driver).lower()
    assert "route=information/contact/success" not in driver.current_url
    assert "successfully sent" not in result


def test_T6_S3_empty_contact_form(driver):
    # Input: Leave all contact form fields empty
    open_route(driver, CONTACT_ROUTE)
    driver.find_element(
        "css selector", "#content input[type='submit']"
    ).click()

    # Expected: empty form is not successfully submitted
    result = page_text(driver).lower()
    assert "route=information/contact/success" not in driver.current_url
    assert "successfully sent" not in result
