
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge import service
# from openai import OpenAI
# from accountCredentials.openai_key import OPENAI_API_KEY
from accountCredentials.reddit_account import reddit_username, reddit_password
from scrapeLinksHelpers import getAskRedditComments, remove_emojis
from datetime import date
import time
import os
import re

# s=service.Service(r"/Users/joshuakim/Downloads/MicrosoftWebDriver.exe")
s=service.Service(executable_path=r"edgedriver_win64/msedgedriver.exe")
driver = webdriver.Edge(service=s)
entire_post = ""

subreddits = {
    "relationships": 1, 
    "relationship_advice": 2, 
    "confessions": 2, 
    "TrueOffMyChest": 1, 
    "offmychest": 3,
    "tifu": 1, 
    "legaladvice": 1, 
    "AmItheAsshole": 3, 
    "AITAH": 4,  
    "askreddit": 4
}   

def check_id(id_name):
    try:
        driver.find_element(By.ID, id_name)
    except NoSuchElementException:
        return False
    return True

def check_class(class_name):
    try:
        driver.find_element(By.CLASS_NAME, class_name)
    except NoSuchElementException:
        return False
    return True


def check_selector(selector):
    try:
        driver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return False
    return True

from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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

def getContentLoggedIn(url, download_path, subreddit, number, custom):
    global subreddits
    if not custom and subreddits[subreddit] <= 0:
        # print(f"Reached quota for {subreddit}")
        return False

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # create the file
    filename = subreddit + str(number) + ".txt"
    output_file = os.path.join(download_path, filename)
    try:
        driver.get(url)
        driver.execute_script("return document.readyState")
        div_post = ""
        contentClass = "_3xX726aBn29LDbsDtzr_6E"
        div_post = driver.find_element(By.CLASS_NAME, contentClass)
        title_element = driver.find_element(By.TAG_NAME, "title")

        # title = title_element.get_attribute("text").split(':')[0].strip()
        title = title_element.get_attribute("text").rsplit(':', 1)[0].strip()
        if not title.endswith(('.', '!', '?', ';', ':')):
            title += '.'

        if title == 'Reddit - Dive into anything.':
            title_element = driver.find_element(By.XPATH, '//*[@id="t3_198rdnr"]/div/div[3]/div[1]/div/h1')
            title = title_element.get_attribute("text").rsplit(':', 1)[0].strip()
            if not title.endswith(('.', '!', '?', ';', ':')):
                title += '.'
            print(f"Default title found, replacing with {title}")

        if "update" in title.lower():
            print(f"Skipping post at url {url}: Update instead of new content")
            return False

        entire_post = title + "\n"

        if subreddit == "askreddit":
             # create a file and write the title to it
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(entire_post)
            return getAskRedditComments(output_file, url)

        # get all text into a variable
        p_elements = div_post.find_elements(By.TAG_NAME, "p")
        for p_element in p_elements:
            # Tokenize the input text into sentences
            entire_post += p_element.text + '\n'

        pattern = re.compile(r'edit:', re.IGNORECASE)
        match = pattern.search(entire_post)
        if match:
            entire_post = entire_post[:match.start()]
        pattern = re.compile(r'update:', re.IGNORECASE)
        match = pattern.search(entire_post)
        if match and (match.start() > (len(entire_post) / 4)):
            entire_post = entire_post[:match.start()]
        pattern = re.compile(r'edited to:', re.IGNORECASE)
        match = pattern.search(entire_post)
        if match and (match.start() > (len(entire_post) / 4)):
            entire_post = entire_post[:match.start()]

        entire_post = entire_post
        # entire_post = title + '.\n' + completion.choices[0].message.content
        entire_post = remove_emojis(entire_post)

        if len(entire_post) < 1000 or len(entire_post) > 4000:
            print(f"Post at {url} is too short or long with {len(entire_post)} characters, skipping...")
            return False

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(entire_post)
        
        subreddits[subreddit] -= 1
        return True
    
    except Exception as e:
        print("An error occurred:", str(e))
        return False

if __name__ == "__main__":
    # Define the URL of the Reddit page you want to scrape
    # today = date.today().strftime("%Y-%m-%d")
    # today = "2023-09-02"

    # url = "https://www.reddit.com/r/AmItheAsshole/comments/167chip/aita_for_not_disclosing_to_my_daughter_she_wasnt/"
    # getContent(url, "", "", "")

    # Define the URL of the Reddit page you want to scrape
    today = date.today().strftime("%Y-%m-%d")
    # today = "2024-01-18"
    # today = "Custom"

    login()
    custom = True if today == "Custom" else False
    filePath = f"RedditPosts/{today}/links.txt"
    download_path = f"RedditPosts/{today}/Texts"
    file = open(filePath, 'r')
    links = file.readlines()
    subreddit = "TIFU"
    count = 1
    for link in links:
        if link.strip():
            tryLink = "https://" + link
            path = download_path + '/' + subreddit
            if "reddit.com" in tryLink:
                # print(link)
                if getContentLoggedIn(tryLink, path, subreddit, count, custom):
                    count += 1
            else:
                subreddit = link.strip()
                count = 1

    # Close the browser
    driver.quit()