from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def main():
    # Setup Chrome options
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment to run in headless mode (no UI)

    print("Initializing Chrome Driver...")
    # Initialize the WebDriver.
    # Selenium 4+ looks for chromedriver in system PATH by default.
    driver = webdriver.Chrome(options=options)

    try:
        url = "https://pimeyes.com"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        print("Page opened successfully.")
        
        # Keep the script running so the browser stays open
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()
