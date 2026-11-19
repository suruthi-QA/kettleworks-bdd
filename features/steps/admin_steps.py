import re
import time

from behave import then, when
from selenium.webdriver.common.by import By

from utils import api_products, find, find_all, money, page_text


def _admin_row(context, name):
    return find(context, By.XPATH, f"//main//table//tr[td[1][contains(., \"{name}\")]]")


@then("the admin table should list every product")
def lists_all(context):
    find(context, By.CSS_SELECTOR, "main table tbody tr")
    rows = find_all(context, "main table tbody tr")
    assert len(rows) == len(api_products()), f"{len(rows)} rows, expected {len(api_products())}"


@then("the stock value should equal price multiplied by stock for all products")
def stock_value(context):
    match = re.search(r"worth\s+(\S+)", page_text(context))
    assert match, "Stock value text not found"
    shown = money(match.group(1))
    expected = sum(p["price"] * p["stock"] for p in api_products())
    assert shown == expected, f"Stock value shows {shown}, expected {expected}"


@when('I click Restock for "{name}"')
def restock(context, name):
    _admin_row(context, name).find_element(By.XPATH, ".//*[normalize-space()='Restock']").click()
    time.sleep(1)


@then('the stock of "{name}" should be more than {minimum:d}')
def stock_above(context, name, minimum):
    stock = int(_admin_row(context, name).find_elements(By.TAG_NAME, "td")[3].text)
    assert stock > minimum, f"Stock of {name} is still {stock}"
