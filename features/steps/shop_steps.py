import time
from collections import Counter

from behave import then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from utils import (all_listed_names, api_products, find, listed_names, listed_prices,
                   page_text, product_by_name, select_option, type_into)


@when('I search for "{term}"')
def search(context, term):
    type_into(context, "q", term)
    time.sleep(0.5)


@when('I select the category "{category}"')
def choose_category(context, category):
    select_option(context, "cat", category)
    time.sleep(0.5)


@when('I sort by "{label}"')
def choose_sort(context, label):
    select_option(context, "sort", label)
    time.sleep(0.5)


@when("I go through all pages")
def go_through_pages(context):
    context.all_names = all_listed_names(context)


@then("I should see {count:d} products")
def product_count(context, count):
    names = listed_names(context)
    assert len(names) == count, f"Expected {count} products, got {len(names)}: {names}"


@then('the pager should show "{text}"')
def pager_text(context, text):
    actual = find(context, By.CSS_SELECTOR, ".pager .meta").text
    assert actual == text, f'Pager shows "{actual}"'


@then('I should see "{name}" in the results')
def name_in_results(context, name):
    names = listed_names(context)
    assert name in names, f'"{name}" not in results: {names}'


@then("no products should be listed")
def no_products(context):
    time.sleep(1)
    assert listed_names(context) == [], f"Products listed: {listed_names(context)}"


@then("the loading spinner should not be visible")
def no_spinner(context):
    assert "Loading products" not in page_text(context), "Spinner still showing 'Loading products'"


@then('every listed product should belong to "{category}"')
def all_in_category(context, category):
    names = listed_names(context)
    assert names, "No products listed"
    wrong = [n for n in names if product_by_name(n)["category"] != category]
    assert not wrong, f"Not in {category}: {wrong}"


@then("the prices should be in ascending order")
def prices_ascending(context):
    prices = listed_prices(context)
    assert prices == sorted(prices), f"Not ascending: {prices}"


@then("the prices should be in descending order")
def prices_descending(context):
    prices = listed_prices(context)
    assert prices == sorted(prices, reverse=True), f"Not descending: {prices}"


@then('the category filter should still be "{category}"')
def category_kept(context, category):
    selected = Select(find(context, By.ID, "cat")).first_selected_option.text
    assert selected == category, f'Category filter changed to "{selected}"'


@then("each product should appear only once")
def no_duplicates(context):
    dupes = [name for name, n in Counter(context.all_names).items() if n > 1]
    assert not dupes, f"Shown on more than one page: {dupes}"


@then("the number of listed products should match the API")
def count_matches_api(context):
    expected = len(api_products())
    assert len(context.all_names) == expected, f"Listed {len(context.all_names)}, API has {expected}"


@then('the "{text}" button should be disabled')
def button_disabled(context, text):
    btn = find(context, By.XPATH, f"//button[normalize-space()='{text}']")
    assert not btn.is_enabled(), f'"{text}" button is enabled'
