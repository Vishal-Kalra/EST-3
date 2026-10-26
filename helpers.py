"""
Small reusable helpers so each test file stays short and readable.
Every locator below was checked against the live site in October 2026.
"""
import re
import time

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Every page on the site is index.php?route=<something>
BASE_URL = "https://opencart.abstracta.us/index.php?route="
TIMEOUT = 30  # seconds; the demo store can be slow at peak times


def open_route(driver, route):
    """Open a page by its OpenCart route, e.g. open_route(driver, 'account/login')."""
    driver.get(BASE_URL + route)
    wait_page_ready(driver)


def wait_page_ready(driver):
    """
    Wait until the page has fully loaded and jQuery has no AJAX calls running.
    Buttons such as Add to Cart only work once the page scripts are attached.
    """
    WebDriverWait(driver, TIMEOUT).until(lambda d: d.execute_script(
        "return document.readyState === 'complete' && "
        "(typeof jQuery === 'undefined' || jQuery.active === 0);"))


def wait_visible(driver, css):
    """Wait until an element is visible and return it."""
    return WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, css))
    )


def wait_clickable(driver, css):
    """Wait until an element is visible and enabled, then return it."""
    return WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css))
    )


def first_visible(driver, css):
    """
    Some controls can appear more than once on a page (one copy hidden).
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
    """Click with JavaScript, for elements that a normal click cannot reach."""
    driver.execute_script("arguments[0].click();", element)


def safe_click(driver, element):
    """
    Scroll the element to the middle of the screen, then click it. If something
    (a sticky bar, a loading overlay) still covers it, fall back to a JavaScript click.
    """
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.click()
    except ElementClickInterceptedException:
        js_click(driver, element)


def page_text(driver):
    """All visible text on the page."""
    return driver.find_element(By.TAG_NAME, "body").text


def wait_for_message(driver, text):
    """Wait until a success/warning/error message with this exact text is visible anywhere on the page."""
    wait_for_text(driver, "body", text)


def wait_for_text(driver, css, text):
    """Wait until the given text appears inside the element."""
    WebDriverWait(driver, TIMEOUT).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, css), text)
    )


def clear_alerts(driver):
    """Remove old alert banners so the next wait only sees the new one."""
    driver.execute_script("document.querySelectorAll('.alert-dismissible').forEach(a => a.remove());")


# Records the message the store sends back after an AJAX action (add to cart, wishlist, compare).
# This is the same text the site puts in its alert banner, so the test still checks what the user sees,
# but it does not depend on the banner still being on screen when Selenium looks for it.
_LISTEN_JS = """
window._storeMsg = null;
jQuery(document).off('ajaxComplete.qa').on('ajaxComplete.qa', function (e, xhr) {
    try {
        var j = JSON.parse(xhr.responseText);
        if (j.success) { window._storeMsg = j.success; }
        else if (j.error) { window._storeMsg = (typeof j.error === 'string') ? j.error : JSON.stringify(j.error); }
    } catch (err) { /* not a JSON response, ignore */ }
});
"""


def _clean(text):
    """Strip HTML tags, the close 'x' and extra spaces from a message."""
    text = re.sub(r"<[^>]+>", "", text or "")
    return " ".join(text.replace("\u00d7", "").split())


def wait_new_alert(driver):
    """Wait for the store's reply to the last action and return the message text."""
    def _message(d):
        for el in d.find_elements(By.CSS_SELECTOR, ".alert-dismissible"):
            if el.is_displayed():                       # banner on screen: read it directly
                return d.execute_script("return arguments[0].textContent;", el)
        return d.execute_script("return window._storeMsg;")  # banner already gone: use the reply
    return _clean(WebDriverWait(driver, TIMEOUT).until(_message))


def click_and_get_alert(driver, element):
    """Click a button that shows an alert banner (wishlist / compare / cart) and return its text."""
    wait_page_ready(driver)          # make sure the button's click handler is attached
    clear_alerts(driver)
    driver.execute_script(_LISTEN_JS)
    safe_click(driver, element)
    return wait_new_alert(driver)


def click_when_settled(driver, css):
    """
    Wait for any loading to finish, then click the element with JavaScript.
    Used on the checkout accordion, where panels slide open and a normal click
    can land on a panel heading instead of the intended button.
    """
    wait_page_ready(driver)
    element = wait_clickable(driver, css)
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: not d.find_elements(By.CSS_SELECTOR, ".collapsing"))   # no panel mid-animation
    js_click(driver, element)
    wait_page_ready(driver)


def cart_count(driver):
    """
    Number of items shown on the header cart button, e.g. '2 item(s) - $246.40' -> 2.
    The header refreshes a moment after the alert appears, so give it a short pause first.
    """
    time.sleep(1)
    text = driver.find_element(By.ID, "cart-total").text
    return int(re.match(r"\s*(-?\d+)", text).group(1))


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
        js_click(driver, driver.find_element(By.NAME, "agree"))  # tick Privacy Policy
    driver.find_element(By.CSS_SELECTOR, "#content input[type='submit'][value='Continue']").click()


def login_via_ui(driver, email, password):
    """Fill and submit the Returning Customer login form (F2)."""
    open_route(driver, "account/login")
    type_into(driver, "#input-email", email)
    type_into(driver, "#input-password", password)
    driver.find_element(By.CSS_SELECTOR, "#content input[type='submit'][value='Login']").click()


def add_product_to_cart(driver, product_id, qty):
    """Open a product page, set the quantity box and click Add to Cart (F10). Returns the alert text."""
    open_route(driver, f"product/product&product_id={product_id}")
    qty_box = wait_visible(driver, "#input-quantity")
    qty_box.clear()                 # remove the default value of 1
    qty_box.send_keys(str(qty))     # type the quantity under test
    return click_and_get_alert(driver, driver.find_element(By.ID, "button-cart"))


# older name kept so existing test files keep working
click_and_get_toast = click_and_get_alert
