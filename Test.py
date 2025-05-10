from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
import threading
import os
import shutil
import tempfile
import uuid

# Path to Chrome user data directory
USER_DATA_DIR = "./"
BASE_PROFILES_DIR = "./"  
EXTENSIONS_DIR = "Extension"  

# 12 YouTube profiles (assumes you are already logged in)
PROFILES = ["Alex", "Alice","Bob","Brandon","Christo","Cristina","Derek","Georgiana","Lexie","Mark","Marly","Molly"]
EMAILS =["alextorresrobbins@gmail.com","alice.melows@gmail.com","bob.flopper.copper@gmail.com","brandon.ercel@gmail.com","christo.bobly@gmail.com","cristina.greyy1@gmail.com","dereksloane1@gmail.com","georgiana.tsumu@gmail.com","yang.lexie27@gmail.com","mark.bobondi@gmail.com","marly.chickens@gmail.com","molly.sumu@gmail.com"]
# Replace with your list of video URLs
YOUTUBE_VIDEOS = [
    "https://www.youtube.com/watch?v=rgaqwFPU7cc",
]
# function to create drivers from profile 
def create_driver(profile):
    
    profile_dir= os.path.join(USER_DATA_DIR, profile)
    profile_name = profile
    profile_path= os.path.join(profile_dir, profile_name)
    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"Profile folder not found: {profile_path}")

   
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={profile_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_name}")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Add extension
    extension= os.path.join(EXTENSIONS_DIR, f"{profile.lower()}")
    print(extension)
    if os.path.exists(extension):
        chrome_options.add_argument(f'--load-extension={extension}')

        print(f"Extension added for profile '{profile}': {extension}")
    else:
        print(f"Warning: Extension ZIP not found for profile '{profile}': {extension}")

    # Launch Chrome
    driver = webdriver.Chrome(options=chrome_options)

    # Anti-detection script
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    driver.set_page_load_timeout(20)

    return driver  # Return temp dir so you can delete it later

def login(driver,email):
    # 1. Go to Google Login
    driver.get("https://accounts.google.com/")
    time.sleep(5)  # Wait for the page to load
    # 2. Enter email in the email field 
    try:
        email_input = driver.find_element(By.ID, "identifierId")
    except:
        #dont throw error and continue
        print("Email field not found")
        return driver
    email_input.send_keys(email)
    time.sleep(2)  # Wait for the input to be entered
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
        print("Password field not found")
    password="PoodlesNoodles123!"
    password_input.send_keys(password)
    time.sleep(2)  # Wait for the input to be entered
    # 5. Click Next
    next_button = driver.find_element(By.ID, "passwordNext")
    next_button.click()
    # 6. Wait for the login to complete
    time.sleep(5)
    return driver

def watch_video(driver, video_url):
    
    try:
        driver.get(video_url)
        print(f"[{profile}] Watching {video_url}")

        # Wait for video to load
        time.sleep(random.randint(3, 7))
        #get play button and click it by x path [@id="movie_player"]/
        play_button = driver.find_element(By.XPATH, '//*[@id="movie_player"]')
        play_button.click()
        time.sleep(random.randint(3, 7))  # Wait for the video to start

        total_watch_time = random.randint(300, 600)  # 5 to 10 mins in seconds
        first_part = random.randint(150, 300)        # First 2.5 to 5 mins

        print(f"[{profile}] Watching start for {first_part} seconds.")
        time.sleep(first_part)

        # # Skip to 5 or 10 minute mark
        # skip_to = random.choice([300, 600])  # seconds
        # driver.execute_script(f"""
        #     document.querySelector('video').currentTime = {skip_to};
        # """)
        # print(f"[{profile}] Skipped to {skip_to // 60} min mark.")

        remaining_time = total_watch_time - first_part
        print(f"[{profile}] Watching rest for {remaining_time} seconds.")
        time.sleep(remaining_time)

    except Exception as e:
        print(f"[{profile}] Error: {e}")
    finally:
        driver.quit()

def run_profile(profile,i):
    driver = create_driver(profile)
    driver=login(driver,EMAILS[i])
    
    try:
        for video_url in YOUTUBE_VIDEOS:
            watch_video(driver, video_url)
            time.sleep(random.randint(30, 60))  # Rest between videos
    finally:
        driver.quit()

# Run all 12 in parallel
threads = []
for i in range(12):
    profile = PROFILES[i]
    t = threading.Thread(target=run_profile, args=(profile,i))
    t.start()
    threads.append(t)
    time.sleep(2)  # slight delay between launches

# Wait for all to finish
for t in threads:
    t.join()
