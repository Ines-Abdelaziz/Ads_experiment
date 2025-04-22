from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

import json


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# Expand ~ to full home path
home_dir = os.path.expanduser("~")

# Chrome user data root directory
user_data_dir = os.path.join(home_dir, "Library", "Application Support", "Google", "Chrome")

# Set up Chrome options
options = Options()
#add headless option 
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





















# # 1. Go to Google Login
# driver.get("https://accounts.google.com/")
# time.sleep(5)  # Wait for the page to load
# # 2. Enter email in the email field
# email_input = driver.find_element(By.ID, "identifierId")
# email="dereksloane1@gmail.com"
# email_input.send_keys(email)
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
#     driver.save_screenshot("error.png")

# password="PoodlesNoodles123!"
# password_input.send_keys(password)
# # 5. Click Next
# next_button = driver.find_element(By.ID, "passwordNext")
# next_button.click()


# # 6. Wait for the login to complete
# time.sleep(2)  


driver.get("https://www.google.com/")

time.sleep(2)  # Wait for the page to load

# 🍪 Load cookies
with open("cookies.json", "r") as f:
    cookies = json.load(f)

for cookie in cookies:
    if 'sameSite' in cookie:
        del cookie['sameSite']  # Avoid errors
    driver.add_cookie(cookie)

driver.get("https://www.google.com/")
time.sleep(2)  # Wait for the page to load
#get loaction
location = driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/div/div[1]')
print(location.text)
#screenshot
driver.save_screenshot("location.png")

