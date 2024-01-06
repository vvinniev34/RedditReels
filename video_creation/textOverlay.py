import random
import os
import re
import string
from datetime import date
import subprocess
import whisper_timestamped as whisper
from moviepy.editor import VideoFileClip, ImageClip, TextClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, concatenate_videoclips
from fileDetails import get_mp3_length, add_mp3_padding, adjust_mp4_volume
from generateClips import createTitleClip, createTextClip

# Get the current working directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the relative path to ffmpeg.exe
ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg-2023-08-30-git-7aa71ab5c0-full_build", "bin", "ffmpeg.exe")

model = whisper.load_model("base")

def replace_abbreviations(sentence):
    pattern_aita = r'\bada\b'
    pattern_tifu1 = r'\btyphoo\b'
    pattern_tifu2 = r'\bTIF(?:\s*,*\s*)you\b'
    
    modified_sentence = re.sub(pattern_aita, 'AITA', sentence, flags=re.IGNORECASE)
    modified_sentence = re.sub(pattern_tifu1, 'TIFU', modified_sentence, flags=re.IGNORECASE)
    modified_sentence = re.sub(pattern_tifu2, 'TIFU', modified_sentence, flags=re.IGNORECASE)

    return modified_sentence

def splitTextForWrap(input_str: str, line_length: int):
    words = input_str.split(" ")
    line_count = 0
    split_input = ""
    line = ""
    i = 0
    for word in words:
        # long word case
        if (line_count == 0 and len(word) >= line_length):
            split_input += (word + ("\n" if i < (len(words) - 1) else ""))
        elif (line_count + len(word) + 1) > line_length:
            paddingNeeded = line_length - line_count
            alternatePadding = True
            while (paddingNeeded > 0):
                if alternatePadding:
                    line = "\u00A0" + line
                else:
                    line = line + "\u00A0"
                alternatePadding = not alternatePadding
                paddingNeeded -= 1
            line += "\n"

            split_input += line
            line = word
            line_count = len(word)
        else:
            line += ("\u00A0" + word) 
            line_count += len(word) + 1
        i += 1
    
    paddingNeeded = line_length - line_count
    alternatePadding = True
    while (line_count != 0 and paddingNeeded > 0):
        if alternatePadding:
            line = "\u00A0" + line
        else:
            line = line + "\u00A0"
        alternatePadding = not alternatePadding
        paddingNeeded -= 1
    split_input += line
    return split_input

def randomVideoSegment(output_video_filepath, duration):
    background_video_path = "backgroundVideos/minecraft_parkour.mp4"
    total_duration_seconds = 60 * 60 # minecraft parkour
    dark_theme_subreddits = ["nosleep", "letsnotmeet", "glitch_in_the_matrix", "creepyencounters"]
    if any(text.lower() in output_video_filepath.lower() for text in dark_theme_subreddits):
        background_video_path = "backgroundVideos/nighttime_minecraft_parkour.mp4"
        total_duration_seconds = 33 * 60 + 33 # nightime minecraft parkour

    random_start_time_seconds = random.uniform(0, total_duration_seconds - duration)
    video_clip = VideoFileClip(background_video_path)
    random_segment = video_clip.subclip(random_start_time_seconds, random_start_time_seconds + duration)
    random_segment.write_videofile(output_video_filepath, codec="libx264", threads=8, logger = None, preset='ultrafast')
    print(f"Snipped {duration} s length video starting at: {random_start_time_seconds} for {output_video_path.split('/')[-1]}")


