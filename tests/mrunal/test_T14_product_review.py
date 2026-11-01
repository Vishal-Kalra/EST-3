
"""
T14  |  Product Review  |  Tester: Mrunal
URL: https://opencart.abstracta.us/index.php?route=product/product&product_id=40
Product: iPhone
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from helpers import open_route, type_into, page_text, TIMEOUT

PRODUCT_ID = 40
PRODUCT_ROUTE = f"product/product&product_id={PRODUCT_ID}"


def open_review_form(driver):
    open_route(driver, PRODUCT_ROUTE)
    driver.find_element(
        By.CSS_SELECTOR, "a[href='#tab-review']"
    ).click()
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: d.find_element(By.ID, "input-review").is_displayed()
    )


def submit_review(driver, name, review):
    type_into(driver, "#input-name", name)
    type_into(driver, "#input-review", review)
    driver.find_element(
        By.CSS_SELECTOR, "input[name='rating'][value='5']"
    ).click()
    driver.find_element(By.ID, "button-review").click()


def test_T14_S1_submit_valid_review(driver):
    # Input: valid name, review longer than 25 characters and 5-star rating
    open_review_form(driver)
    submit_review(
        driver,
        "Test11 Student",
        "This is an amazing product and I am happy with its quality. I will buy one for my friend "
    )

    # Expected: review submission confirmation appears
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: "thank you for your review" in page_text(d).lower()
        or "submitted to team" in page_text(d).lower()
    )
    result = page_text(driver).lower()
    assert (
        "thank you for your review" in result
        or "submitted to team for approval" in result
    )


def test_T14_S2_submit_empty_review(driver):
    # Input: name and rating supplied, but review text left empty
    open_review_form(driver)
    type_into(driver, "#input-name", "Testing Student 15")
    driver.find_element(
        By.CSS_SELECTOR, "input[name='rating'][value='5']"
    ).click()
    driver.find_element(By.ID, "button-review").click()

    # Expected: empty review is not accepted
    result = page_text(driver).lower()
    assert "thank you for your review" not in result
    assert "submitted for approval" not in result


def test_T14_S3_submit_short_review(driver):
    # Input: review shorter than 25 characters
    open_review_form(driver)
    submit_review(driver, "Test 7 Student", "Nice product.")

    # Expected: short review is not accepted
    result = page_text(driver).lower()
    assert "thank you for your review" not in result
    assert "Keep shopping for exciting offers and deals!" not in result
