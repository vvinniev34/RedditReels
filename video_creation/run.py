import os
import subprocess

if __name__ == "main":
    # Run the Python files
    subprocess.run(["python", "topKWeeklyPostsScraper.py"])
    subprocess.run(["python", "scrapeLinks.py"])
    subprocess.run(["python", "textToSpeech.py"])
    subprocess.run(["python", "videoMaker.py"])

    today = "2023-09-02"
    folder_path = f"RedditPosts/{today}/Texts"
    for subreddit in os.listdir(folder_path):
        post_path = f"{folder_path}/{subreddit}"
        for post in os.listdir(post_path):
            if post.endswith("F.mp3"):
                subprocess.run(["python", "uploadVideo", "--file", f"{post_path}/{post}"])