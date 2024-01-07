import requests
import json
import demoji

MAX_COMMENTS = 5

def remove_emojis(text):
    return demoji.replace(text, '')

def getAskRedditComments(output_file, url):
    # Send a GET request to the URL
    response = requests.get(f"{url}.json")
    if response.status_code == 200:
        # Parse the HTML content using Beautiful Soup
        data = response.json()

        i = 0
        top_comments = []
        for thread in data[1]["data"]["children"]:
            thread_data = thread["data"]
            if "body" in thread_data:
                top_thread_body = thread_data["body"]
                top_comments.append(remove_emojis(top_thread_body))

                with open(output_file, 'a', encoding='utf-8') as file:
                    file.write(str(top_thread_body) + "\n\n")

            i += 1
            if (i >= 5):
                break
        return True
    else:
        print(f"Failed to fetch the URL. Status code: {response.status_code}")
        return False