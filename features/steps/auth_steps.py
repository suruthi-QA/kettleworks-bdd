import time

from behave import then

import config
from utils import go, page_text, wait


@then("the account page should show the customer email")
def account_shows_email(context):
    go(context, "/account")
    email = config.CUSTOMER_EMAIL.lower()
    wait(context).until(lambda d: email in page_text(context).lower(),
                        f"{email} not shown on the Account page")


@then("I should not see the customer email")
def email_hidden(context):
    time.sleep(1)
    assert config.CUSTOMER_EMAIL.lower() not in page_text(context).lower(), \
        "Account details are still visible after signing out"
