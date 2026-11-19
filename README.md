# Kettleworks UI automation (Python + Selenium + Behave + Allure)

Simple BDD suite for https://interview-qa-task.vercel.app.
Each scenario is tagged with its test case ID (`@TC-xx`) from the "Test Cases" sheet,
and with the bug ID (`@BUG-xx`, `@LBUG-xx`, `@ABUG-xx`) it is expected to catch.
Scenarios that check a known bug are written for the CORRECT behaviour, so they FAIL until the bug is fixed.

## Folder structure

```
kettleworks-bdd/
├── config.py              # URL, test accounts, headless, timeout (override with env variables)
├── utils.py               # small helper functions (find, type, money, cart rows, login, ...)
├── behave.ini             # behave settings + html and allure formatters
├── requirements.txt
└── features/
    ├── environment.py       # start Chrome, clear localStorage before each scenario, screenshot on failure
    ├── 01_shop.feature      # search, filter, sort, pagination
    ├── 02_product.feature   # add to cart, stock/qty checks, modal, reviews
    ├── 03_cart.feature      # totals, qty change, remove, promo, currency
    ├── 04_checkout.feature  # place order, field validation, Enter key, double submit
    ├── 05_auth.feature      # sign in, sign out, protected pages
    ├── 06_admin.feature     # admin access, stock value, restock
    └── steps/               # one step file per feature + common_steps.py
```

Feature files are numbered because behave runs them in alphabetical order.

## Setup (one time)

```bash
git clone https://github.com/<your-username>/kettleworks-bdd.git
cd kettleworks-bdd
python -m venv .venv
.venv\Scripts\activate            # Windows   (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```
Google Chrome must be installed. Selenium downloads the matching driver by itself.
`requirements.txt` includes `allure-behave`, so the Allure formatter is installed with the other packages.

## Run

```bash
behave -f progress                       # everything
behave --tags=@smoke                     # quick smoke run (should all pass)
behave --tags=@TC-25                     # one test case
behave --tags=@BUG-12                    # all checks for one bug
behave features/03_cart.feature          # one feature file
behave -f html -o reports/report.html    # simple HTML report
behave --junit --junit-directory reports/junit   # JUnit XML for CI
```

Headless or another account (Windows PowerShell):
```bash
$env:HEADLESS="1"
$env:CUSTOMER_EMAIL="someone@yopmail.com"
$env:CUSTOMER_PASSWORD="India1@1"
behave -f progress
```

Screenshots of failed steps are saved in `reports/screenshots/`.

## Allure report

### One-time setup
Allure needs Java 8 or later (check with `java -version`; install Temurin JDK 17 from adoptium.net if missing).

Install the Allure command line tool (pick one):
```bash
npm install -g allure-commandline
scoop install allure
```
Check: `allure --version`

### Run tests and open the report
```bash
# Windows PowerShell: clear old results first so runs don't mix
Remove-Item -Recurse -Force reports\allure-results -ErrorAction SilentlyContinue

behave -f allure -o reports/allure-results -f progress
allure serve reports/allure-results
```
`allure serve` builds the report and opens it in the browser.

### Save the report as a folder (to share)
```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### What the report shows
- Pass / fail summary and charts
- Each feature, scenario and step with timings
- Tags: `@TC-xx` (test case) and `@BUG-xx` / `@LBUG-xx` / `@ABUG-xx` (bug it catches)
- Screenshot attached to every failed step

## Notes

- The app keeps cart, orders, reviews and the signed-in user in the browser's localStorage,
  so `environment.py` clears it before every scenario and `set_cart()` fills the cart directly for fast setup.
- Expected answers (category, stock, price) come from `GET /api/products`, so tests don't hard-code product data.
- Scenarios tagged with a bug ID are expected to fail until that bug is fixed.
