from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import os
import unicodedata

printable = {'Lu', 'Ll'}
def filter_non_printable(str):
  return ''.join(c for c in str if unicodedata.category(c) in printable)


options = webdriver.safari.options.Options()
driver = webdriver.Safari(options=options)

def getContent(url, download_path, subreddit, number):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Check if the request was successful by ensuring the page title contains "reddit"
    try:
        driver.get(url)

        # get the post ID from the share button
        idString = driver.find_element(By.TAG_NAME, "embed-snippet-share-button")
        postId = idString.get_attribute("postid")

        # add the post ID where it should be for the title, content, and button
        titleId = "post-title-" + postId
        contentId = postId + "-post-rtjson-content"

        # get the title and post
        div_post = driver.find_element(By.ID, contentId)
        post_title = driver.find_element(By.ID, titleId)
        title = post_title.text
        # filter out non alphabet characters for the text file
        filename = subreddit + str(number) + ".txt"

        # create a file and write the title to it
        output_file = os.path.join(download_path, filename)
        with open(output_file, 'a') as file:
            file.write(title)
            file.write("\n")
        
        # write the post to the file
        p_elements = div_post.find_elements(By.TAG_NAME, "p")
        for p_element in p_elements:
            with open(output_file, 'a') as file:
                file.write(p_element.text)
                file.write("\n")
        

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    # Define the URL of the Reddit page you want to scrape
    url = "https://www.reddit.com/r/tifu/comments/167v1hi/tifu_by_making_a_porn_video_without_even_knowing/"
    today = date.today().strftime("%Y-%m-%d")
    download_path = f"redditPosts/{today}/Texts"
    getContent(url, download_path)