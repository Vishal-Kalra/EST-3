"""
Shared helpers for Prithvi's Assignment 3 tests.

Site under test: Abstracta OpenCart demo store (https://opencart.abstracta.us)
Functions covered: F1 User Registration, F2 User Login, F3 Forgotten Password
"""
import os
import random
import time
from pathlib import Path

# Base address of the website. It can be overridden with the A3_BASE_URL
# environment variable, but normally you leave it as the live demo store.
BASE_URL = os.environ.get("A3_BASE_URL", "https://opencart.abstracta.us")

# The three pages under test (these are the URLs listed in Section 2 of the report)
REGISTER_URL = f"{BASE_URL}/index.php?route=account/register"
LOGIN_URL = f"{BASE_URL}/index.php?route=account/login"
FORGOTTEN_URL = f"{BASE_URL}/index.php?route=account/forgotten"

# Test data used across the scenarios (test-only values, not real accounts)
FIRST_NAME = "Prithvi"
LAST_NAME = "Tester"
TELEPHONE = "0412345678"
PASSWORD = "Test@12345"

# Every screenshot is saved into this folder, named by test case and scenario
SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)


def unique_email() -> str:
    """Build a new email address for every run.

    The site refuses an email that is already registered, so a fixed address
    would make the successful-registration test fail on the second run.
    A millisecond timestamp plus a random number keeps every address unique.
    example.com is a reserved domain, so no real person receives these emails.
    """
    return f"prithvi.a3.{int(time.time() * 1000)}{random.randint(100, 999)}@example.com"


def snap(page, name: str) -> None:
    """Save a full-page screenshot, e.g. screenshots/T001_S1_2_result.png."""
    page.screenshot(path=str(SCREENSHOT_DIR / f"{name}.png"), full_page=True)


def fill_registration_form(page, email: str, password: str, confirm: str, agree: bool = True) -> None:
    """Fill in every field on the Register Account page (does not submit)."""
    page.fill("#input-firstname", FIRST_NAME)   # First Name
    page.fill("#input-lastname", LAST_NAME)     # Last Name
    page.fill("#input-email", email)            # E-Mail
    page.fill("#input-telephone", TELEPHONE)    # Telephone
    page.fill("#input-password", password)      # Password
    page.fill("#input-confirm", confirm)        # Password Confirm
    if agree:
        # Tick "I have read and agree to the Privacy Policy".
        # The checkbox has no id on this site, so we find it by its name.
        page.check("#content form input[name='agree']")


def submit_registration(page) -> None:
    """Click the Continue button at the bottom of the Register Account form."""
    page.locator("#content form input[type='submit'][value='Continue']").click()
    page.wait_for_load_state()
