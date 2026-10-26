"""
Shared pytest fixtures for the Assignment 3 system tests.

Site under test: OpenCart demo store
https://opencart.abstracta.us

What lives here:
  * driver            -> a fresh Chrome browser for EVERY scenario (clean cookies, empty cart)
  * registered_user   -> one account created through the UI once per run (F1 must pass first)
  * screenshot hook   -> saves screenshots/<test name>.png after every scenario, pass or fail
"""
import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helpers import BASE_URL, register_via_ui, unique_email

# Folder where the evidence screenshots are written
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Shared test data for the account created in registered_user
DEFAULT_PASSWORD = "Test@1234"


def _new_chrome():
    """Start Chrome with a fixed desktop size so the desktop header and menus are shown."""
    options = Options()
    # Run headless only when HEADLESS=1 is set, so testers can watch the run by default
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")  # desktop layout, not the mobile menu
    options.add_argument("--disable-notifications")  # stop browser pop ups getting in the way
    # Selenium Manager (built into Selenium 4.6+) downloads the matching chromedriver automatically
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)  # we only use explicit waits, which are more reliable
    return drv


@pytest.fixture
def driver():
    """Fresh browser per scenario, so one scenario can never leak cart or login state into another."""
    drv = _new_chrome()
    drv.get(BASE_URL + "common/home")  # every scenario starts from the home page
    yield drv
    drv.quit()  # always close the browser, even if the scenario failed


@pytest.fixture(scope="session")
def registered_user():
    """
    Create ONE customer account through the real registration form (function F1).
    Login, edit account, wishlist and forgotten password tests depend on this account,
    which is exactly the F1 -> F2/F3/F4/F5 dependency described in Section 2 of the report.
    """
    drv = _new_chrome()
    email = unique_email("member")  # timestamped so it is never already registered
    register_via_ui(drv, "Alex", "Tester", email, "0412345678", DEFAULT_PASSWORD)
    drv.quit()
    return {"email": email, "password": DEFAULT_PASSWORD}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """After each scenario runs, save a screenshot named after the test (evidence for the report)."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":  # only after the test body, not setup/teardown
        drv = item.funcargs.get("driver")
        if drv is not None:
            status = "PASS" if report.passed else "FAIL"
            name = f"{item.name}_{status}.png"
            time.sleep(0.5)  # let toasts/alerts finish rendering before the capture
            drv.save_screenshot(os.path.join(SCREENSHOT_DIR, name))
