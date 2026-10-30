"""
T001 - F1 User Registration
Tester: Prithvi
URL: https://opencart.abstracta.us/index.php?route=account/register

Scenario 1 (success): register with valid details and a brand-new email
Scenario 2 (failure): register with an email that is already registered
Scenario 3 (failure): register with a Password Confirm that doesn't match the Password
"""
import re

from playwright.sync_api import expect

from helpers import PASSWORD, REGISTER_URL, fill_registration_form, snap, submit_registration, unique_email


def test_T001_S1_valid_registration(page):
    """S1: valid details + new email -> account is created."""
    email = unique_email()  # new address so the site can't reject it as a duplicate

    page.goto(REGISTER_URL)                                       # Step 1: open the Register page
    fill_registration_form(page, email, PASSWORD, PASSWORD)      # Steps 2-8: fill every field, tick Privacy Policy
    snap(page, "T001_S1_1_form_filled")                          # evidence: the completed form

    submit_registration(page)                                    # Step 9: click Continue
    snap(page, "T001_S1_2_result")                               # evidence: the page shown afterwards

    # Expected: redirected to the success page with a congratulations message.
    # (The page title is checked rather than the heading, because every
    # account page on this site has the same "Account" heading.)
    expect(page).to_have_url(re.compile(r"route=account/success"))
    expect(page).to_have_title("Your Account Has Been Created!")
    expect(page.locator("#content")).to_contain_text("Your new account has been successfully created!")


def test_T001_S2_duplicate_email(page, registered_account):
    """S2: an email that already has an account -> registration is refused."""
    existing_email = registered_account["email"]  # registered by the fixture in conftest.py

    page.goto(REGISTER_URL)                                             # Step 1
    fill_registration_form(page, existing_email, PASSWORD, PASSWORD)   # Steps 2-8, same email again
    snap(page, "T001_S2_1_form_filled")

    submit_registration(page)                                          # Step 9
    snap(page, "T001_S2_2_result")

    # Expected: stay on the Register page with a red warning about the email.
    # .alert-danger is the red warning box (green .alert-success boxes are
    # used for good news, so we check the colour-specific class).
    expect(page).to_have_url(re.compile(r"route=account/register"))
    expect(page.locator(".alert-danger")).to_contain_text("E-Mail Address is already registered")


def test_T001_S3_password_mismatch(page):
    """S3: Password and Password Confirm differ -> registration is refused."""
    email = unique_email()

    page.goto(REGISTER_URL)                                             # Step 1
    fill_registration_form(page, email, PASSWORD, "Different@999")     # Steps 2-8, confirm doesn't match
    snap(page, "T001_S3_1_form_filled")

    submit_registration(page)                                          # Step 9
    snap(page, "T001_S3_2_result")

    # Expected: stay on the Register page with an error under Password Confirm
    expect(page).to_have_url(re.compile(r"route=account/register"))
    expect(page.locator(".text-danger", has_text="Password confirmation does not match password")).to_be_visible()
