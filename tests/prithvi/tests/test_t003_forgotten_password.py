"""
T003 - F3 Forgotten Password
Tester: Prithvi
URL: https://opencart.abstracta.us/index.php?route=account/forgotten
Depends on: F1 User Registration (a registered email is needed for the success case)

Scenario 1 (success): request a reset link for a registered email
Scenario 2 (failure): request a reset link for an email that was never registered
Scenario 3 (failure): click Continue with the email field empty
"""
import re

from playwright.sync_api import expect

from helpers import FORGOTTEN_URL, snap, unique_email

NOT_FOUND = "E-Mail Address was not found in our records"


def request_reset(page, email: str) -> None:
    """Type the email (can be empty) on the Forgot Your Password page."""
    page.fill("#input-email", email)


def click_continue(page) -> None:
    """Click the Continue button on the Forgot Your Password page."""
    page.locator("#content form input[type='submit'][value='Continue']").click()
    page.wait_for_load_state()


def test_T003_S1_registered_email(page, registered_account):
    """S1: registered email -> confirmation that a reset link was emailed."""
    page.goto(FORGOTTEN_URL)                                # Step 1: open Forgot Your Password page
    request_reset(page, registered_account["email"])        # Step 2: enter the registered email
    snap(page, "T003_S1_1_form_filled")

    click_continue(page)                                    # Step 3: click Continue
    snap(page, "T003_S1_2_result")

    # Expected: sent back to the Login page with a green success message
    expect(page).to_have_url(re.compile(r"route=account/login"))
    expect(page.locator(".alert-success")).to_contain_text("confirmation link")


def test_T003_S2_unregistered_email(page):
    """S2: an email with no account -> request refused."""
    never_registered = unique_email()   # brand-new address, so it can't exist on the site

    page.goto(FORGOTTEN_URL)                     # Step 1
    request_reset(page, never_registered)        # Step 2
    snap(page, "T003_S2_1_form_filled")

    click_continue(page)                         # Step 3
    snap(page, "T003_S2_2_result")

    # Expected: stay on the same page with a red "not found" warning
    expect(page).to_have_url(re.compile(r"route=account/forgotten"))
    expect(page.locator(".alert-danger")).to_contain_text(NOT_FOUND)


def test_T003_S3_empty_email(page):
    """S3: empty email field -> request refused."""
    page.goto(FORGOTTEN_URL)          # Step 1
    request_reset(page, "")           # Step 2: leave the field blank
    snap(page, "T003_S3_1_form_empty")

    click_continue(page)              # Step 3
    snap(page, "T003_S3_2_result")

    # Expected: stay on the same page with the same "not found" warning
    expect(page).to_have_url(re.compile(r"route=account/forgotten"))
    expect(page.locator(".alert-danger")).to_contain_text(NOT_FOUND)
