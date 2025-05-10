import time
import random , pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def human_typing(element, text, delay_range=(0.1, 0.3)):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(*delay_range))


def search_google(driver, query):
    driver.get("https://www.google.com")

    # Accept cookies if shown
    try:
        consent_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I agree')]"))
        )
        consent_btn.click()
    except:
        pass

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    human_typing(search_box, query)
    time.sleep(random.uniform(0.5, 1.5))
    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))
    time.sleep(random.uniform(1, 2))

    links = driver.find_elements(By.CSS_SELECTOR, "div#search a")
    valid_links = [
        l for l in links
        if l.get_attribute("href") and
        "google.com" not in l.get_attribute("href") and
        l.is_displayed()
    ]

    if valid_links:
        link = random.choice(valid_links)
        # Scroll into view before clicking
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        time.sleep(random.uniform(0.5, 1))
        try:
            link.click()
            print("Clicked:", link.get_attribute("href"))
        except Exception as e:
            print("Failed to click link:", e)
    else:
        print("No clickable search results found.")



# === Run the script ===
if __name__ == "__main__":
    profile_dir='/Users/iabdelaz/Library/Application Support/Google/Chrome/'
    profile_name='Profile 18'
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
    # # # 1. Go to Google Login
    # driver.get("https://accounts.google.com/")
    # time.sleep(5)  # Wait for the page to load
    # # 2. Enter email in the email field
    # email_input = driver.find_element(By.ID, "identifierId")
    # email="brandon.ercel@gmail.com"
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

    queries = pd.read_csv('misinfo2_queries.csv')['Query'].tolist()  # Load queries from CSV

   

    try:
        for query in queries:
            print(f"\nSearching: {query}")
            search_google(driver, query)
            time.sleep(random.uniform(5, 10))  # Wait before next search
    finally:
        driver.quit()
