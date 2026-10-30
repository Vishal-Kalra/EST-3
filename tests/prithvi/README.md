# Assignment 3 – Prithvi's system tests

Automated tests for three functions of the Abstracta OpenCart demo store
(https://opencart.abstracta.us):

| Test case | Function | File | Scenarios |
|---|---|---|---|
| T001 | F1 User Registration | `tests/test_t001_registration.py` | valid registration · email already registered · passwords don't match |
| T002 | F2 User Login | `tests/test_t002_login.py` | valid login · wrong password · empty fields |
| T003 | F3 Forgotten Password | `tests/test_t003_forgotten_password.py` | registered email · unregistered email · empty email |

Stack: Python 3 · pytest · Playwright for Python · Chromium · pytest-html

## Setup (once)

1. Install Python 3.10 or newer from https://www.python.org/downloads/
   (on Windows, tick **"Add python.exe to PATH"** during install).
2. Open a terminal in this folder (`a3-prithvi-tests`).
3. Create and activate a virtual environment:
   - macOS / Linux
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell)
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
4. Install the libraries and the browser:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## Run the tests

```bash
pytest
```

This runs all 9 scenarios and creates:

- `screenshots/` – two screenshots per scenario (`T001_S1_1_form_filled.png`, `T001_S1_2_result.png`, …). These go in the Test Results row of each test case.
- `report.html` – one page listing all 9 results as PASSED / FAILED / ERROR. A screenshot of it works well as a results summary.
- `test-results/` – an extra screenshot for any test that fails.

To watch the browser while it runs (handy for a screen recording):

```bash
pytest --headed --slowmo 500
```

To run just one test case:

```bash
pytest tests/test_t002_login.py
```

## Notes

- Every run registers a fresh account with an `@example.com` address, so the tests don't clash with earlier runs.
- Login and Forgotten Password need an existing account. `tests/conftest.py` registers one at the start of each run (Login and Forgotten Password depend on Registration).
- The wrong-password test only fails a login once. The site locks an account for about an hour after ~5 failed attempts, so don't change it to loop.
- If a test fails because the site's wording is slightly different, open the failure screenshot in `test-results/`, then update the expected text near the top of that test file.

## Put it on GitHub

```bash
git init
git add .
git commit -m "Assignment 3 tests: registration, login, forgotten password"
git branch -M main
git remote add origin https://github.com/<your-username>/a3-system-tests.git
git push -u origin main
```

A `.gitignore` is included so the virtual environment and generated files stay out of the repo.
