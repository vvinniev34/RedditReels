# RedditReels
Scrapes top daily posts daily on reddit and creates short-form video content for TikTok, Youtube Shorts, Instagram Reels, etc...

# Overview

RedditReels functions as an automated video creator and uploader for YouTube Shorts, specializing in short-form video content, particularly Reddit-style narration videos layered over video gameplay. This script autonomously fetches the top 15 weekly posts from chosen subreddits, converting them into short-form video content for seamless uploading. Subsequently, it handles the uploading process to YouTube channels managed by the user, all without any need for further user interaction. 

This script is designed to run independently every week.

# How It Works

1. **Subreddit Selection and Weekly Scraping:**
   - The script selects specific subreddits for content sourcing.
   - It automatically scrapes the top 15 most popular posts from these subreddits on a weekly basis using Selenium and Beautiful Soup, posting the results into a .txt file within a folder managed by the script. 

2. **Video Content Creation:**
   - Automatically transforms the extracted content into short-form video clips suitable for YouTube Shorts.
   - Transforms posted results from .txt file contents into .mp3 format, or the narration in the short-form video, using Python pytt3x and pydub libraries
   - The script randomly selects a segment from tailored gameplay, matching the length of the TTS .mp3. Narration from the generated .mp3 is then overlayed using the Python moviePy library and text matching the TTS speech is superimposed upon the video using the ffmpeg command line tool.

3. **YouTube Upload and Management:**
   - Uploads the generated videos to YouTube channels managed by the user.
   - Handles video metadata, descriptions, and scheduling.

Overall, RedditReels is an automated script designed to streamline the process of creating and uploading short-form video content to YouTube Shorts. It operates without the need for user intervention and runs on a weekly schedule. 

# Setup

**MSEDGEDRIVER**
- Download Microsft Edge webdriver using https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ and place executable in working directory and edit the _edge_driver_path_ variable in topKWeeklyPostsScraper.py file to match the relative path to the edge driver executable. 

**FFMPEG**
- Download ffmpeg command line tool using https://ffmpeg.org/. Ensure downloaded file is in either in System PATH or within working directory. Edit the _ffmpeg_exe_path_ variable in videoMaker.py file to match ffmpeg executable location. 

**Google Cloud Platform**
- Register application on Google Cloud Platform to enable OAuth 2.0 and enable Youtube Data API for the project. Place a generated OAuth clientID .json file in the working directory and edit the _CLIENT_SECRETS_FILE_ variable in uploadVideo.py to match the absolute path to the .json generated. 

**PIP INSTALL**
- selenium
- bs4
- gtts
- pydub
- pyttsx3
- moviepy
- googleapiclient
- oauth2client

# Instructions
