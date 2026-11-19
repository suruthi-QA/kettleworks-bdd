"""Steps used by more than one feature file."""
import time

from behave import given, step, then, when
from selenium.webdriver.common.by import By

import config
from utils import (badge_count, button, click_button, find, go, login, page_text, set_cart,
                   wait, wait_for_products, wait_for_toast)


# ---------- opening pages ----------

@given("I am on the shop page")
def open_shop(context):
    go(context, "/")
    wait_for_products(context)


@given('I open the product "{product_id}"')
def open_product(context, product_id):
    go(context, f"/product/{product_id}")
    find(context, By.ID, "qty")


@given("my cart has these items")
def cart_has_items(context):
    set_cart(context, [{"id": row["id"], "qty": int(row["qty"])} for row in context.table])


@given("I am on the cart page")
def open_cart(context):
    go(context, "/cart")
    find(context, By.CSS_SELECTOR, "table.table")


@given("I am on the checkout page")
def open_checkout(context):
    go(context, "/checkout")
    find(context, By.ID, "fullName")


@given("I am on the sign in page")
def open_login(context):
    go(context, "/login")
    find(context, By.ID, "email")


@given("I am not signed in")
def not_signed_in(context):
    # localStorage is cleared before every scenario, so just make sure we are on the site
    go(context, "/")


@when('I open "{path}"')
def open_path(context, path):
    go(context, path)
    time.sleep(1)  # give client-side redirects a moment


# ---------- signing in ----------

@step("I sign in as the customer")
def sign_in_customer(context):
    login(context, config.CUSTOMER_EMAIL, config.CUSTOMER_PASSWORD)


@step("I sign in as the admin")
def sign_in_admin(context):
    login(context, config.ADMIN_EMAIL, config.ADMIN_PASSWORD)


@when("I sign out")
def sign_out(context):
    click_button(context, "Sign out")
    time.sleep(0.5)


# ---------- clicking ----------

@when('I click "{text}"')
def click(context, text):
    click_button(context, text)


# ---------- checks ----------

@then('I should see a toast containing "{text}"')
def toast_shown(context, text):
    assert wait_for_toast(context, text), f'No toast containing "{text}" appeared'


@then('I should not see a toast containing "{text}"')
def toast_not_shown(context, text):
    assert not wait_for_toast(context, text, timeout=2), f'Unexpected toast containing "{text}"'


@then("the cart badge should show {count:d}")
def badge_shows(context, count):
    time.sleep(0.5)
    actual = badge_count(context)
    assert actual == count, f"Cart badge shows {actual}, expected {count}"


@then('I should see the text "{text}"')
def text_visible(context, text):
    wait(context).until(lambda d: text in page_text(context), f'"{text}" not found on page')


@then('I should not see the text "{text}"')
def text_not_visible(context, text):
    time.sleep(1.5)
    assert text not in page_text(context), f'"{text}" should not be on the page'


@then('the page should not contain the word "{word}"')
def word_absent(context, word):
    time.sleep(1)
    body = context.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert word.lower() not in body, f'Page contains the misspelt word "{word}"'


@then("I should be on the sign in page")
def on_login_page(context):
    try:
        wait(context, 5).until(lambda d: "/login" in d.current_url)
    except Exception:
        raise AssertionError(f"Not redirected to sign in; still on {context.driver.current_url}")


@then('the header should show "{text}"')
def header_shows(context, text):
    assert button(context, text).is_displayed()
