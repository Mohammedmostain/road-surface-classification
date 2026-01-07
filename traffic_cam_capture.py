import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
WEBSITE_URL = "https://edmontontrafficcam.com/"
INTERVAL_SECONDS = 60  # 2 minutes
SAVE_FOLDER = "traffic_screenshots"

def setup_driver():
    """Sets up the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run in background (no visible window)
    options.add_argument("--start-maximized")
    # Automatically install and manage the correct ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def main():
    # 1. Create folder for screenshots if it doesn't exist
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        print(f"Created folder: {SAVE_FOLDER}")

    driver = setup_driver()

    try:
        # 2. Open the website
        print(f"Opening {WEBSITE_URL}...")
        driver.get(WEBSITE_URL)

        # 3. User Interaction Step
        print("\n" + "="*50)
        print("ACTION REQUIRED:")
        print("1. The browser window is now open.")
        print("2. Please verify the map is loaded.")
        print("3. CLICK on the camera icon you want to monitor.")
        print("4. Wait until the video/image popup appears and the footage is visible.")
        input("5. Press ENTER in this terminal once the camera footage is ready... ")
        print("="*50 + "\n")

        # 4. Attempt to find the video element to screenshot ONLY the footage
        # We look for a <video> tag or a container that likely holds the image.
        target_element = None
        
        # Try finding the HTML5 video tag first
        try:
            target_element = driver.find_element(By.TAG_NAME, "video")
            print("Found video element! focusing capture on the video stream.")
        except:
            print("Could not isolate <video> tag. Falling back to full window capture.")
            target_element = None

        print(f"Starting capture loop. Taking a screenshot every {INTERVAL_SECONDS} seconds.")
        print("Press Ctrl+C in this terminal to stop.")

        while True:
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{SAVE_FOLDER}/cam_{timestamp}.png"

            if target_element:
                # Screenshot just the video element
                target_element.screenshot(filename)
            else:
                # Screenshot the whole visible browser window if element specific failed
                driver.save_screenshot(filename)

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved {filename}")
            
            # Wait for the next interval
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nStopping script...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()