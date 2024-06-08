import argparse
from datetime import datetime, date, timedelta
import re
from helpers import YouTubeUploader
from typing import Optional
import time

from firefox_profile import FIREFOX_PROFILE

current_time = datetime.now()
month = current_time.month
day = current_time.day
year = current_time.year
hour = current_time.hour
minutes = current_time.minute
SCHEDULE_DATE = f"{month}/{day}/{year}, {hour}:{minutes}"

# check if string contains "_p{number}.mp4" or ".mp4" and remove
def remove_ending(string):
    pattern_with_part = r"_p\d+\.mp4"
    pattern_long_form = r"\.mp4"
    modified_string = re.sub(pattern_with_part, '', string)
    modified_string = re.sub(pattern_long_form, '', modified_string)
    return modified_string

def contains_pattern(string):
    pattern = re.compile(r"_p\d+\.mp4")
    return bool(pattern.search(string))

def get_max_title(title):
    valid_title = ""
    title_words = title.split()
    for word in title_words:
        if len(valid_title) + len(word) + 1 <= 100:
            valid_title += (word + " ")
        else:
            break
    return valid_title.strip()

def getNextSchedule():
    global SCHEDULE_DATE
    date = SCHEDULE_DATE.split(',')[0].strip().split("/")
    month, day, year = map(int, date)
    time = SCHEDULE_DATE.split(',')[1].strip().split(":")
    hour, minutes = map(int, time)

    if (hour < 12):
        SCHEDULE_DATE = f"{month}/{day}/{year}, 12:00"
    elif (hour < 17 or (hour <= 17 and minutes < 30)):
        SCHEDULE_DATE = f"{month}/{day}/{year}, 17:30"
    else:
        next_day = datetime(year=year, month=month, day=day) + timedelta(days=1)
        year = next_day.year
        month = next_day.month
        day = next_day.day
        SCHEDULE_DATE = f"{month}/{day}/{year}, 00:00"
    return SCHEDULE_DATE

def getNextDaySchedule():
    global SCHEDULE_DATE
    date = SCHEDULE_DATE.split(',')[0].strip().split("/")
    month, day, year = map(int, date)
    time = SCHEDULE_DATE.split(',')[1].strip().split(":")
    hour, minutes = map(int, time)

    next_day = datetime(year=year, month=month, day=day) + timedelta(days=1)
    year = next_day.year
    month = next_day.month
    day = next_day.day
    SCHEDULE_DATE = f"{month}/{day}/{year}, 00:00"
    return SCHEDULE_DATE

def main(video_path: str,
         metadata_path: Optional[str] = None,
         thumbnail_path: Optional[str] = None,
         profile_path: Optional[str] = None):
    uploader = YouTubeUploader(video_path, metadata_path, thumbnail_path, profile_path)
    was_video_uploaded, video_id = uploader.upload()
    return was_video_uploaded


if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    today = "2024-01-12"

    YOUTUBE_UPLOADS = []
    with open(f"../RedditPosts/{today}/uploadQueue/youtube_queue.txt", "r", encoding="utf-8") as file:
        file_contents = file.read()
        YOUTUBE_UPLOADS = file_contents.split('\n')
        YOUTUBE_UPLOADS = [upload for upload in YOUTUBE_UPLOADS if upload]

    used_uploads = []
    max_uploads = 20
    for upload in YOUTUBE_UPLOADS:
        # skip multiple part videos, might remove might keep
        if contains_pattern(upload):
            continue

        subreddit = upload.split("/")[3]
        video_num = upload.split("/")[4]
        title = "redditstory"
        with open(f"../RedditPosts/{today}/Texts/{subreddit}/{video_num}/videoTitle.txt", "r", encoding="utf-8") as file:
            title = file.readline().strip()
        json = {
            "title": get_max_title(title),
            "description": f"{title}\n\n#shorts #redditstories #{subreddit} #cooking",
            "tags": [],
            # "schedule": f"{getNextSchedule()}"
            "schedule": f"{getNextDaySchedule()}"
        }

        if not main(upload, json, profile_path=FIREFOX_PROFILE):
            break

        used_uploads.append(upload)
        max_uploads -= 1
        if max_uploads <= 0:
            break

        time.sleep(2)

    # remaining_youtube_uploads = [upload for upload in YOUTUBE_UPLOADS if upload not in used_uploads]
    # with open(f"../RedditPosts/{today}/uploadQueue/youtube_queue.txt", "w", encoding="utf-8") as file:
    #     file.writelines('\n'.join(remaining_youtube_uploads))