def overlayText(mp3_file_path, mp3_title_file_path, video_path, post_path, postName):
    partNum = 0 
    mp3_duration = get_mp3_length(mp3_file_path)

    video_title_path = f"{mp4_file_path.split('.')[0]}/videoTitle.txt"
    video_title = "Errors Reading From Title"
    with open(video_title_path, 'r', encoding='utf-8') as file:
        video_title = file.read().strip()
        # print(video_title)
    title_duration = get_mp3_length(mp3_title_file_path)

     # if more than a 6 parter, create long form content intead
    long_form = False
    if (mp3_duration + title_duration) >= 180:
        long_form = True
    multipleParts = title_duration + mp3_duration > 60

    b_clip, title_clip, banner_clip, comment_clip = createTitleClip(video_title + (" (p1)" if multipleParts and not long_form else ""), 0, title_duration)
    
    # title_last_word_time = 0
    # title_audio = whisper.load_audio(mp3_title_file_path)
    # title_audio_result = whisper.transcribe(model, title_audio, 'en')
    # for segment in title_audio_result['segments']:
    #     title_last_word_time = segment['end']

    audio = whisper.load_audio(mp3_file_path)
    result = whisper.transcribe(model, audio, 'en')

    start_time = 0
    currentVidTime = 0
    currentMaxVidTime = 60

    video_segments = [[[], []]]  # To store paths of individual video segments
    video_segments[partNum][1].append(0)
    video_segments[partNum][0].append(b_clip)
    video_segments[partNum][0].append(title_clip)
    video_segments[partNum][0].append(banner_clip)
    video_segments[partNum][0].append(comment_clip)

    video_clip = VideoFileClip(video_path)

    print(f"Overlaying Text on {postName}...")
    first_segment = True
    for segment in result['segments']:
        abbreviationFixedText = replace_abbreviations(segment['text'])
        if first_segment:
            first_segment = False

        # split segment into multiple if phrase is longer than 30 characters
        splitSegments = []
        if (len(abbreviationFixedText) <= 30 and (len(abbreviationFixedText) < 20 or len(abbreviationFixedText) > 21)):
            splitSegments.append([abbreviationFixedText, segment['end']])
        else:
            currentText = ""
            prevEnd = start_time
            for word in segment['words']:
                if (len(word['text']) + len(currentText) + 1) < 15:
                    currentText += (word['text'] + " ")
                else:
                    splitSegments.append([replace_abbreviations(currentText), prevEnd])
                    currentText = (word['text'] + " ")
                prevEnd = word['end']
            splitSegments.append([replace_abbreviations(currentText), prevEnd])
            if (prevEnd == -1):
                print("Invalid word, too many characters")
                return

        # create text overlay for each segment
        for split in splitSegments:
            text = split[0].strip()
            endTime = split[1]

            # wrappedText = splitTextForWrap(text.strip(), 15)
            wrappedText = text

            duration = endTime - start_time
            # print(f"{start_time} {start_time + duration} {duration}\n'{wrappedText}'")

            # if length is over 60 seconds, create a new part for the video
            if ((endTime + (title_duration + 1) * (partNum + 1)) > currentMaxVidTime and not long_form):
                video_segments[partNum][1].append(start_time)
                currentMaxVidTime += 60
                partNum += 1
                video_segments.append([[], []])
                video_segments[partNum][1].append(start_time)
                b_clip, title_clip, banner_clip, comment_clip = createTitleClip(video_title + f" (p{partNum + 1})", 0, title_duration)
                video_segments[partNum][0].append(b_clip)
                video_segments[partNum][0].append(title_clip)
                video_segments[partNum][0].append(banner_clip)
                video_segments[partNum][0].append(comment_clip)

                currentVidTime = 0

            new_textclip, shadow_textclip = createTextClip(wrappedText, currentVidTime, duration)

            video_segments[partNum][0].append(shadow_textclip)
            video_segments[partNum][0].append(new_textclip)

            # Update start time for the next segment
            start_time = endTime
            currentVidTime += duration

        # for video title testing purposes
        # if (currentVidTime > 6):
        #     break
    video_segments[partNum][1].append(start_time)

    audio_clip = AudioFileClip(mp3_file_path)

    # subclip to remove audio artifact, unusure why AudioFileclip makes, maybe a bug?
    title_audio_clip = AudioFileClip(mp3_title_file_path)
    # title_audio_clip.write_audiofile("temp.mp3", codec='mp3')
    # title_audio_clip = title_audio_clip.subclip(0, title_last_word_time)
    
    partNum = 1
    for part in video_segments:
        start_time = part[1][0]
        end_time = part[1][1]

        snipped_title_video = video_clip.subclip(0, title_duration) if partNum == 1 else video_clip.subclip(start_time, start_time + title_duration)
        # print(str(snipped_title_video.duration) + " " + str(title_last_word_time))
        snipped_title_audio_clip = title_audio_clip.subclip(0, -0.15)#.audio_fadeout(snipped_title_video.duration - title_last_word_time)
        
        snipped_video = video_clip.subclip(start_time + title_duration, end_time + title_duration)
        snipped_audio = audio_clip.subclip(start_time, end_time)

        title_video_with_text = snipped_title_video.set_audio(snipped_title_audio_clip)
        title_video_with_text = CompositeVideoClip([title_video_with_text] + part[0][:4])

        # title_video_with_text.write_videofile("temp.mp4", codec="libx264", threads=8, preset='ultrafast', logger = None)

        video_with_text = CompositeVideoClip([snipped_video] + part[0][4:])
        video_with_text = video_with_text.set_audio(snipped_audio)

        final_video_clip = concatenate_videoclips([title_video_with_text, video_with_text])
        
        # add dark theme to some subreddits and if it's not long form content
        dark_theme_subreddits = ["nosleep", "creepyencounters", "letsnotmeet", "glitch_in_the_matrix"]
        if any(text.lower() in postName.lower() for text in dark_theme_subreddits) and not long_form:
            # add snowfall background music for horror stories
            random_start_time_seconds = random.uniform(0, (15 * 60 + 28) - final_video_clip.duration)
            snowfall_audio = AudioFileClip("audio/snowfall_volume_boosted.mp3").subclip(random_start_time_seconds, random_start_time_seconds + final_video_clip.duration)
            final_audio = CompositeAudioClip([final_video_clip.audio, snowfall_audio])
            final_video_clip.audio = final_audio

        if not os.path.exists(f"{post_path}/{postName}"):
            os.makedirs(f"{post_path}/{postName}")
        output_video_path = f"{post_path}/{postName}/part{partNum}.mp4"
        print(f"Writing output video: {output_video_path}")
        final_video_clip.write_videofile(output_video_path, codec="libx264", threads=8, preset='ultrafast', logger = None)
        print(f"Finished writing part {partNum}")

        partNum += 1

    print("Overlay complete.")

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    # today = "2024-01-03"
    # today = "Test"
    folder_path = f"RedditPosts/{today}/Texts"
    for subreddit in os.listdir(folder_path):
        post_path = f"{folder_path}/{subreddit}"
        for post in os.listdir(post_path):
            if post.endswith(".mp3") and not post.endswith("title.mp3"):
                mp3_file_path = f"{post_path}/{post}"
                mp3_title_file_path = f"{post_path}/{post.split('.')[0]}_title.mp3"
                output_video_path = f"{post_path}/{post.split('.')[0]}.mp4"
                # add_mp3_padding(mp3_file_path, 1)
                duration = get_mp3_length(mp3_file_path)
                title_duration = get_mp3_length(mp3_title_file_path)
                # randomVideoSegment(output_video_path, duration + title_duration)
    
    for subreddit in os.listdir(folder_path):
        post_path = f"{folder_path}/{subreddit}"
        for post in os.listdir(post_path):
            if post.endswith(".mp4"):
                mp3_file_path = f"{post_path}/{post.split('.')[0]}.mp3"
                mp3_title_file_path = f"{post_path}/{post.split('.')[0]}_title.mp3"
                mp4_file_path = f"{post_path}/{post}"
                overlayText(mp3_file_path, mp3_title_file_path, mp4_file_path, post_path, f"{post.split('.')[0]}")

    # adjust audio to -14dB for youtube
    # for subreddit in os.listdir(folder_path):
    #     post_path = f"{folder_path}/{subreddit}"
    #     for post in os.listdir(post_path):
    #         video_path = f"{post_path}/{post}"
    #         if os.path.isdir(video_path):
    #             for video in os.listdir(video_path):
    #                 if video.endswith(".mp4"):
    #                     adjust_mp4_volume(f"{video_path}/{video}", -14)
    print("Video Maker Completed")