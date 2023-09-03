from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.safari.options.Options()
driver = webdriver.Safari(options=options)


def scrape(url):
    # Check if the request was successful by ensuring the page title contains "reddit"
    try:
        driver.get(url)
        time.sleep(5)
        # Wait for the button to be clickable (you can specify a timeout in seconds)
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "t3_ocx94s-read-more-button"))
        )

      # Click the button
        button.click()
        time.sleep(5)
        div_post = driver.find_element(By.ID, "t3_ocx94s-post-rtjson-content")
        
        p_elements = div_post.find_elements(By.TAG_NAME, "p")
        for p_element in p_elements:
            print(p_element.text)
        

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    # Define the URL of the Reddit page you want to scrape
    url = "https://www.reddit.com/r/AmItheAsshole/comments/ocx94s/aita_for_telling_my_wife_the_lock_on_my_daughters/?rdt=38827"
    scrape(url)