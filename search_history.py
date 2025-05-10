import os
import openai
import google.generativeai as genai
from googleapiclient.discovery import build
import pandas as pd

# Set API keys


import random


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from selenium.webdriver.common.action_chains import ActionChains


import json


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


import csv 

















# # 1. Go to Google Login
# driver.get("https://accounts.google.com/")
# time.sleep(5)  # Wait for the page to load
# # 2. Enter email in the email field
# email_input = driver.find_element(By.ID, "identifierId")
# email="yang.lexie27@gmail.com"
# email_input.send_keys(email)
# time.sleep(2)  # Wait for the input to be entered
# # 3. Click Next
# next_button = driver.find_element(By.ID, "identifierNext")
# next_button.click()
# time.sleep(5)  # Wait for the next page to load
# # 4. Enter password in the password field
# #try catch for password field
# try:
#     password_input = driver.find_element(By.NAME, "Passwd")
# except:
#     #save png screenshot
#     print("Password field not found")

# password="PoodlesNoodles123!"
# password_input.send_keys(password)
# time.sleep(2)  # Wait for the input to be entered
# # 5. Click Next
# next_button = driver.find_element(By.ID, "passwordNext")
# next_button.click()


# # 6. Wait for the login to complete
# time.sleep(5)  



# --- Read domains from CSV ---
def read_domains(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        #return a list of random 50 domains
        domains = [row['domain'] for row in reader]
        random_domains = random.sample(domains, 50)
        #save the random domains to a new csv file
        with open('Fact_domains.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['domain'])
            for domain in random_domains:
                writer.writerow([domain])
        return random_domains


# --- Simulated Browsing ---


def human_scroll(driver):
    for _ in range(random.randint(3, 7)):
        pixels = random.randint(200, 800)
        driver.execute_script(f"window.scrollBy(0, {pixels});")
        time.sleep(random.uniform(0.5, 2))

def click_random_link(driver):
    links = driver.find_elements(By.TAG_NAME, "a")
    visible_links = [l for l in links if l.is_displayed() and l.get_attribute("href")]
    if visible_links:
        link = random.choice(visible_links)
        href = link.get_attribute("href")  # capture before clicking
        ActionChains(driver).move_to_element(link).pause(0.5).click(link).perform()
        print("Clicked a link:", href)
        time.sleep(random.uniform(5, 10))


def simulate_browsing(driver, url):
    driver.get(url)
    time.sleep(random.uniform(5, 10))

    human_scroll(driver)
    click_random_link(driver)
    human_scroll(driver)



# --- Main ---
def main():
    profile_dir='/Users/iabdelaz/Library/Application Support/Google/Chrome/'
    profile_name='Profile 12'
    # Set up Chrome options
    options = Options()
    #add headless option 
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument(f"--profile-directory={profile_name}")

    # options.add_argument("--headless=new")  # << Use new headless mode
    options.add_argument("--window-size=1920,1080")  # Important for rendering properly
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_extension('./cookies.crx')

    # Start Chrome with the specified user profile
    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    driver.set_page_load_timeout(20)  # seconds


    #read csv File 
    domains_fact= pd.read_csv('Fact_domains.csv')
    domains_misinfo= pd.read_csv('Misinfo_domains.csv')
    domains_fact= domains_fact['domain'].tolist()
    domains_misinfo= domains_misinfo['domain'].tolist()

   #remove t-first 3 domains from the list
    domains_fact = domains_fact[6:]

    try:
        for domain in domains_fact:
            #try https or http else skip without throwing error
            try:
                response = requests.get("https://"+domain)
                domain = response.url
            except requests.exceptions.RequestException:
                try:
                    response = requests.get("http://"+domain)
                    domain = response.url
                except requests.exceptions.RequestException:
                    print("Skipping:", domain)
                    continue
            # If the request was successful, proceed
            if response.status_code != 200:
                print("Skipping:", domain)
                continue
            # If the request was successful, proceed

         
            print("Browsing:", domain)
            simulate_browsing(driver, domain)
            time.sleep(random.uniform(3, 6))
    finally:
        driver.quit()

if __name__ == "__main__":
    main()