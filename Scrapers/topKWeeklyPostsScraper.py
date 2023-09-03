import os
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from msedge.selenium_tools import Edge, EdgeOptions
from datetime import date

# Set the desired user agent string
user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/95.0.1020.30 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/95.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Edge/95.0.1020.30 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/95.0",
    ]

headers = {
    "User-Agent": user_agents[7],
    "Accept-Language": "en-US,en;q=0.9",
}

# # Set up Chrome WebDriver with the desired user agent
# chrome_options = Options()
# chrome_options.add_argument(f"user-agent={user_agents[1]}")
# driver = webdriver.Chrome()

# Configure Edge WebDriver options
edge_options = EdgeOptions()
edge_options.use_chromium = True  # Use Chromium-based Edge
edge_options.add_argument(f"user-agent={user_agents[1]}")  # Change the index as needed

# Specify the path to the Microsoft Edge WebDriver executable
edge_driver_path = "msedgedriver.exe"  # Replace with the actual path

# Create an Edge WebDriver instance
driver = Edge(executable_path=edge_driver_path, options=edge_options)

# Function to scroll the page by a specified amount (in pixels)
def scroll_page(by_pixels):
    driver.execute_script(f"window.scrollBy(0, {by_pixels});")

def scrape(url, download_path):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    output_file = os.path.join(download_path, "links.txt")

    try:
        # Send an HTTP GET request to the URL using Selenium
        driver.get(url)
        # Wait for the page to load (adjust the wait time as needed)
        scroll_page("document.body.scrollHeight")
        time.sleep(10)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[slot="full-post-link"]')))

        # Get the page source (HTML content) using Selenium
        page_source = driver.page_source

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all <div> elements with the specified class
        div_elements = soup.find_all("a", {"slot": "full-post-link"})

        count = 0
        # Iterate through the div elements and filter based on your criteria
        for div_element in div_elements:
            if count == 15:
                break
            print("reddit.com" + div_element.get("href"))

            with open(output_file, 'a') as file:
                file.write(f"reddit.com{div_element.get('href')}\n")

            count += 1
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Define the URL of the Reddit page you want to scrape
    url = "https://www.reddit.com/r/tifu/top/?t=week"
    # Get today's date
    today = date.today().strftime("%Y-%m-%d")
    download_path = f"redditPosts/{today}"
    scrape(url, download_path)