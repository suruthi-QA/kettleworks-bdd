"""Behave hooks: start Chrome once, give every scenario a clean app state, screenshot failures."""
import os
import re
import sys

# make config.py and utils.py (project root) importable from the step files
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver  # noqa: E402
import allure
import config  # noqa: E402


def before_all(context):
    options = webdriver.ChromeOptions()
    if config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    context.driver = webdriver.Chrome(options=options)   # Selenium Manager downloads the driver


def before_scenario(context, scenario):
    # The app stores cart, orders, reviews and login in localStorage -> wipe it for a clean start
    context.driver.get(config.BASE_URL + "/")
    context.driver.execute_script("window.localStorage.clear();")
    context.driver.delete_all_cookies()


def after_step(context, step):
    if step.status == "failed":
        os.makedirs("reports/screenshots", exist_ok=True)
        name = re.sub(r"\W+", "_", context.scenario.name)[:80]
        context.driver.save_screenshot(f"reports/screenshots/{name}.png")
        allure.attach(context.driver.get_screenshot_as_png(),
                      name="failure screenshot",
                      attachment_type=allure.attachment_type.PNG)

def after_all(context):
    context.driver.quit()
