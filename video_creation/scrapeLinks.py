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
from nltk.tokenize import sent_tokenize

def add_current_part(current_part, sentence_parts):
    if current_part:
        sentence_parts.append(', '.join(current_part))

def split_sentences_at_comma(sentence):
    # Initialize variables
    max_length = 40
    sentence_parts = []
    current_part = []

    # Split the sentence by commas while maintaining the character limit
    for word in sentence.split(','):
        word = word.strip()  # Remove leading/trailing spaces

        # Check if adding the word to the current part exceeds the character limit
        if len(' '.join(current_part)) <= max_length:
            current_part.append(word)
        else:
            # Add the current part to sentence_parts
            add_current_part(current_part, sentence_parts)
            current_part.clear()
            current_part.append(word)  # Add the word to a new part

    # Add any remaining part to sentence_parts
    add_current_part(current_part, sentence_parts)

    # Print the split sentences
    return sentence_parts



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
        time.sleep(1)
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
                split_up = split_sentences_at_comma(sentence)
                for sentence_part in split_up:
                    getOneLine(sentence_part, output_file)
        

    except Exception as e:
        print("An error occurred:", str(e))
  

if __name__ == "__main__":
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
