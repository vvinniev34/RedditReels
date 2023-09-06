from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time
import os
import nltk
nltk.download('punkt')  # Download the Punkt tokenizer data (only needs to be done once)
from nltk.tokenize import sent_tokenize, word_tokenize

conjunctions = {", and", ", but", ", or", ", so", ", yet", ", nor"}
def split_sentences_at_conjunctions(sentence):
    split_sentences = []
    
    for conjunction in conjunctions:
        if conjunction in sentence:
            parts = sentence.split(conjunction, 1)  # Split at the first occurrence
            if len(parts) == 2:
                split_sentences.extend([parts[0].strip(), conjunction[2 : len(conjunction)] + " " + parts[1].strip() + "."])
            break
    if split_sentences == []:
        split_sentences.append(sentence)
    
    return split_sentences



options = webdriver.safari.options.Options()
driver = webdriver.Safari(options=options)

def getOneLine(line, output_file):
    with open(output_file, 'a') as file:
        file.write(line)
        file.write("\n")

def getContent(url, download_path, subreddit, number):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Check if the request was successful by ensuring the page title contains "reddit"
    try:
        driver.get(url)
        time.sleep(2)
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
        with open(output_file, 'w') as file:
            file.write(title)
            file.write("\n")
        
        # write the post to the file
        p_elements = div_post.find_elements(By.TAG_NAME, "p")
        for p_element in p_elements:
            # Tokenize the input text into sentences
            sentences = sent_tokenize(p_element.text)

            for sentence in sentences:
                split_up = split_sentences_at_conjunctions(sentence)
                for sentence_part in split_up:
                    getOneLine(sentence_part, output_file)
        

    except Exception as e:
        print("An error occurred:", str(e))
  

if __name__ == "__main__":
    # Define the URL of the Reddit page you want to scrape
    today = date.today().strftime("%Y-%m-%d")

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
