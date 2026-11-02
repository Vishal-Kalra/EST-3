"""
T08	|	Product Search	|	Tester: Jasmine Joseph
Website: https://opencart.abstracta.us
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import wait_page_ready, wait_visible


def open_product_compare(driver):
    """Open the product comparison page."""
    driver.get(
        "https://opencart.abstracta.us/index.php?route=product/compare"
    )
    wait_page_ready(driver)


def add_to_compare(driver, product_id):
    """Open a product page and click its Compare button."""
    driver.get(
        f"https://opencart.abstracta.us/index.php?route=product/product&product_id={product_id}"
    )
    wait_page_ready(driver)

    # Find the product comparison button
    compare_button = wait_visible(
        driver, "button[ data-original-title='Compare this Product']"
    )
    compare_button.click()
    wait_page_ready(driver)


def test_T08_S1_add_product_to_compare(driver):
    # Input: add iPhone (product ID 40) to comparison
    add_to_compare(driver, 40)

    # Expected: website displays a success message
    body_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Success: You have added" in body_text, (
        "No success message appeared after adding a product to comparison"
    )


def test_T08_S2_compare_two_products(driver):
    # Input: add iPhone and MacBook to comparison
    add_to_compare(driver, 40)
    add_to_compare(driver, 43)

    # Open the comparison page
    open_product_compare(driver)

    # Expected: comparison page displays both products
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()

    assert "iphone" in body_text, (
        "iPhone was not found on the product comparison page"
    )
    assert "macbook" in body_text, (
        "MacBook was not found on the product comparison page"
    )

def test_T08_S3_open_compare_page_without_products(driver):
    # Step 1: Open the website in a fresh browser session.
    # The driver fixture creates a new browser for each test.
    driver.get(
        "https://opencart.abstracta.us/index.php?route=common/home"
    )
    wait_page_ready(driver)

    # Step 2: Open the product comparison page without adding any products.
    open_product_compare(driver)

    # Step 3: Verify that the comparison page opens successfully.
    assert "route=product/compare" in driver.current_url, (
        "The product comparison page did not open"
    )

    # Step 4: Verify that no products are displayed for comparison.
    product_rows = driver.find_elements(
        By.CSS_SELECTOR, "#content table tbody tr"
    )

    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()

    assert (
        "you have not chosen any products to compare" in page_text
        or "no products" in page_text
        or len(product_rows) == 0
    ), "The comparison page did not display the expected empty state"
