"""
pytest fixtures shared by all three test files.

Login (F2) and Forgotten Password (F3) both depend on Registration (F1):
you can only log in, or reset a password, for an account that exists.
So before those tests run, this fixture registers one fresh account
through the real Register page and hands its email/password to the tests.
"""
import re

import pytest
from playwright.sync_api import expect

from helpers import PASSWORD, REGISTER_URL, fill_registration_form, submit_registration, unique_email


@pytest.fixture(scope="session")
def registered_account(browser):
    """Register one new account per test run and return its login details."""
    email = unique_email()

    # Use a separate browser context so this setup doesn't leave
    # the tests themselves logged in.
    context = browser.new_context()
    page = context.new_page()

    page.goto(REGISTER_URL)
    fill_registration_form(page, email, PASSWORD, PASSWORD, agree=True)
    submit_registration(page)

    # If registration itself is broken, stop here with a clear message
    expect(page).to_have_url(re.compile(r"route=account/success"))

    context.close()
    return {"email": email, "password": PASSWORD}
