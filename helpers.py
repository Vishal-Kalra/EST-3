"""
Small reusable helpers so each test file stays short and readable.
Every locator below was checked against the live site in October 2026.
"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Every page on the site is index.php?route=<something>
BASE_URL = "https://ecommerce-playground.lambdatest.io/index.php?route="
TIMEOUT = 15  # seconds; the playground can be slow at peak times


def open_route(driver, route):
    """Open a page by its OpenCart route, e.g. open_route(driver, 'account/login')."""
    driver.get(BASE_URL + route)


def wait_visible(driver, css):
    """Wait until an element is visible and return it."""
    return WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, css))
    )


def first_visible(driver, css):
    """
    The theme renders some controls twice (desktop + mobile copy, one hidden).
    This waits for and returns the copy that is actually displayed.
    """
    def _find(d):
        for el in d.find_elements(By.CSS_SELECTOR, css):
            if el.is_displayed():
                return el
        return False
    return WebDriverWait(driver, TIMEOUT).until(_find)


def type_into(driver, css, text):
    """Clear a field and type new text into it."""
    field = wait_visible(driver, css)
    field.clear()
    field.send_keys(text)


def js_click(driver, element):
    """
    Click with JavaScript. Used for the theme's custom checkboxes/radios, whose real
    <input> is hidden under a styled label (and the label also contains a link we must not hit).
    """
    driver.execute_script("arguments[0].click();", element)


def safe_click(driver, element):
    """
    Scroll the element to the middle of the screen, then click it. If something
    (a sticky bar, a loading overlay) still covers it, fall back to a JavaScript click.
    """
    from selenium.common.exceptions import ElementClickInterceptedException
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.click()
    except ElementClickInterceptedException:
        js_click(driver, element)


def page_text(driver):
    """All visible text on the page (alerts sit outside #content on some pages)."""
    return driver.find_element(By.TAG_NAME, "body").text


def wait_for_message(driver, text):
    """Wait until a success/warning/error message with this exact text is visible anywhere on the page."""
    wait_for_text(driver, "body", text)


def wait_for_text(driver, css, text):
    """Wait until the given text appears inside the element."""
    WebDriverWait(driver, TIMEOUT).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, css), text)
    )


def click_and_get_toast(driver, element):
    """Click a button that shows a pop up notification (wishlist / compare) and return its text."""
    before = len(driver.find_elements(By.CSS_SELECTOR, "#notification-box-top .toast"))
    safe_click(driver, element)
    return wait_new_toast(driver, before)


def cart_badge(driver):
    """Number shown on the header cart icon (read via textContent because one copy is hidden)."""
    badge = driver.find_element(By.CSS_SELECTOR, ".cart-item-total")
    return int(driver.execute_script("return arguments[0].textContent;", badge).strip())


def unique_email(prefix):
    """A never-used-before email, e.g. reg.1728201234567@mailinator.com"""
    return f"{prefix}.{int(time.time() * 1000)}@mailinator.com"


def register_via_ui(driver, first, last, email, phone, password, confirm=None, agree=True):
    """Fill and submit the Register Account form (F1)."""
    open_route(driver, "account/register")
    type_into(driver, "#input-firstname", first)
    type_into(driver, "#input-lastname", last)
    type_into(driver, "#input-email", email)
    type_into(driver, "#input-telephone", phone)
    type_into(driver, "#input-password", password)
    type_into(driver, "#input-confirm", confirm if confirm is not None else password)
    if agree:
        js_click(driver, driver.find_element(By.ID, "input-agree"))  # tick Privacy Policy
    driver.find_element(By.CSS_SELECTOR, "#content input[type='submit'][value='Continue']").click()


def login_via_ui(driver, email, password):
    """Fill and submit the Returning Customer login form (F2)."""
    open_route(driver, "account/login")
    type_into(driver, "#input-email", email)
    type_into(driver, "#input-password", password)
    driver.find_element(By.CSS_SELECTOR, "#content input[type='submit'][value='Login']").click()


def add_product_to_cart(driver, product_id, qty):
    """Open a product page, set the quantity box and click Add to Cart (F10)."""
    open_route(driver, f"product/product&product_id={product_id}")
    qty_box = wait_visible(driver, "#entry_216841 input[name='quantity']")
    qty_box.clear()                 # remove the default value of 1
    qty_box.send_keys(str(qty))     # type the quantity under test
    toasts_before = len(driver.find_elements(By.CSS_SELECTOR, "#notification-box-top .toast"))
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, "#entry_216842 button.button-cart"))
    return wait_new_toast(driver, toasts_before)


def wait_new_toast(driver, count_before):
    """Wait for a NEW pop up notification to appear and return its text."""
    sel = "#notification-box-top .toast"
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, sel)) > count_before
    )
    toast = driver.find_elements(By.CSS_SELECTOR, sel)[-1]
    # textContent keeps the sentence on one line (.text splits it around the links),
    # then collapse the extra spaces/newlines: "Success: You have added iPhone to your shopping cart!"
    raw = driver.execute_script("return arguments[0].textContent;", toast)
    return " ".join(raw.split())
