"""
T07	|	Product Search	|	Tester: Jasmine Joseph
URL: https://opencart.abstracta.us/index.php?route=product/search
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from helpers import BASE_URL, wait_visible, wait_page_ready


def search_product(driver, keyword):
    """Enter a keyword into the header search box and submit it."""
    search_box = wait_visible(driver, "input[name='search']")
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.ENTER)

    wait_page_ready(driver)


def test_T07_S1_search_existing_product(driver):
    
    search_product(driver, "iPhone") # searching for an existing product

    # Search results page displays matching products
    assert "route=product/search" in driver.current_url, (
        "The website did not navigate to the product search results page"
    )

    # Find product-name links
    product_links = driver.find_elements(
        By.CSS_SELECTOR, ".product-thumb h4 a"
    )

    # getting visible product names
    product_names = [
        link.text.strip().lower()
        for link in product_links
        if link.text.strip()
    ]

    # Verify that at least one matching iPhone product is displayed
    assert any("iphone" in name for name in product_names), (
        f"No matching iPhone product found. Results: {product_names}"
    )


def test_T07_S2_search_nonexistent_product(driver):
 
    search_product(driver, "asdfghj") # random input

    products = driver.find_elements(
        By.CSS_SELECTOR, ".product-thumb"
    )
    assert len(products) == 0, (
        f"Expected no products, but found {len(products)} product cards"
    )


def test_T07_S3_search_empty_keyword(driver):

    search_box = wait_visible(driver, "input[name='search']")
    search_box.clear()
    search_box.send_keys(Keys.ENTER)

    wait_page_ready(driver)

    assert driver.find_element(By.TAG_NAME, "body").text.strip(), (
        "The page contains no visible text after an empty search"
    )
