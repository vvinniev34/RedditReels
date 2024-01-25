# RedditReels (readme and requirements is outdated, will update sometime soon)

RedditReels is an automated video creator/uploader for YouTube Shorts, Instagram Reels, and Tiktok, specializing in short-form video content, particularly Reddit-style narration videos layered over video gameplay. 

This script is designed to run independently every week.

# Setup/Installation

1. Within project directory, run the following command: ```$ pip install -r requirements.txt```
   
2. Download the following dependencies if not on machine: [Microsoft EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH) | [FFmpeg](https://ffmpeg.org/download.html) | [ImageMagick](https://imagemagick.org/script/download.php)
   
3. Setup [Microsoft Azure](https://azure.microsoft.com/en-us/products/ai-services/text-to-speech) account and Speech Services. 
   - If tiktok voices or pytt3x are sufficient, uncomment corresponding imports and code blocks in the ./TextToSpeech.py file.
   - OpenAI voices are also available if an account already exists
   
4. Follow instructions within provided example .env to fill in necesary environment variables

# Usage/Instructions

1. Enter directory containing redditReels
   
2. Run the following command: ```$ python run.py```
   
3. Wait until script finishes. Created videos are contained within RedditPosts/{current_day} folder
   
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
