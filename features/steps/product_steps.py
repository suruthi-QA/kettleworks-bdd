import time

from behave import then, when
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils import (click_button, find, find_all, product_by_name, read_storage, type_into,
                   wait)


@when("I add {qty} of it to the cart")
def add_to_cart(context, qty):
    type_into(context, "qty", qty)
    click_button(context, "Add to cart")
    time.sleep(0.5)


@then('the cart should not hold more than the stock of "{name}"')
def within_stock(context, name):
    product = product_by_name(name)
    cart = read_storage(context, "kw.cart") or []
    qty = sum(item["qty"] for item in cart if item["id"] == product["id"])
    assert qty <= product["stock"], f"Cart has {qty} but only {product['stock']} in stock"


@then("the cart should be empty")
def cart_empty(context):
    cart = read_storage(context, "kw.cart") or []
    assert cart == [], f"Cart should be empty but has {cart}"


@when("I open the care and sizing guide")
def open_guide(context):
    click_button(context, "Care and sizing guide")
    find(context, By.CSS_SELECTOR, ".modal")


@then("the Close button should be inside the modal")
def close_inside_modal(context):
    inside = context.driver.execute_script("""
        const m = document.querySelector('.modal').getBoundingClientRect();
        const b = document.querySelector('.modal-close').getBoundingClientRect();
        return b.left >= m.left && b.right <= m.right && b.top >= m.top && b.bottom <= m.bottom;
    """)
    assert inside, "Close button sits outside the modal box"


@when("I press Escape")
def press_escape(context):
    ActionChains(context.driver).send_keys(Keys.ESCAPE).perform()


@then("the modal should be closed")
def modal_closed(context):
    try:
        wait(context, 3).until(lambda d: not [m for m in find_all(context, ".modal") if m.is_displayed()])
    except Exception:
        raise AssertionError("Modal is still open after pressing Escape")


@when('I post the review "{text}"')
def post_review(context, text):
    type_into(context, "review", text)
    click_button(context, "Post review")


@then('the review "{text}" should be listed')
def review_listed(context, text):
    wait(context).until(lambda d: any(text in r.text for r in find_all(context, ".review")),
                        f'Review "{text}" not listed')


@then('the review "{text}" should be listed as plain text')
def review_plain_text(context, text):
    time.sleep(1)
    reviews = [r.text for r in find_all(context, ".review")]
    assert any(text in r for r in reviews), f"HTML was rendered instead of shown as text: {reviews}"
