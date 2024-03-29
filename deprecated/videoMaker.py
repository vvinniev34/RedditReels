import random
import os
import time
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from fileDetails import get_mp3_length

# Get the current working directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg.exe")

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
    audio_clip = AudioFileClip(input_audio_filepath)

    # Trim the video to the 2-minute random segment
    random_segment = video_clip.subclip(random_start_time_seconds, random_start_time_seconds + duration)

    # Set the audio of the random segment to the input audio
    random_segment = random_segment.set_audio(audio_clip)

    # Write the final video to the output file
    random_segment.write_videofile(output_video_filepath, codec="libx264", threads=8, logger = None, preset='ultrafast')
    
    print(f"Snipped {duration} s length video starting at: {random_start_time_seconds}")



def textOverlay(video_path, text_input, post_path, post):
    partNum = 0
    currentVidTime = 60

    start_time = 0
    video_segments = [[]]  # To store paths of individual video segments
    durations = []  # Initialize an empty list to store the durations
    # Open the line_times file to fill line durations array
    with open(f"{video_path.split('.')[0]}_line_times.txt", "r") as file:
        for line in file:
            parts = line.split()
            duration_str = parts[-1]
            try:
                duration = float(duration_str)
                durations.append(duration)
            except ValueError:
                print(f"Skipped invalid line: {line.strip()}")

    duration_i = 0
    # Loop through the text_array and overlay text every 5 seconds
    for i, text in enumerate(text_input):
        # print(f"{duration_i}, {text}")
        # Remove leading and trailing whitespace and normal spaces from the line
        text = text.strip()#.replace(", ", " ")
        noWhitespaceText = text.replace(" ", "")
        
        if not noWhitespaceText or len(noWhitespaceText) == 0:
            continue

        wrappedText = splitTextForWrap(text, 20)
        print(start_time, " ", (start_time + durations[duration_i]), " ", durations[duration_i])

        print(f"{duration_i},\n'{wrappedText}'")
        
        cmd = [
            ffmpeg_exe_path,
            "-nostdin",  # Disable interaction with standard input
            "-i", video_path,
            "-vf", f"drawtext=text='{wrappedText}':x=(w-text_w)/2:y=(h-text_h)/3:fontsize=70:fontcolor=white:fontfile=C\\:/Windows/fonts/arlrdbd.ttf:bordercolor=black:borderw=5",
            "-c:a", "copy",
            "-preset", "ultrafast",  # Use a faster preset"
            "-threads", "4",
            "-ss", str(start_time),     
            "-t", str(durations[duration_i]),
            "-y",
            f"temp/segment_{duration_i}.mp4"  # Output path for this segment
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("Command ran successfully")
        else:
            print("Command encountered an error")
            print(result.stdout)  # Print the standard output for debugging
            print(result.stderr)  # Print the standard error for debugging
        

        # if length is over 60 seconds, create a new part for the video
        if (start_time + durations[duration_i] > currentVidTime):
            currentVidTime += 60
            partNum += 1
            video_segments.append([])

        # Append the path of the generated segment to the list
        video_segments[partNum].append(f"temp/segment_{duration_i}.mp4")

        # Update start time for the next segment
        start_time += durations[duration_i]
        duration_i += 1

    partNum = 1
    for part in video_segments:
        # Load the video clips, List to store video clips
        video_clips = []
        # Iterate through the list of segment paths
        for path in part:
            if os.path.exists(path):
                clip = VideoFileClip(path)
                video_clips.append(clip)
            else:
                # Handle non-existent files (you can print a message or take other actions)
                print(f"File not found: {path}")
        # Concatenate the video clips sequentially; maybe change compose to chain
        final_video = concatenate_videoclips(video_clips, method="chain")
        # Write the concatenated video to a file
        output_video_path = f"{post_path}/(part{partNum})_{post}"
        print(f"Writing output video: {output_video_path}")
        final_video.write_videofile(output_video_path, codec="libx264", threads=8, logger = None, preset='ultrafast')
        print(f"Finished writing part {partNum}")
        # Close the video clips
        for clip in video_clips:
            clip.close()

        # Clean up individual video segments
        for segment in part:
            if os.path.exists(segment):
                os.remove(segment)

        partNum += 1

    print("Overlay complete.")


if __name__ == "__main__":
    background_video_path = "SubwaySurfers/subwaySurfers.mp4"
    # today = date.today().strftime("%Y-%m-%d")
    today = "2023-12-29"

    folder_path = f"RedditPosts/{today}/Texts"
    for subreddit in os.listdir(folder_path):
        post_path = f"{folder_path}/{subreddit}"
        for post in os.listdir(post_path):
            if post.endswith(".mp3"):
                mp3_file_path = f"{post_path}/{post}"
                output_video_path = f"{post_path}/{post.split('.')[0]}.mp4"
                duration = get_mp3_length(mp3_file_path)
                randomVideoSegment(background_video_path, mp3_file_path, output_video_path, duration)
    
    for subreddit in os.listdir(folder_path):
        post_path = f"{folder_path}/{subreddit}"
        for post in os.listdir(post_path):
            if post.endswith(".mp4") and not post.endswith("F.mp4"):
                mp4_file_path = f"{post_path}/{post}"
                text_input = []
                text_file_path = f"{post_path}/{post.split('.')[0]}.txt"
                # Open the file for reading
                with open(text_file_path, 'r', encoding='utf-8') as file:
                    # Read each line and add it to the list
                    for line in file:
                        # Remove leading and trailing whitespace from the line
                        line = line.strip()
                        removed_spaces_line = line.replace(" ", "")  # This removes spaces
                        if removed_spaces_line:
                            text_input.append(line)
                            
                textOverlay(mp4_file_path, text_input, post_path, f"{post.split('.')[0]}F.mp4")
    print("Video Maker Completed")
