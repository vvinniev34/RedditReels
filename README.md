# RedditReels
Automates creation of short-form video content for TikTok, YouTube Shorts, etc, using top weekly Reddit posts with upcoming support for automatic script execution scheduling

# Overview (readme and requirements is outdated, will update sometime soon)

RedditReels is an automated video creator/uploader for YouTube Shorts, Instagram Reels, and Tiktok, specializing in short-form video content, particularly Reddit-style narration videos layered over video gameplay. This script autonomously fetches the top weekly posts from chosen subreddits, converting them into short-form video content for seamless uploading. 

This script is designed to run independently every week.

# Setup/Installation

1. Within project directory, either run $ pip install -r requirements.txt or pip install the following dependencies:
   - azure-cognitiveservices-speech
   - whisper_timestamped
   - pydub
   - wave
   - moviepy
   - selenium_firefox==2.0.8
   - selenium==4.0.0
   - bs4
   - demoji
   - requests
   - python-dotenv

2. Download Microsoft EdgeDriver using the following link: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/. Place path to .exe within a .env within working direcotry with key value EDGE_DRIVER_PATH. 
3. Download ffmpeg command line tool using https://ffmpeg.org/. Ensure downloaded .exe file is in either in System PATH or within working directory
4. Setup Microsoft Azure account and Speech Services. Place the corresponding SPEECH_KEY and SPEECH_REGION within the .env file
   - https://azure.microsoft.com/en-us/products/ai-services/text-to-speech
   - If tiktok voices or pytt3x are sufficient, uncomment corresponding imports and portions in the ./TextToSpeech.py file.
   - OpenAI voices are also available if an account already exists
6. Place Reddit account username and password into the .env file with corresponding keys values, REDDIT_USERNAME and REDDIT_PASSWORD

Summary:
Install dependencies and ensure .env file is properly setup. An example is provided within code. 

# Usage/Instructions

1. Enter directory containing redditReels
3. Run $ python run.py
4. Wait until script finishes, created videos are contained within RedditPosts/{current_day} folder
   
# How It Works

1. **Subreddit Selection and Weekly Scraping:**
   - The script selects specific subreddits for content sourcing.
   - It automatically scrapes the top 15 most popular posts from these subreddits on a weekly basis using Selenium and Beautiful Soup, posting the results into a .txt file within a folder managed by the script. 

2. **Video Content Creation:**
   - Transforms the extracted text content into short-form video clips suitable for Tiktok, Reels, and Shorts.
   - Transforms posted results from .txt file contents into .wav format, using the chosen TTS service (Azure, pytt3x, tiktok API, openAI)
   - The script randomly selects a segment from tailored video gameplay, matching the length of the TTS .wav. Text captioning from the generated .wav is then overlayed using the Python moviePy library using openAI Whisper API to transcribe timestamps upon captions.

3. **YouTube Upload and Management:**
   - more requirements needed, will update later
   - Uploads the generated videos to YouTube channels managed by the user.
   - Handles video metadata, descriptions, and scheduling.

