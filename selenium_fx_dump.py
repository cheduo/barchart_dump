import os
import glob
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import tempfile
import time
import pandas as pd
from datetime import datetime
import numpy as np

# Credentials - ideally should be stored in environment variables
# USERNAME = "parkcora94@gmail.com"
# PASSWORD = "Guru2024@"

USERNAME = "larry@kust.edu.cn"
PASSWORD = "Tech2022@"
name = "^AUDUSD"


def setup_driver(headless=True):
    """Set up and return the WebDriver with appropriate options"""
    temp_dir = tempfile.mkdtemp()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")

    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

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


def navigate_to_download_page(driver, name):
    """Navigate to the price history download page"""
    driver.get(f"https://www.barchart.com/my/price-history/download/{name}")


def setup_form_defaults(driver, wait):
    """Set up the default form values"""
    # Set frequency to Intraday Nearby
    frequency_dropdown = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "select[data-ng-model='frequency']")
        )
    )
    select = Select(frequency_dropdown)
    select.select_by_visible_text("Intraday")

    # Set aggregation to 1
    aggregation_input = wait.until(
        EC.presence_of_element_located((By.NAME, "aggregation"))
    )
    aggregation_input.clear()
    aggregation_input.send_keys("1")


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
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    start_date_str = start_date.strftime("%m/%d/%Y")
    end_date_str = end_date.strftime("%m/%d/%Y")

    # Set start date
    start_date_input = wait.until(EC.presence_of_element_located((By.NAME, "dateFrom")))
    set_date_field(start_date_input, start_date_str, wait)

    # Set end date
    end_date_input = wait.until(EC.presence_of_element_located((By.NAME, "dateTo")))
    set_date_field(end_date_input, end_date_str, wait)

    # Click download button
    download_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.bc-button.add.light-blue.download-btn")
        )
    )
    download_button.click()
    # Wait for download to complete
    time.sleep(15)


def get_most_recent_csv():
    """Get the most recently created CSV file from the Downloads folder"""
    downloads_path = r"C:\Users\cdsjt\Downloads"
    csv_files = glob.glob(os.path.join(downloads_path, "*.csv"))

    if not csv_files:
        print("No CSV files found in Downloads folder")
        return None

    # Sort files by creation time, newest first
    most_recent_csv = max(csv_files, key=os.path.getctime)
    return most_recent_csv


# Initialize driver and login
driver = setup_driver(
    headless=False
)  # Set to True for headless mode, False for visible browser
wait = WebDriverWait(driver, 10)

login(driver, wait)
# start download
time.sleep(10)

navigate_to_download_page(driver, name)
# Download initial sample to determine optimal batch size
# END_DATE = datetime.now().strftime("%Y-%m-%d")
START_DATE = "2010-02-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")
END_DATE = "2024-08-02"
END_DATE = "2023-01-23"
END_DATE = "2020-12-29"

if END_DATE == datetime.now().strftime("%Y-%m-%d"):
    setup_form_defaults(driver, wait)
    download_data(
        start_date="2025-04-10", end_date="2025-04-17", driver=driver, wait=wait
    )
    time.sleep(10)
    # Get the most recent CSV file after the download
    most_recent_csv = get_most_recent_csv()
    df_test = pd.read_csv(most_recent_csv, parse_dates=["Time"])
    df_test = df_test.dropna(subset=["Time", "Open"])
    df_test["Time"] = pd.to_datetime(df_test["Time"])
    sample_per_day = df_test.groupby(df_test.Time.dt.date)["Time"].count().max()
    nday_per_bucket = int(np.floor(20000 / sample_per_day))
    nday_per_bucket += 2 * nday_per_bucket // 5
    print(f"nday_per_bucket : {nday_per_bucket}")


# nday_per_bucket
nday_per_bucket = 18
print(f"nday_per_bucket : {nday_per_bucket}")
data_range = pd.date_range(start=END_DATE, end=START_DATE, freq=f"{-nday_per_bucket}D")
# Download data in chunks
for end_date in data_range:
    # Reset form defaults for each iteration
    setup_form_defaults(driver, wait)
    # Calculate start date for this chunk
    start_date = end_date - pd.Timedelta(days=nday_per_bucket)
    print(
        f"Downloading data for {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}..."
    )
    # Download data for this date range
    download_data(start_date, end_date, driver, wait)
