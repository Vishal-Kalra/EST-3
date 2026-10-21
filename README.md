# EST Assignment 3: System Test (starter project)

Automated system tests for the LambdaTest eCommerce Playground:
https://ecommerce-playground.lambdatest.io

Stack: **Python + Selenium WebDriver + pytest**, running in Google Chrome.

Everyone uses this same project so our code looks the same and the report is easy to merge.

---

## Quick start (5 minutes)

You need **Python 3.10+**, **Google Chrome** and **VS Code** installed (details in section 2).

**macOS**: open Terminal in this folder and run:
```bash
./run_tests.sh vishal          # swap vishal for your name: prithvi, mihir, jasmine, mrunal
```

**Windows**: open Command Prompt in this folder and run:
```bat
run_tests.bat vishal
```

The first run creates a `.venv`, installs everything and runs that person's tests. After that, the same command just runs the tests. Chrome opens and clicks through the site by itself. When it finishes you get:
* a PASS / FAIL / SKIPPED summary in the terminal
* a screenshot of every scenario in `screenshots/`
* an HTML report in `report.html` (open it in your browser)

Run `./run_tests.sh` (or `run_tests.bat`) with no name to run the whole group's tests.

---

## 1. Who does what

| Member | SID | Test cases (your folder) | Group report section |
|---|---|---|---|
| Vishal Kalra | 25675962 | T10 Add to Cart, T11 Shopping Cart, T12 Guest Checkout (`tests/vishal`) **done, use as examples** | Overview, System Functions, final merge + submit |
| Prithvi Krishna Prasad | 25966060 | T01 Registration, T02 Login, T03 Forgotten Password (`tests/prithvi`) | Analysis and Reflections |
| Mihir Chauhan | 25620699 | T04 Edit Account, T05 Wish List, T13 Change Password (`tests/mihir`) | Test Team, Task Schedule + Gantt |
| Jasmine Joseph | 25729738 | T07 Product Search, T08 Category Sorting, T09 Product Compare (`tests/jasmine`) | Test Environments |
| Mrunal Ghag | 25717430 | T06 Contact Us, T14 Product Review, T15 Newsletter (`tests/mrunal`) | Week 12 presentation slides |

Your 3 test files are already created in your folder with the scenario names, suggested inputs and expected outputs. You just write the steps.

**Deadlines:** tests done **22 Oct**, report section done **27 Oct**, final submission **31 Oct** (due 1 Nov).

---

## 2. One time setup (about 10 minutes)

### You need
* **Python 3.10 or newer**: https://www.python.org/downloads/ (Windows: tick **"Add Python to PATH"** in the installer)
* **Google Chrome** (normal version)
* **VS Code** (recommended) with the **Python** extension, or PyCharm

### Steps

**macOS (Terminal)**
```bash
cd path/to/EST_A3_System_Test
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (Command Prompt or PowerShell)**
```bat
cd path\to\EST_A3_System_Test
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

You do **not** need to download chromedriver. Selenium downloads the right one automatically the first time you run a test.

### Open it in VS Code
1. **File > Open Folder** and pick this project folder (or run `code .` in the terminal here).
2. Install the **Python** extension if VS Code suggests it (bottom right pop up).
3. Press `Cmd + Shift + P` (Mac) or `Ctrl + Shift + P` (Windows) > **Python: Select Interpreter** > pick the one that shows `.venv` (VS Code usually picks it automatically once `.venv` exists).
4. Open the **Testing** panel (the beaker icon on the left bar). If it asks, click **Configure Python Tests** > **pytest** > **tests**. All tests show up there grouped by folder. Click the play button next to a file or a single scenario to run it, and the green tick / red cross shows the result.
5. To run in the VS Code terminal instead: **Terminal > New Terminal**, then `source .venv/bin/activate` (Mac) or `.venv\Scripts\activate` (Windows), then any `pytest` command from section 3.

