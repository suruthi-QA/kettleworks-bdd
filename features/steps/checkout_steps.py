import re
import time

from behave import then, when
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils import button, fill_checkout, find, find_all, go, page_text, read_storage, type_into, wait


@when("I fill the checkout form with valid details")
def fill_valid(context):
    context.customer = fill_checkout(context)


@when('I change "{field}" to "{value}"')
def change_field(context, field, value):
    type_into(context, field, "   " if value == "SPACES" else value)


@when('I press Enter in the "{field}" field')
def press_enter(context, field):
    find(context, By.ID, field).send_keys(Keys.ENTER)


@when('I double click "{text}"')
def double_click(context, text):
    ActionChains(context.driver).double_click(button(context, text)).perform()


@then("I should see the order confirmation with a reference")
def confirmation(context):
    try:
        wait(context, 5).until(lambda d: "/order/" in d.current_url)
    except Exception:
        raise AssertionError("Order confirmation page did not open")
    match = re.search(r"KW\d+", page_text(context))
    assert match, "No order reference on the confirmation page"
    context.order_ref = match.group(0)


@then("the order should be listed on the Orders page")
def order_listed(context):
    go(context, "/orders")
    wait(context).until(lambda d: context.order_ref in page_text(context),
                        f"{context.order_ref} not on Orders page")


@then('I should see the field error "{text}"')
def field_error(context, text):
    wait(context).until(lambda d: any(text in e.text for e in find_all(context, ".field-error")),
                        f'Field error "{text}" not shown')


@then("the order should not be placed")
def not_placed(context):
    time.sleep(1.5)
    orders = read_storage(context, "kw.orders") or []
    assert "/order/" not in context.driver.current_url and not orders, \
        f"Order was placed with invalid data ({len(orders)} order(s) saved)"


@then("exactly {count:d} order should be saved")
def order_count(context, count):
    time.sleep(2)
    orders = read_storage(context, "kw.orders") or []
    assert len(orders) == count, f"{len(orders)} orders saved, expected {count}"
