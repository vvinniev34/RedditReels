from tiktok_uploader.upload import upload_video
import argparse
from datetime import datetime, date, timedelta
import re
from typing import Optional
import time

FILENAME = "/Users/joshuakim/Downloads/TIFU_thinking_I_p1.mp4"

current_time = datetime.now()
month = current_time.month
day = current_time.day
year = current_time.year
hour = current_time.hour
minutes = current_time.minute
SCHEDULE_DATE = f"{month}/{day}/{year}, {hour}:{minutes}"

dates = [datetime.datetime(year, day, 12, 00, 00), datetime.datetime(year, day, 17, 30, 00), datetime.datetime(year, day, 00, 00, 00) + timedelta(days=1)]
curr = 0
days_since = 0

def getNextSchedule():
    global SCHEDULE_DATE
    date = SCHEDULE_DATE.split(',')[0].strip().split("/")
    month, day, year = map(int, date)
    time = SCHEDULE_DATE.split(',')[1].strip().split(":")
    hour, minutes = map(int, time)
    if (hour < 12):
        SCHEDULE_DATE = f"{month}/{day}/{year}, 12:00"
        return datetime.datetime(year, month, day, 12, 00, 00)
    elif (hour < 17 or (hour <= 17 and minutes < 30)):
        SCHEDULE_DATE = f"{month}/{day}/{year}, 17:30"
        return datetime.datetime(year, month, day, 17, 30, 00)
    else:
        next_day = datetime(year=year, month=month, day=day) + timedelta(days=1)
        year = next_day.year
        month = next_day.month
        day = next_day.day
        SCHEDULE_DATE = f"{month}/{day}/{year}, 00:00"
        return datetime.datetime(year, month, day, 00, 00, 00)

def remove_ending(string):
    pattern_with_part = r"_p\d+\.mp4"
    pattern_long_form = r"\.mp4"
    modified_string = re.sub(pattern_with_part, '', string)
    modified_string = re.sub(pattern_long_form, '', modified_string)
    return modified_string

def get_max_title(title):
    valid_title = ""
    title_words = title.split()
    for word in title_words:
        if len(valid_title) + len(word) + 1 <= 100:
            valid_title += (word + " ")
        else:
            break
    return valid_title.strip()

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    today = "2024-01-12"

    TIKTOK_UPLOADS = []
    with open(f"../RedditPosts/{today}/uploadQueue/tiktok_queue.txt", "r", encoding="utf-8") as file:
        file_contents = file.read()
        TIKTOK_UPLOADS = file_contents.split('\n')
        TIKTOK_UPLOADS = [upload for upload in TIKTOK_UPLOADS if upload]

    used_uploads = []
    max_uploads = 21
    for upload in TIKTOK_UPLOADS:
        subreddit = upload.split("/")[3]
        video_num = upload.split("/")[4]
        title = "redditstory"
        with open(f"../RedditPosts/{today}/Texts/{subreddit}/{video_num}/videoTitle.txt", "r", encoding="utf-8") as file:
            title = file.readline().strip()
        title = get_max_title(title) + f"{title}\n\n#shorts #redditstories #{subreddit} #cooking"
        schedule = getNextSchedule()

        upload_video(upload,
                 description="title",
                 cookies="cookies/tiktokcookies.txt", schedule=schedule)

        used_uploads.append(upload)
        max_uploads -= 1
        if max_uploads <= 0:
            break

        time.sleep(5)

    remaining_tiktok_uploads = [upload for upload in TIKTOK_UPLOADS if upload not in used_uploads]
    with open(f"../RedditPosts/{today}/uploadQueue/tiktok_queue.txt", "w", encoding="utf-8") as file:
        file.writelines('\n'.join(remaining_tiktok_uploads))
