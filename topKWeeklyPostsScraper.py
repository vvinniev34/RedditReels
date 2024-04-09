import os
import datetime
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge import service

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from datetime import date

from dotenv import load_dotenv
load_dotenv()
reddit_username = os.environ.get('REDDIT_USERNAME')
reddit_password = os.environ.get('REDDIT_PASSWORD')
edge_driver_path = os.environ.get('EDGE_DRIVER_PATH')

# Configure Edge WebDriver options
edge_options = EdgeOptions()
edge_options.use_chromium = True  # Use Chromium-based Edge
edge_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/95.0.1020.30 Safari/537.36")

s = service.Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=s)

# Function to scroll the page by a specified amount (in pixels)
def scroll_page(by_pixels):
    driver.execute_script(f"window.scrollBy(0, {by_pixels});")

def login():
    driver.get("https://www.reddit.com/login/")
    # time.sleep(3000)
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-username"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-password"))
    )
    username_field.send_keys(reddit_username)
    password_field.send_keys(reddit_password)
    # time.sleep(30000)
    # login_button = WebDriverWait(driver, 10).until(
    #     # EC.element_to_be_clickable((By.CLASS_NAME, "AnimatedForm__submitButton"))
    #     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log In')]"))
    # )
    # print(login_button)
    # login_button.click()

    time.sleep(10)
    
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
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[slot="full-post-link"]')))
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "SQnoC3ObvgnGjWt90zD9Z")))
        # Get the page source (HTML content) using Selenium
        page_source = driver.page_source

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all <div> elements with the specified class
        link_elements = soup.find_all("a", {"slot": "full-post-link"})
        # link_elements = soup.find_all("a", class_="SQnoC3ObvgnGjWt90zD9Z")

        # Iterate through the div elements and filter based on your criteria
        for i in range(min(len(link_elements), 15)):
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
        ["relationship_advice", 2, 6], ["relationships", 1, 6],
        ["confessions", 2, 6], 
        ["TrueOffMyChest", 1, 6], ["offmychest", 3, 6],
        ["tifu", 1, 6], ["legaladvice", 1, 6], 
        ["AmItheAsshole", 3, 6], ["AITAH", 4, 6],  
        # ["askreddit", 4, 6]
    ]

    for subreddit in subreddits:
        # if current_date.weekday() == subreddit[2]:
        if True:
            url = f"https://www.reddit.com/r/{subreddit[0]}/top/?t=week"
            download_path = f"RedditPosts/{today}"
            scrape(url, download_path, subreddit)

    # Close the browser
    driver.quit()