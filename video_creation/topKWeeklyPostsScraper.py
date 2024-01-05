import os
import datetime
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge import service

# from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
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

# Configure Edge WebDriver options
edge_options = EdgeOptions()
edge_options.use_chromium = True  # Use Chromium-based Edge
edge_options.add_argument(f"user-agent={user_agents[1]}")  # Change the index as needed

# Specify the path to the Microsoft Edge WebDriver executable
script_dir = os.path.dirname(os.path.abspath(__file__))
edge_driver_path = os.path.join(script_dir, "edgedriver_win64/msedgedriver.exe")

# Create an Edge WebDriver instance
# driver = webdriver.Edge(options=edge_options)

s=service.Service(r"edgedriver_win64/msedgedriver.exe")
driver = webdriver.Edge(service=s)

# Function to scroll the page by a specified amount (in pixels)
def scroll_page(by_pixels):
    driver.execute_script(f"window.scrollBy(0, {by_pixels});")
    
def scrape(url, download_path, subreddit, max_stories):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    output_file = os.path.join(download_path, "links.txt")
    with open(output_file, 'a') as file:
        file.write(f"{subreddit}\n\n")

    try:
        # Send an HTTP GET request to the URL using Selenium
        driver.get(url)
        # Wait for the page to load (adjust the wait time as needed)
        scroll_page("document.body.scrollHeight")
        time.sleep(3)

        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[slot="full-post-link"]')))
        # Get the page source (HTML content) using Selenium
        page_source = driver.page_source

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all <div> elements with the specified class
        link_elements = soup.find_all("a", {"slot": "full-post-link"})

        # Iterate through the div elements and filter based on your criteria
        for i in range(min(len(link_elements), max_stories)):
            link_element = link_elements[i]
            print(f"reddit.com{link_element.get('href')}")

            with open(output_file, 'a') as file:
                file.write(f"reddit.com{link_element.get('href')}\n")
        with open(output_file, 'a') as file:
            file.write("\n")
    except:
        print(f"No posts today on {subreddit}")
    finally:
        print(f"Finished running {subreddit}")

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    current_date = datetime.datetime.now()
    
    long_form_subreddits = ["nosleep"]
    daily_subreddits = ["nosleep", "LetsNotMeet", "TrueOffMyChest", "MaliciousCompliance", "creepyencounters"]
    weekly_subreddits = ["entitledparents", "pettyrevenge", "tifu", "AmItheAsshole", "relationship_advice", "Glitch_in_the_Matrix"]
    for subreddit in daily_subreddits:
        # Define the URLs of the Reddit page you want to scrape
        url = f"https://www.reddit.com/r/{subreddit}/top/?t=daily"
        # Get today's date
        download_path = f"RedditPosts/{today}"
        scrape(url, download_path, subreddit, 3)
    # run weekly scraper on sundays
    if current_date.weekday() == 6:
        for subreddit in weekly_subreddits:
            # Define the URLs of the Reddit page you want to scrape
            url = f"https://www.reddit.com/r/{subreddit}/top/?t=weekly"
            # Get today's date
            download_path = f"RedditPosts/{today}"
            scrape(url, download_path, subreddit, 5)
    # Close the browser
    driver.quit()