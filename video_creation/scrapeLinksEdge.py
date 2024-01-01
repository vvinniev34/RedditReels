
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge import service
from openai import OpenAI
from datetime import date
# client = OpenAI()

import time
import os
import nltk
# nltk.download('punkt')  # Download the Punkt tokenizer data (only needs to be done once)
from nltk.tokenize import sent_tokenize

s=service.Service(r"/Users/joshuakim/Downloads/MicrosoftWebDriver.exe")
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


def getContent(url, download_path, subreddit, number):
    # if not os.path.exists(download_path):
    #     os.makedirs(download_path)

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
        entire_post = title + '\n'

        div_post = ""
        if check_id(contentId):
            div_post = driver.find_element(By.ID, contentId)
        else:
            return False
        # filter out non alphabet characters for the text file
        # filename = subreddit + str(number) + ".txt"

        # create a file and write the title to it
        # output_file = os.path.join(download_path, filename)
        # with open(output_file, 'w') as file:
            # file.write(title)
            # file.write("\n")
    
        
        # get all text into a variable
        p_elements = div_post.find_elements(By.TAG_NAME, "p")
        for p_element in p_elements:
            # Tokenize the input text into sentences
            entire_post += p_element.text + '\n'

        # prompt = "Can you edit this text to get rid of grammar errors and to shorten long sentences?" + '\n' + entire_post
        # client = OpenAI()

        # completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # messages=[
        #     {"role": "system", "content": "You are a writing assistant, skilled in correcting grammatical errors and reviewing texts."},
        #     {"role": "user", "content": prompt}
        # ])
        # print(completion.choices[0].message.content)
            
        print(entire_post)
        return True
    except Exception as e:
        print("An error occurred:", str(e))
  

if __name__ == "__main__":
    # Define the URL of the Reddit page you want to scrape
    # today = date.today().strftime("%Y-%m-%d")
    # today = "2023-09-02"


    # url = "https://www.reddit.com/r/AmItheAsshole/comments/167chip/aita_for_not_disclosing_to_my_daughter_she_wasnt/"
    # getContent(url, "", "", "")

    # Define the URL of the Reddit page you want to scrape
    # today = date.today().strftime("%Y-%m-%d")
    today = "2023-09-02"

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
                getContent(tryLink, path, subreddit, count)
                count += 1
            else:
                subreddit = link.strip()
                count = 1
