
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge import service
from openai import OpenAI
from accountCredentials.openai_key import OPENAI_API_KEY
from accountCredentials.reddit_account import reddit_username, reddit_password
from scrapeLinksHelpers import getAskRedditComments, remove_emojis
from datetime import date
import time
import os
import re

# s=service.Service(r"/Users/joshuakim/Downloads/MicrosoftWebDriver.exe")
s=service.Service(r"edgedriver_win64/msedgedriver.exe")
driver = webdriver.Edge(service=s)
entire_post = ""

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

def getContentLoggedIn(url, download_path, subreddit, number):
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

        entire_post = entire_post
        # entire_post = title + '.\n' + completion.choices[0].message.content
        entire_post = remove_emojis(entire_post)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(entire_post)
        return True
    
    except Exception as e:
        print("An error occurred:", str(e))
        return False


def getContent(url, download_path, subreddit, number):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Check if the request was successful by ensuring the page title contains "reddit"
    try:
        driver.get(url)
        entire_post = ""
        driver.execute_script("return document.readyState")

        # get the post ID from the share button
        idString = driver.find_element(By.TAG_NAME, "shreddit-post")
        postId = idString.get_attribute("id")
        # add the post ID where it should be for the title, content, and button
        titleId = "post-title-" + postId
        contentId = postId + "-post-rtjson-content"
        more_button_id = postId + "-read-more-button"

        # click read more if possible
        try:
            driver.find_element(By.ID, more_button_id).click()
        except Exception as e:
            pass
        # get the title and post
        post_title = driver.find_element(By.ID, titleId)
        title = post_title.text
        
        if not title.strip().endswith(('.', '!', '?', ';', ':')):
            title += '.'

        div_post = ""
        if check_id(contentId):
            div_post = driver.find_element(By.ID, contentId)
        else:
            return False
        
        # get all text into a variable
        p_elements = div_post.find_elements(By.TAG_NAME, "p")
        for p_element in p_elements:
            # Tokenize the input text into sentences
            entire_post += p_element.text + '\n'

        pattern = re.compile(r'edit:', re.IGNORECASE)
        match = pattern.search(entire_post)
        if match:
            entire_post = entire_post[:match.start()]

        # prompt = "Can you edit this text to get rid of grammar errors and to shorten long sentences?" + '\n' + entire_post
        # # client = OpenAI()
        # client = OpenAI(api_key=OPENAI_API_KEY)

        # completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # messages=[
        #     {"role": "system", "content": "You are a writing assistant, skilled in correcting grammatical errors and reviewing texts."},
        #     {"role": "user", "content": prompt}
        # ]) 

        # create the file
        filename = subreddit + str(number) + ".txt"

        entire_post = title + '.\n' + entire_post
        # entire_post = title + '.\n' + completion.choices[0].message.content
        entire_post = remove_emojis(entire_post)

        # create a file and write the title to it
        output_file = os.path.join(download_path, filename)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(entire_post)
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
    # today = "2023-09-02"
    # today = "Test"
    login()

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
                if getContentLoggedIn(tryLink, path, subreddit, count):
                    count += 1
            else:
                subreddit = link.strip()
                count = 1