### Check it works
```bash
pytest tests/vishal/test_T10_add_to_cart.py
```
Chrome opens, does things by itself, closes, and you see `3 passed` or `1 passed, 2 failed` (those 2 failures are real bugs on the site, that's expected).

---

## 3. Running tests

Easiest: `./run_tests.sh <yourname>` (Mac) or `run_tests.bat <yourname>` (Windows), see Quick start.

Or with the `.venv` activated, run pytest directly:

```bash
pytest tests/<yourname>                    # only your 3 test cases
pytest tests/<yourname>/test_T07_product_search.py   # one file
pytest tests/<yourname> -k S2              # only scenario 2 of each file
pytest                                     # everything (whole group)
pytest tests/<yourname> --html=report.html --self-contained-html   # HTML report
```

Run without opening a browser window: macOS `HEADLESS=1 pytest tests/<yourname>`, Windows `set HEADLESS=1` then `pytest tests/<yourname>`.

**Screenshots are automatic.** After every scenario, a screenshot is saved to `screenshots/` named like `test_T07_S1_search_existing_keyword_PASS.png`. Use these in the report.

Before your files are finished, unfinished scenarios show as **SKIPPED**. That's fine.

---

## 4. How to write a test (read this once)

Each scenario is one function. Pattern:

```python
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
| `first_visible(driver, "css")` | Returns the **visible** copy (the site has hidden duplicates of many buttons) |
| `safe_click(driver, element)` | Scrolls to the element and clicks; falls back to a JS click if something covers it. Use this for normal buttons |
| `js_click(driver, element)` | Click via JavaScript. Use for the site's custom checkboxes/radios (e.g. Privacy Policy, Terms) |
| `wait_for_message(driver, "text")` | Waits until that exact text appears anywhere on the page |
| `page_text(driver)` | All visible text on the page |
| `unique_email("reg")` | A never used email like `reg.1729.....@mailinator.com` |
| `register_via_ui(...)` / `login_via_ui(driver, email, pw)` | Register / log in through the real forms |
| `add_product_to_cart(driver, product_id, qty)` | Adds a product, returns the pop up text |
| `click_and_get_toast(driver, button)` | Clicks a button that shows a pop up (wishlist, compare) and returns its text |
| `cart_badge(driver)` | Number on the header cart icon |

### Fixtures (just add them as function arguments)
* `driver`: a fresh Chrome window, closed automatically after the scenario.
* `registered_user`: an account created once per run through the real register form. Use `registered_user["email"]` and `registered_user["password"]` when you need to log in.

### Finding locators
Right click the element in Chrome > **Inspect**. Prefer `id` (`#input-email`), then `name`, then a short CSS selector. Things that tripped us up on this site:
* Many buttons exist twice (desktop + hidden mobile). Use `first_visible`.
* Checkboxes/radios are hidden under styled labels, and labels contain links. Use `js_click` on the `<input>` by id.
* Success/error banners are sometimes outside `#content`, so use `wait_for_message`, which checks the whole page.
* On search and category pages the products live in `#container .product-layout`, not `#content`.

### Useful product ids (no options, easy to add to cart)
`40` iPhone, `43` MacBook, `28` HTC Touch HD, `29` Palm Treo Pro, `33` Samsung SyncMaster 941BW

---

## 5. What goes in the report (for each of your 3 test cases)

Copy the test case table from the template and fill:
1. **Test Case ID** (e.g. T07) and **Function ID/Name** (e.g. F7 Product Search)
2. **Tester**: your name
3. **Test Scenario 1, 2, 3**: numbered steps with the URL, the data typed, and the expected output
4. **Test Results**: for each scenario, expected vs actual and PASS/FAIL, plus the screenshots from `screenshots/`
5. **Screenshot of your source code** for that test case (VS Code, zoom so it is readable)

Also send Vishal: your **UTS email**, **laptop + CPU** (Apple M1/M2/M3 = Arm, Intel/AMD = x86), **OS**, **editor**, and **tutorial code**.

---

## 6. Submitting your code (individual)

When your 3 files are done and run:
```bash
python make_submission.py <yourname>      # e.g. python make_submission.py jasmine
```
This creates `<SID>_<Name>_A3_code.zip` with the shared files and only your tests. Upload that zip to Canvas under Assignment 3. It warns you if any scenario is still `pytest.skip`.

---

## 7. Project layout

```
EST_A3_System_Test/
  conftest.py          fresh Chrome per scenario, shared test account, auto screenshots
  helpers.py           shared actions and waits
  pytest.ini           pytest settings
  requirements.txt     selenium, pytest, pytest-html
  make_submission.py   builds your Canvas zip
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

## 8. Stuck?
* `ModuleNotFoundError: selenium`: your `.venv` isn't activated. Run the activate line again.
* `./run_tests.sh: Permission denied` (Mac): run `chmod +x run_tests.sh` once.
* `python3: command not found` / `python is not recognized`: install Python from python.org (Windows: tick "Add Python to PATH").
* Tests don't show in the VS Code Testing panel: select the `.venv` interpreter (section 2), then click the refresh icon in the Testing panel.
* `chromedriver` / session errors: update Chrome, then rerun.
* `TimeoutException`: the locator is wrong or the page is slow. Check it in Inspect, try `first_visible`.
* `ElementClickInterceptedException`: something is covering it. Use `safe_click` instead of `.click()`.
* `You may not select a disabled option` / element not interactable: the form is still reloading. Wait until the field `is_enabled()` first (see `start_guest_checkout` in tests/vishal/test_T12_guest_checkout.py).
* Still stuck: message the group chat with the error and your file.
