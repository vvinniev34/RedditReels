import random
import os
import re
import time
import subprocess
import whisper_timestamped as whisper
from moviepy.editor import VideoFileClip, TextClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from fileDetails import get_mp3_length, add_mp3_padding

# Get the current working directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the relative path to ffmpeg.exe
ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg-2023-08-30-git-7aa71ab5c0-full_build", "bin", "ffmpeg.exe")

model = whisper.load_model("base")

def replace_ada(sentence):
    # Define the pattern using regular expression with the IGNORECASE flag
    # pattern = r'(^|[.,;?!])ada(?=[\s.,;?!])'
    pattern = r'\bada\b'
    
    # Use re.sub() with the IGNORECASE flag to replace the matched pattern
    # modified_sentence = re.sub(pattern, r'\1AITA', sentence, flags=re.IGNORECASE)
    modified_sentence = re.sub(pattern, 'AITA', sentence, flags=re.IGNORECASE)

    return modified_sentence

def splitTextForWrap(input_str: str, line_length: int):
    words = input_str.split(" ")
    line_count = 0
    split_input = ""
    line = ""
    for word in words:
        if (line_count + len(word) + 1) > line_length:
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
    
    paddingNeeded = line_length - line_count
    alternatePadding = True
    while (paddingNeeded > 0):
        if alternatePadding:
            line = "\u00A0" + line
        else:
            line = line + "\u00A0"
        alternatePadding = not alternatePadding
        paddingNeeded -= 1
    split_input += line
    return split_input

def randomVideoSegment(input_video_filepath, input_audio_filepath, output_video_filepath, duration):
    total_duration_seconds = 12 * 30 + 35
    # Generate a random start time within the valid range
    random_start_time_seconds = random.uniform(0, total_duration_seconds - duration)

    # Load the input video and audio
    video_clip = VideoFileClip(input_video_filepath)
    # audio_clip = AudioFileClip(input_audio_filepath)

    # Trim the video to the 2-minute random segment
    random_segment = video_clip.subclip(random_start_time_seconds, random_start_time_seconds + duration)

    # Set the audio of the random segment to the input audio
    # random_segment = random_segment.set_audio(audio_clip)

    # Write the final video to the output file
    random_segment.write_videofile(output_video_filepath, codec="libx264", threads=8, logger = None, preset='ultrafast')
    
    print(f"Snipped {duration} s length video starting at: {random_start_time_seconds}")

