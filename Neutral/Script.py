#!/usr/bin/env python

import os
import csv
import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



EXTENSIONS_DIR = "../Extension"

# === GET ARGUMENTS ===
if len(sys.argv) != 2:
    print("Usage: python watch_batch.py  <path/to/batch.csv>")
    sys.exit(1)

PROFILE= "Neutral"


BATCH_FILE = sys.argv[1]

if not os.path.exists(BATCH_FILE):
    print(f"Batch file not found: {BATCH_FILE}")
    sys.exit(1)

# === DRIVER SETUP ===
def create_driver(profile):


    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--headless=new") 

    extension = os.path.join(EXTENSIONS_DIR, profile.lower())
    if os.path.exists(extension):
        chrome_options.add_argument(f'--load-extension={extension}')
        print(f"Extension added for profile '{profile}': {extension}")

    driver = webdriver.Chrome(options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    driver.set_page_load_timeout(20)
    return driver

def login(driver, email):
    driver.get("https://accounts.google.com/")
    time.sleep(5)
    try:
        email_input = driver.find_element(By.ID, "identifierId")
        email_input.send_keys(email)
        driver.find_element(By.ID, "identifierNext").click()
        time.sleep(5)
        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys("PoodlesNoodles123!")
        driver.find_element(By.ID, "passwordNext").click()
        time.sleep(5)
    except Exception as e:
        print(f"[{PROFILE}] Login skipped or failed: {e}")
    return driver

def watch_video(driver, url):
    try:
        driver.get(url)
        print(f"[{PROFILE}] Watching {url}")
        time.sleep(random.randint(3, 7))

    
        total_watch = random.randint(300, 600)
        print(f"[{PROFILE}] Watching start for  {total_watch }s .")
        time.sleep(total_watch)
    except Exception as e:
        print(f"[{PROFILE}] Error while watching video {url}: {e}")

# === MAIN FUNCTION ===
def main():
    print(f"Running batch file for no profile: {BATCH_FILE}")
    driver = create_driver(PROFILE)

    try:
        with open(BATCH_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                video_id = row["video_id"]
                watch_video(driver, video_id)
                time.sleep(random.randint(30, 60))
    finally:
        driver.quit()

# === RUN ===
if __name__ == "__main__":
    main()
