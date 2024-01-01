import os
import subprocess

if __name__ == "main":
    # Run the Python files
    # get top weekly posts
    subprocess.run(["python", "topKWeeklyPostsScraper.py"])
    # get post content
    subprocess.run(["python", "scrapeLinks.py"])
    # convert post content to mp3
    subprocess.run(["python", "textToSpeech.py"])
    # create videos
    subprocess.run(["python", "textOverlay.py"])

    # upload videos
    # today = date.today().strftime("%Y-%m-%d")
    today = "2023-09-02"
    folder_path = f"RedditPosts/{today}/Texts"
    for subreddit in os.listdir(folder_path):
        post_path = f"{folder_path}/{subreddit}"
        for post in os.listdir(post_path):
            if post.endswith("F.mp3"):
                subprocess.run(["python", "uploadVideo", "--file", f"{post_path}/{post}"])