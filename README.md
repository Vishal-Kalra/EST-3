# EST Assignment 3: System Test (starter project)

Automated system tests for the OpenCart demo store:
https://opencart.abstracta.us

Stack: **Python + Selenium WebDriver + pytest**, running in Google Chrome.

---

## Start

You need **Python 3.9+**, **Google Chrome** and **VS Code** installed (see One time setup below).

```bash
./run_tests.sh vishal        
```

* a PASS / FAIL summary in the terminal
* a screenshot of every scenario in `screenshots/`

Run `./run_tests.sh` (or `run_tests.bat`) with no name to run the whole group's tests.

---

## One time setup

* **Python 3.9 or newer**: https://www.python.org/downloads/ (Windows: tick **"Add Python to PATH"** in the installer)
* **Google Chrome** (normal version)
* **VS Code** (recommended) with the **Python** extension, or PyCharm

### Steps

**macOS (Terminal)**
```bash
cd path/to/EST_3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Check it works
```bash
pytest tests/vishal/test_T10_add_to_cart.py
```
---

## How to write a test (read this once)

Each scenario is one function. Pattern:

```python
from selenium.webdriver.common.by import By
from helpers import open_route, type_into, wait_for_message


def test_T06_S1_send_valid_enquiry(driver):          # driver = fresh Chrome, given automatically
    # Input: valid name, email and enquiry
    open_route(driver, "information/contact")         # opens ...index.php?route=information/contact
    type_into(driver, "#input-name", "Alex Tester")   # clear the field and type
    type_into(driver, "#input-email", "alex@mailinator.com")
    type_into(driver, "#input-enquiry", "Hello, what is the delivery time to Sydney?")
    driver.find_element(By.CSS_SELECTOR, "#content input[type='submit']").click()
    # Expected: success message
    wait_for_message(driver, "Your enquiry has been successfully sent to the store owner!")
    assert "contact/success" in driver.current_url
```

Rules we all follow so marks are safe:
* **3 scenarios per test case**, at least one success and one failure input.
* Comment on each step: `# Input: ...` and `# Expected: ...` (the rubric wants clear comments).
* Write the **expected result from what the site SHOULD do**, not what it does. If the site is wrong, the test fails, and that's a defect to write up, not a broken test.
* Every scenario gets a fresh browser, so never rely on another scenario having run first.

### Helpers you can use (in `helpers.py`)

| Helper | What it does |
|---|---|
| `open_route(driver, "account/login")` | Opens a page by its route |
| `type_into(driver, "#input-email", "x")` | Waits for a field, clears it, types |
| `wait_visible(driver, "css")` | Waits for an element to show and returns it |
| `first_visible(driver, "css")` | Returns the first element that is actually visible |
| `safe_click(driver, element)` | Scrolls to the element and clicks; falls back to a JS click if something covers it. Use this for normal buttons |
| `js_click(driver, element)` | Click via JavaScript. Use when a normal click is blocked |
| `wait_for_message(driver, "text")` | Waits until that exact text appears anywhere on the page |
| `page_text(driver)` | All visible text on the page |
| `unique_email("reg")` | A never used email like `reg.1729.....@mailinator.com` |
| `register_via_ui(...)` / `login_via_ui(driver, email, pw)` | Register / log in through the real forms |
| `add_product_to_cart(driver, product_id, qty)` | Adds a product, returns the green banner text |
| `click_and_get_alert(driver, button)` | Clicks a button that shows a green banner (wishlist, compare) and returns its text |
| `cart_count(driver)` | Number of items shown on the header cart button |
| `click_when_settled(driver, "css")` | Waits for loading to finish, then clicks (good for the checkout steps) |


---

## Project layout

```
EST_3/
  conftest.py          fresh Chrome per scenario, shared test account, auto screenshots
  helpers.py           shared actions and waits
  pytest.ini           pytest settings
  requirements.txt     selenium, pytest, pytest-html
  run_tests.sh         one command setup + run (Mac)
  run_tests.bat        one command setup + run (Windows)
  screenshots/         filled automatically when tests run
  tests/
    vishal/            T10, T11, T12 (finished examples)
    prithvi/           T01, T02, T03
    mihir/             T04, T05, T13
    jasmine/           T07, T08, T09
    mrunal/            T06, T14, T15
```
