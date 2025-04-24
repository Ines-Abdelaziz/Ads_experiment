from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests


import json


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


# Set up Chrome options
options = Options()
#add headless option 
options.add_argument('--user-data-dir=/tmp/chrome-user-data')
options.add_argument('--remote-debugging-port=9222')

options.add_argument("--headless=new")  # << Use new headless mode
options.add_argument("--window-size=1920,1080")  # Important for rendering properly
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")
# Start Chrome with the specified user profile
driver = webdriver.Chrome(options=options)





















# 1. Go to Google Login
driver.get("https://accounts.google.com/")
time.sleep(5)  # Wait for the page to load
# 2. Enter email in the email field
email_input = driver.find_element(By.ID, "identifierId")
email="dereksloane1@gmail.com"
email_input.send_keys(email)
time.sleep(2)  # Wait for the input to be entered
driver.save_screenshot("e1.png")
# 3. Click Next
next_button = driver.find_element(By.ID, "identifierNext")
next_button.click()
time.sleep(5)  # Wait for the next page to load
# 4. Enter password in the password field
#try catch for password field
try:
   
    password_input = driver.find_element(By.NAME, "Passwd")
except:
    #save png screenshot
    driver.save_screenshot("error.png")

password="PoodlesNoodles123!"
password_input.send_keys(password)
time.sleep(2)  # Wait for the input to be entered
driver.save_screenshot("e2.png")
# 5. Click Next
next_button = driver.find_element(By.ID, "passwordNext")
next_button.click()


# 6. Wait for the login to complete
time.sleep(5)  
driver.save_screenshot("e3.png")

try:
    recovery_button = driver.find_element(
        By.XPATH,
        "//li[contains(., 'Confirm your recovery phone number')]"
    )
    print("Element found:", recovery_button.text)
    recovery_button.click()  # Optional
    time.sleep(5)  
    driver.save_screenshot("e4.png")
    number_input = driver.find_element(By.ID, "phoneNumberId")
    number="(303) 257 2627"
    number_input.send_keys(number)
    time.sleep(2)  # Wait for the input to be entered
    driver.save_screenshot("e5.png")
    send_button = driver.find_element(By.XPATH, "//button[.//span[text()='Send']]")
    send_button.click()
    time.sleep(5)  # Wait for the next page to load
    driver.save_screenshot("e6.png")

except Exception as e:
    print("Element not found:", str(e))
    driver.save_screenshot("confirm_phone_not_found.png")


driver.get("https://www.google.com/")
time.sleep(2)  # Wait for the page to load
driver.save_screenshot("e7.png")

# # 🍪 Load cookies
# with open("cookies.json", "r") as f:
#     cookies = json.load(f)

# for cookie in cookies:
#     if 'sameSite' in cookie:
#         del cookie['sameSite']  # Avoid errors
#     driver.add_cookie(cookie)

response = requests.get('https://ipinfo.io')
data = response.json()
country = data.get('country', 'Unknown')
ip_address = data.get('ip', 'Unknown')
print(f"IP Address: {ip_address}")

print(f"Country: {country}")
driver.get("https://mail.google.com/mail/")
time.sleep(2)  # Wait for the page to load
#screenshot
driver.save_screenshot("e8.png")

