import time

from behave import then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils import cart_rows, clear_field, click_button, find, page_text, totals, type_into


def _row(context, name):
    for row in cart_rows(context):
        if row["name"] == name:
            return row
    raise AssertionError(f'"{name}" is not in the cart')


@then('the line total for "{name}" should be {amount:d}')
def line_total(context, name, amount):
    actual = _row(context, name)["line_total"]
    assert actual == amount, f"Line total for {name} is {actual}, expected {amount}"


@then("the subtotal should be {amount:d}")
def subtotal(context, amount):
    time.sleep(0.5)
    actual = totals(context).get("Subtotal")
    assert actual == amount, f"Subtotal is {actual}, expected {amount}"


@when('I change the quantity of "{name}" to {qty:d}')
def change_qty(context, name, qty):
    field = find(context, By.CSS_SELECTOR, f'input[aria-label="Quantity for {name}"]')
    clear_field(field)
    field.send_keys(str(qty), Keys.TAB)
    time.sleep(0.5)


@when('I remove "{name}" from the cart')
def remove_item(context, name):
    _row(context, name)["row"].find_element(By.XPATH, ".//button[normalize-space()='Remove']").click()
    time.sleep(0.5)


@then('the cart should not contain "{name}"')
def not_in_cart(context, name):
    names = [r["name"] for r in cart_rows(context)]
    assert name not in names, f'"{name}" is still in the cart: {names}'


@then('the cart should contain "{name}"')
def in_cart(context, name):
    names = [r["name"] for r in cart_rows(context)]
    assert name in names, f'"{name}" is missing from the cart: {names}'


@when('I apply the promo code "{code}"')
def apply_code(context, code):
    type_into(context, "promo", code)
    click_button(context, "Apply code")
    time.sleep(0.5)


@then("the discount should be 10 percent of the subtotal")
def ten_percent(context):
    t = totals(context)
    discount = next((abs(v) for k, v in t.items() if k.startswith("Discount")), None)
    assert discount is not None, f"No discount line shown: {t}"
    expected = round(t["Subtotal"] * 0.10, 2)
    assert abs(discount - expected) < 1, f"Discount is {discount}, expected {expected}"


@then('the cart page should not show the "{symbol}" symbol')
def no_symbol(context, symbol):
    assert symbol not in page_text(context), f'Cart page shows "{symbol}"'
