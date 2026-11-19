"""Small helper functions shared by all step files.

Kept as plain functions (no page-object classes) so the project stays simple.
Every function takes behave's `context`, which holds the WebDriver as context.driver.
"""
import json
import re
import time

import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

import config


# ---------- navigation & waiting ----------

def go(context, path="/"):
    context.driver.get(config.BASE_URL + path)


def wait(context, timeout=None):
    return WebDriverWait(context.driver, timeout or config.TIMEOUT)


def find(context, by, value):
    return wait(context).until(EC.visibility_of_element_located((by, value)))


def find_all(context, css):
    return context.driver.find_elements(By.CSS_SELECTOR, css)


def button(context, text):
    xpath = f"//button[normalize-space()='{text}']"
    return wait(context).until(EC.element_to_be_clickable((By.XPATH, xpath)))


def click_button(context, text):
    button(context, text).click()


def page_text(context):
    return context.driver.find_element(By.TAG_NAME, "main").text


def current_path(context):
    return context.driver.current_url.replace(config.BASE_URL, "") or "/"


# ---------- typing ----------

def clear_field(element):
    """React inputs ignore element.clear(), so select all and delete instead."""
    element.click()
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(Keys.BACKSPACE)
    if element.get_attribute("value"):          # macOS uses Command instead of Control
        element.send_keys(Keys.COMMAND, "a")
        element.send_keys(Keys.BACKSPACE)


def type_into(context, element_id, text):
    element = find(context, By.ID, element_id)
    clear_field(element)
    element.send_keys(text)
    return element


def select_option(context, element_id, visible_text):
    Select(find(context, By.ID, element_id)).select_by_visible_text(visible_text)


# ---------- money & toasts ----------

def money(text):
    """'₹2,450' / '$740' / '-₹367.00' -> float"""
    cleaned = re.sub(r"[^\d.\-]", "", text)
    return float(cleaned) if cleaned else 0.0


def wait_for_toast(context, text, timeout=None):
    try:
        wait(context, timeout).until(
            lambda d: any(text in t.text for t in d.find_elements(By.CSS_SELECTOR, ".toast"))
        )
        return True
    except TimeoutException:
        return False


def visible_toasts(context):
    return [t.text for t in find_all(context, ".toast") if t.is_displayed()]


# ---------- browser storage (the app keeps cart, orders and user in localStorage) ----------

def read_storage(context, key):
    raw = context.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)
    return json.loads(raw) if raw else None


def set_cart(context, items):
    """items: list of {"id": "kw-201", "qty": 2}. Fast setup without clicking through pages."""
    go(context, "/")
    context.driver.execute_script(
        "window.localStorage.setItem('kw.cart', arguments[0]);", json.dumps(items)
    )


# ---------- product data from the API (used to know the correct answers) ----------

_products_cache = None


def api_products():
    global _products_cache
    if _products_cache is None:
        response = requests.get(config.BASE_URL + "/api/products", timeout=15)
        response.raise_for_status()
        _products_cache = response.json()["products"]
    return _products_cache


def product_by_name(name):
    return next(p for p in api_products() if p["name"] == name)


# ---------- shop page ----------

def wait_for_products(context):
    wait(context).until(lambda d: d.find_elements(By.CSS_SELECTOR, "article.card"))


def listed_names(context):
    return [a.text for a in find_all(context, "article.card h3 a")]


def listed_prices(context):
    return [money(p.text) for p in find_all(context, "article.card .price")]


def all_listed_names(context):
    """Click Next until the last page and return every product name seen."""
    names = listed_names(context)
    while button(context, "Next").is_enabled():
        click_button(context, "Next")
        time.sleep(0.3)
        names += listed_names(context)
    return names


# ---------- cart page ----------

def cart_rows(context):
    rows = []
    for tr in find_all(context, "table.table tbody tr"):
        cells = tr.find_elements(By.TAG_NAME, "td")
        rows.append({
            "name": cells[0].find_element(By.TAG_NAME, "a").text,
            "qty": int(cells[1].find_element(By.TAG_NAME, "input").get_attribute("value") or 0),
            "line_total": money(cells[2].text),
            "row": tr,
        })
    return rows


def totals(context):
    """Returns {'Subtotal': 1220.0, 'GST at 18%': 219.0, 'Total': ...} from the totals box."""
    result = {}
    for line in find_all(context, ".totals > div"):
        spans = line.find_elements(By.TAG_NAME, "span")
        if len(spans) >= 2:
            result[spans[0].text.strip()] = money(spans[1].text)
    return result


def badge_count(context):
    return int(find(context, By.CSS_SELECTOR, "header .badge").text or 0)


# ---------- login ----------

def login(context, email, password):
    go(context, "/login")
    type_into(context, "email", email)
    type_into(context, "password", password)
    click_button(context, "Sign in")
    button(context, "Sign out")          # waits until the header shows Sign out


# ---------- checkout ----------

VALID_CUSTOMER = {
    "fullName": "Amir Khan",
    "email": "amir.test@yopmail.com",
    "phone": "9876543210",
    "address": "12 Anna Salai",
    "city": "Chennai",
    "pincode": "600002",
}


def fill_checkout(context, overrides=None):
    data = dict(VALID_CUSTOMER, **(overrides or {}))
    for field_id, value in data.items():
        type_into(context, field_id, value)
    return data
