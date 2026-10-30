"""
T002 - F2 User Login
Tester: Prithvi
URL: https://opencart.abstracta.us/index.php?route=account/login
Depends on: F1 User Registration (the account is created by the registered_account fixture)

Scenario 1 (success): log in with the registered email and the correct password
Scenario 2 (failure): log in with the registered email and a wrong password
Scenario 3 (failure): click Login with both fields left empty
"""
import re

from playwright.sync_api import expect

from helpers import LOGIN_URL, snap

LOGIN_ERROR = "No match for E-Mail Address and/or Password"


def fill_login(page, email: str, password: str) -> None:
    """Type the email and password into the Returning Customer form (does not submit)."""
    page.fill("#input-email", email)        # E-Mail Address field
    page.fill("#input-password", password)  # Password field


def click_login(page) -> None:
    """Click the Login button under the Returning Customer form."""
    page.locator("#content form input[type='submit'][value='Login']").click()
    page.wait_for_load_state()


def test_T002_S1_valid_login(page, registered_account):
    """S1: correct email + correct password -> My Account page."""
    page.goto(LOGIN_URL)                                                        # Step 1: open the Login page
    fill_login(page, registered_account["email"], registered_account["password"])   # Steps 2-3
    snap(page, "T002_S1_1_form_filled")

    click_login(page)                                                           # Step 4: click Login
    snap(page, "T002_S1_2_result")

    # Expected: redirected to the customer's My Account page
    expect(page).to_have_url(re.compile(r"route=account/account"))
    expect(page.locator("#content")).to_contain_text("My Account")


def test_T002_S2_wrong_password(page, registered_account):
    """S2: correct email + wrong password -> login refused.

    Only ONE wrong attempt is made. The site locks an account for an hour
    after about 5 failed logins, which would break later runs.
    """
    page.goto(LOGIN_URL)                                              # Step 1
    fill_login(page, registered_account["email"], "WrongPass@000")        # Steps 2-3
    snap(page, "T002_S2_1_form_filled")

    click_login(page)                                                 # Step 4
    snap(page, "T002_S2_2_result")

    # Expected: stay on the Login page with a red warning
    expect(page).to_have_url(re.compile(r"route=account/login"))
    expect(page.locator(".alert-danger")).to_contain_text(LOGIN_ERROR)


def test_T002_S3_empty_fields(page):
    """S3: both fields empty -> login refused."""
    page.goto(LOGIN_URL)                     # Step 1
    fill_login(page, "", "")                      # Steps 2-3: leave both fields blank
    snap(page, "T002_S3_1_form_empty")

    click_login(page)                        # Step 4
    snap(page, "T002_S3_2_result")

    # Expected: same warning as a wrong password; the user is not logged in
    expect(page).to_have_url(re.compile(r"route=account/login"))
    expect(page.locator(".alert-danger")).to_contain_text(LOGIN_ERROR)
