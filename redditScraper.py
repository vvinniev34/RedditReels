import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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


# Set up Chrome WebDriver with the desired user agent
chrome_options = Options()
chrome_options.add_argument(f"user-agent={user_agents[1]}")
driver = webdriver.Chrome()


def scrape(url):
    # Check if the request was successful by ensuring the page title contains "reddit"
    try:
        # Send an HTTP GET request to the URL using Selenium
        driver.get(url)
        # Wait for the page to load (adjust the wait time as needed)
        time.sleep(10)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_1poyrkZ7g36PawDueRza")))

        print("found")
        # Get the page source (HTML content) using Selenium
        page_source = driver.page_source

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all <div> elements with the specified class
        div_elements = soup.find_all("div", class_="_1poyrkZ7g36PawDueRza-J")

        count = 0
        # Iterate through the div elements and filter based on your criteria
        for div_element in div_elements:
            if count == 10:
                break
            print("outer for loop")
            # FILTER OUT PROMOTED ADS

            # Find nested div elements with class "_14-YvdFiW5iVvfe5wdgmET"
            nested_div = div_element.find("div", class_="_14-YvdFiW5iVvfe5wdgmET")
            # Find the div with class "cZPZhMe-UCZ8htPodMyJ5"
            inner_div = nested_div.find("div", class_="cZPZhMe-UCZ8htPodMyJ5")
            # Find the span with class "_3AStxql1mQsrZuUIFP9xSg"
            inner_span = inner_div.find("span", class_="_3AStxql1mQsrZuUIFP9xSg")
            # Check if the inner span contains a span with the text "Promoted"
            if inner_span and "Promoted" in inner_span.text:
                continue  # Skip this div as it contains the "Promoted" span

            # NORMAL POST
            else:
                nested_div = div_element.find("div", class_="_2FCtq-QzlfuN-SwVMUZMM3")
                inner_div = nested_div.find("div", class_="y8HYJ-y_lTUHkQIc1mdCq")
                link = inner_div.find("a", class_="SQnoC3ObvgnGjWt90zD9Z").get("href")
                print(link)
            count += 1
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Define the URL of the Reddit page you want to scrape
    url = "https://www.reddit.com/r/tifu/top/?t=week"
    scrape(url)