def overlayText(mp3_file_path, video_path, post_path, postName):
    partNum = 0
    currentVidTime = 60
    videoTitle = post

    start_time = 0
    video_segments = [[[], []]]  # To store paths of individual video segments
    video_segments[partNum][1].append(0)

    audio = whisper.load_audio(mp3_file_path)
    result = whisper.transcribe(model, audio, 'en')

    video_clip = VideoFileClip(video_path)

    first_segment = True
    for segment in result['segments']:
        abbreviationFixedText = replace_ada(segment['text'])
        if first_segment:
            videoTitle = abbreviationFixedText
            first_segment = False

        # split segment into multiple if phrase is longer than 30 characters
        splitSegments = []
        if (len(abbreviationFixedText) <= 40):
            splitSegments.append([abbreviationFixedText, segment['end']])
        else:
            currentText = ""
            prevEnd = -1
            for word in segment['words']:
                if (len(word['text']) + len(currentText) + 1) <= 20:
                    currentText += (word['text'] + " ")
                else:
                    splitSegments.append([replace_ada(currentText), prevEnd])
                    currentText = (word['text'] + " ")
                prevEnd = word['end']
            splitSegments.append([replace_ada(currentText), prevEnd])
            if (prevEnd == -1):
                print("Invalid word, too many characters")
                return

        # create text overlay for each segment
        for split in splitSegments:
            text = split[0]
            endTime = split[1]

            wrappedText = splitTextForWrap(text.strip(), 20)

            duration = endTime - start_time
            print(f"{start_time} {start_time + duration} {duration}\n'{wrappedText}'")

            # if length is over 60 seconds, create a new part for the video
            if (endTime > currentVidTime):
                video_segments[partNum][1].append(start_time)
                currentVidTime += 60
                partNum += 1
                video_segments.append([[], []])
                video_segments[partNum][1].append(start_time)

            width_x = 1080
            height_y = 1920
            textbox_size_x = 900
            textbox_size_y = 600
            offset = 8

            center_x = width_x / 2 - textbox_size_x / 2
            center_y = height_y / 2 - textbox_size_y / 2
            new_textclip = TextClip(
                wrappedText, 
                fontsize=75, 
                color='white', 
                bg_color='transparent',
                method='label',
                font='C:/Windows/fonts/GILBI___.TTF', 
                size=(textbox_size_x, textbox_size_y)
            ).set_start(start_time % 60).set_duration(duration).set_position((center_x, center_y))#.set_pos('center')

            shadow_textclip = TextClip(
                wrappedText, 
                fontsize=75, 
                color='black', 
                bg_color='transparent', 
                font='C:/Windows/fonts/GILBI___.TTF', 
                size=(textbox_size_x, textbox_size_y)
            ).set_start(start_time % 60).set_duration(duration).set_position((center_x + offset, center_y + offset))#.set_pos((5, 5))

            video_segments[partNum][0].append(shadow_textclip)
            video_segments[partNum][0].append(new_textclip)

            # Update start time for the next segment
            start_time = endTime
    video_segments[partNum][1].append(start_time)

    audio_clip = AudioFileClip(mp3_file_path)
    
    partNum = 1
    for part in video_segments:
        start_time = part[1][0]
        end_time = part[1][1]

        snipped_video = video_clip.subclip(start_time, end_time)
        snipped_audio = audio_clip.subclip(start_time, end_time)

        video_with_text = CompositeVideoClip([snipped_video] + part[0])
        video_with_text = video_with_text.set_audio(snipped_audio)

        # print(video_with_text.audio.duration)  # Print audio duration after overlay

        if not os.path.exists(f"{post_path}/{postName}"):
            os.makedirs(f"{post_path}/{postName}")
        output_video_path = f"{post_path}/{postName}/part{partNum}.mp4"
        print(f"Writing output video: {output_video_path}")
        video_with_text.write_videofile(output_video_path, codec="libx264", threads=8, logger = None)
        print(f"Finished writing part {partNum}")

        with open(f"{post_path}/{postName}/videoTitle.txt", 'w') as file:
            file.write(videoTitle)

        partNum += 1

    print("Overlay complete.")

if __name__ == "__main__":
    background_video_path = "SubwaySurfers/subwaySurfers.mp4"
    # today = date.today().strftime("%Y-%m-%d")
    today = "2023-12-29"
    today = "Test"

    folder_path = f"RedditPosts/{today}/Texts"
    for subreddit in os.listdir(folder_path):
        post_path = f"{folder_path}/{subreddit}"
        for post in os.listdir(post_path):
            if post.endswith(".mp3"):
                mp3_file_path = f"{post_path}/{post}"
                output_video_path = f"{post_path}/{post.split('.')[0]}.mp4"
                # add_mp3_padding(mp3_file_path, 1)
                # duration = get_mp3_length(mp3_file_path)
                # randomVideoSegment(background_video_path, mp3_file_path, output_video_path, duration)
    
    for subreddit in os.listdir(folder_path):
        post_path = f"{folder_path}/{subreddit}"
        for post in os.listdir(post_path):
            if post.endswith(".mp4") and not post.endswith("F.mp4"):
                mp3_file_path = f"{post_path}/{post.split('.')[0]}.mp3"
                mp4_file_path = f"{post_path}/{post}"
                overlayText(mp3_file_path, mp4_file_path, post_path, f"{post.split('.')[0]}")
    print("Video Maker Completed")
