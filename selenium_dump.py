from sys import argv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import tempfile
import time
import pandas as pd
import argparse
from datetime import datetime

# Credentials - ideally should be stored in environment variables
USERNAME = "parkcora94@gmail.com"
PASSWORD = "Guru2024@"
# name = "NQM25"
# name = "M0M25"
# name = "CLK25"
name = "GCJ25"
name = "HAJ25"

data_range = pd.date_range(start="2010-02-01", end="2025-04-11")
data_range = pd.date_range(start="2010-02-01", end="2024-11-11")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Download data from Barchart')
    parser.add_argument('--name', required=True, help='Symbol name (e.g., GCJ25)')
    parser.add_argument('--start-date', required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', required=True, help='End date in YYYY-MM-DD format')
    return parser.parse_args()


def setup_driver():
    """Set up and return the WebDriver with appropriate options"""
    temp_dir = tempfile.mkdtemp()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    return webdriver.Chrome(options=chrome_options)


def login(driver, wait):
    """Handle the login process"""
    driver.get("https://www.barchart.com/login")

    username_field = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='text'][name='email']")
        )
    )
    password_field = wait.until(
        EC.presence_of_element_located((By.ID, "login-page-form-password"))
    )
    time.sleep(1)
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bc-button.login-button"))
    )
    submit_button.click()

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='My Account']"))
    )
    print("Login successful!")


def navigate_to_download_page(driver, name="VIJ25"):
    """Navigate to the price history download page"""
    driver.get(f"https://www.barchart.com/my/price-history/download/{name}")


def setup_form_defaults(driver, wait):
    """Set up the default form values"""
    # Clear and set up symbol input

    # Set frequency to Intraday Nearby
    frequency_dropdown = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "select[data-ng-model='frequency']")
        )
    )
    select = Select(frequency_dropdown)
    select.select_by_visible_text("Intraday Nearby")

    # Set aggregation to 1
    aggregation_input = wait.until(
        EC.presence_of_element_located((By.NAME, "aggregation"))
    )
    aggregation_input.clear()
    aggregation_input.send_keys("1")

    # Check Total Volume and Open Interest checkbox if not already selected
    volume_checkbox = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='bc-total-volume']"))
    )
    checkbox_input = driver.find_element(By.ID, "bc-total-volume")
    if not checkbox_input.is_selected():
        volume_checkbox.click()


def set_date_field(field, date_value, wait):
    """Set a date field with proper clearing and waiting"""
    field.clear()
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    time.sleep(0.5)
    field.send_keys(date_value)
    time.sleep(0.5)


def download_data(start_date, end_date, driver, wait):
    """Download data for a specific date range"""
    # Set start date
    start_date_input = wait.until(EC.presence_of_element_located((By.NAME, "dateFrom")))
    set_date_field(start_date_input, start_date, wait)

    # Set end date
    end_date_input = wait.until(EC.presence_of_element_located((By.NAME, "dateTo")))
    set_date_field(end_date_input, end_date, wait)

    # Click download button
    download_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.bc-button.add.light-blue.download-btn")
        )
    )
    download_button.click()

    # Wait for download to complete
    print(f"Downloading data for {start_date} to {end_date}...")
    time.sleep(15)


# def main():
# args = parse_arguments()
# name = argv.name
# data_range = pd.date_range(start=args.start_date, end=args.end_date)

# Initialize driver and wait
driver = setup_driver()
wait = WebDriverWait(driver, 10)

login(driver, wait)
navigate_to_download_page(driver, name)

# Download data in chunks
for i in range(1, 251):
    # Reset form defaults for each iteration
    setup_form_defaults(driver, wait)

    # Calculate date range for this chunk
    start_index = 18 * i + 1
    end_index = 18 * i - 17

    # Skip if indices are out of range
    if start_index >= len(data_range) or end_index < 0:
        continue

    start_date = data_range[-start_index].strftime("%m/%d/%Y")
    end_date = data_range[-end_index].strftime("%m/%d/%Y")

    # Download data for this date range
    download_data(start_date, end_date, driver, wait)
