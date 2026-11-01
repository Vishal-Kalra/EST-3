"""
T07	|	Product Search	|	Tester: Jasmine Joseph
Website: https://opencart.abstracta.us
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from helpers import wait_page_ready, wait_visible


def open_category(driver):
    """Open the Laptops & Notebooks category."""
    driver.get(
        "https://opencart.abstracta.us/index.php?route=product/category&path=18"
    )
    wait_page_ready(driver)


def get_product_names(driver):
    """Return visible product names from the category listing."""
    links = driver.find_elements(
        By.CSS_SELECTOR, ".product-thumb h4 a"
    )
    return [link.text.strip() for link in links if link.text.strip()]


def test_T09_S1_sort_products_by_name_ascending(driver):
   
    open_category(driver)  # Opening the category

   
    sort_dropdown = wait_visible(driver, "#input-sort")  # Select sorting order Name (A - Z)
    Select(sort_dropdown).select_by_visible_text("Name (A - Z)")
    wait_page_ready(driver)

    
    names = get_product_names(driver)   # Verifying if the products are sorted alphabetically
    assert len(names) > 0, "No products were displayed in the category"

    assert names == sorted(names, key=str.lower), (
        f"Products are not sorted alphabetically: {names}"
    )


def test_T09_S2_sort_products_by_price_ascending(driver):
    
    open_category(driver) # Opening the category

    
    sort_dropdown = wait_visible(driver, "#input-sort") # Select sorting order Price (Low > High)
    Select(sort_dropdown).select_by_visible_text("Price (Low > High)")
    wait_page_ready(driver)

    
    selected_option = Select(
        driver.find_element(By.ID, "input-sort")
    ).first_selected_option.text   # Verifying if the selected sorting option is retained

    assert selected_option == "Price (Low > High)", (
        f"Unexpected sorting option: {selected_option}"
    )

    
    names = get_product_names(driver) # Verify that products are displayed
    assert len(names) > 0, "No products were displayed after sorting by price"


def test_T09_S3_change_category_sorting(driver):
    
    open_category(driver) # Opening the category

    
    sort_dropdown = wait_visible(driver, "#input-sort") # Selecting sorting order Name (A - Z)
    Select(sort_dropdown).select_by_visible_text("Name (A - Z)")
    wait_page_ready(driver)

    
    sort_dropdown = wait_visible(driver, "#input-sort")   # Change sorting order to Name (Z - A)
    Select(sort_dropdown).select_by_visible_text("Name (Z - A)")
    wait_page_ready(driver)

    
    selected_option = Select(
        driver.find_element(By.ID, "input-sort")
    ).first_selected_option.text # Verifying if the new sorting option is selected

    assert selected_option == "Name (Z - A)", (
        f"Sorting did not change correctly. Selected: {selected_option}"
    )

    
    names = get_product_names(driver) # Verifying if those products are displayed
    assert len(names) > 0, "No products were displayed after changing the sort order" 
