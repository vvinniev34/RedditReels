import os
import datetime
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge import service

# from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from datetime import date

from accountCredentials.reddit_account import reddit_username, reddit_password

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

def login():
    driver.get("https://www.reddit.com/login/")
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginUsername"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginPassword"))
    )
    username_field.send_keys(reddit_username)
    password_field.send_keys(reddit_password)
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "AnimatedForm__submitButton"))
    )
    login_button.click()

    time.sleep(5)
    
def scrape(url, download_path, subreddit):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    output_file = os.path.join(download_path, "links.txt")
    with open(output_file, 'a') as file:
        file.write(f"{subreddit[0]}\n\n")

    try:
        # Send an HTTP GET request to the URL using Selenium
        driver.get(url)
        # Wait for the page to load (adjust the wait time as needed)
        scroll_page("document.body.scrollHeight")
        time.sleep(3)

        wait = WebDriverWait(driver, 5)
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[slot="full-post-link"]')))
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "SQnoC3ObvgnGjWt90zD9Z")))
        # Get the page source (HTML content) using Selenium
        page_source = driver.page_source

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all <div> elements with the specified class
        # link_elements = soup.find_all("a", {"slot": "full-post-link"})
        link_elements = soup.find_all("a", class_="SQnoC3ObvgnGjWt90zD9Z")

        # Iterate through the div elements and filter based on your criteria
        for i in range(min(len(link_elements), 10)):#subreddit[1])):
            link_element = link_elements[i]
            print(f"reddit.com{link_element['href']}")

            with open(output_file, 'a') as file:
                file.write(f"reddit.com{link_element.get('href')}\n")
        with open(output_file, 'a') as file:
            file.write("\n")
    except:
        print(f"No posts today on {subreddit[0]}")
    finally:
        print(f"Finished running {subreddit[0]}")

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    # today = "Custom"
    current_date = datetime.datetime.now()

    login()
    
    long_form_subreddits = ["nosleep"]
    # considered = [["entitledparents", 1, 6], ["Glitch_in_the_Matrix", 1, 6], ["creepyencounters", 1, 6], ["LetsNotMeet", 1, 6], ["confession", 2, 6],]
    subreddits = [
        ["relationships", 1, 6], ["relationship_advice", 2, 6], 
        ["confessions", 2, 6], 
        ["TrueOffMyChest", 1, 6], ["offmychest", 3, 6],
        ["tifu", 1, 6], ["legaladvice", 1, 6], 
        ["AmItheAsshole", 3, 6], ["AITAH", 4, 6],  
        ["askreddit", 4, 6]
    ]

    for subreddit in subreddits:
        # if current_date.weekday() == subreddit[2]:
        if True:
            url = f"https://www.reddit.com/r/{subreddit[0]}/top/?t=week"
            download_path = f"RedditPosts/{today}"
            scrape(url, download_path, subreddit)

    # Close the browser
    driver.quit()