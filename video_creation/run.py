import os
import subprocess

if __name__ == "__main__":
    # Run the Python files
    # get top weekly posts
    subprocess.run(["python", "./topKWeeklyPostsScraper.py"])
    # get post content
    subprocess.run(["python", "./scrapeLinks.py"])
    # convert post content to mp3
    subprocess.run(["python", "./textToSpeech.py"])
    # create videos
    subprocess.run(["python", "./textOverlay.py"])
    # upload videos to YouTube
    subprocess.run(["python", "./youtube_upload/upload.py"])
