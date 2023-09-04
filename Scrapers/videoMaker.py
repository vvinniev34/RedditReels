import random
import os
import subprocess
import time
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoClip, TextClip, VideoFileClip, AudioFileClip, clips_array, concatenate_videoclips
from fileDetails import get_mp3_length

def randomVideoSegment(input_video_filepath, input_audio_filepath, output_video_filepath, duration):
    total_duration_seconds = 12 * 30 + 35
    # Generate a random start time within the valid range
    random_start_time_seconds = random.uniform(0, total_duration_seconds - duration)

    print(random_start_time_seconds)
    # Load the input video and audio
    video_clip = VideoFileClip(input_video_filepath)
    audio_clip = AudioFileClip(input_audio_filepath)

    # Trim the video to the 2-minute random segment
    random_segment = video_clip.subclip(random_start_time_seconds, random_start_time_seconds + duration)

    # Set the audio of the random segment to the input audio
    random_segment = random_segment.set_audio(audio_clip)

    # Write the final video to the output file
    random_segment.write_videofile(output_video_filepath, codec="libx264")


def textOverlay(video_path, text_input, characters_per_second, output_video_path):
    # Get the current working directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the relative path to ffmpeg.exe
    ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg-2023-08-30-git-7aa71ab5c0-full_build", "bin", "ffmpeg.exe")

    start_time = 0
    video_segments = []  # To store paths of individual video segments
    # Loop through the text_array and overlay text every 5 seconds
    for i, text in enumerate(text_input):
        print(text)
        # Remove leading and trailing whitespace and normal spaces from the line
        text = text.strip()
        
        noWhitespaceText = text.replace(" ", "")
        # Sleep for time it takes to read the sentence, adjust as needed
        sleep_time = (len(noWhitespaceText) / characters_per_second)
        if sleep_time == 0:
            continue

        cmd = [
            ffmpeg_exe_path,
            "-nostdin",  # Disable interaction with standard input
            "-i", video_path,
            "-vf", f"drawtext=text='{text}':x=10:y=10:fontsize=24:fontcolor=white:fontfile=C\\:/Windows/fonts/arial.ttf",
            "-c:a", "copy",
            "-ss", str(start_time),
            "-t", str(sleep_time),
            "-y",
            f"segment_{i}.mp4"  # Output path for this segment
        ]
        print(start_time, " ", (start_time + sleep_time), " ", sleep_time)
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Append the path of the generated segment to the list
        video_segments.append(f"segment_{i}.mp4")

        # Update start time for the next segment
        start_time += sleep_time

    # Load the video clips
    video_clips = [VideoFileClip(path) for path in video_segments]
    # Concatenate the video clips sequentially
    final_video = concatenate_videoclips(video_clips, method="compose")
    # Write the concatenated video to a file
    final_video.write_videofile(output_video_path, codec="libx264")
    # Close the video clips
    for clip in video_clips:
        clip.close()

    # Clean up individual video segments
    for segment in video_segments:
        os.remove(segment)

    print("Overlay complete.")


if __name__ == "__main__":
    background_video_path = "SubwaySurfers/subwaySurfers.mp4"

    folder_path = "RedditPosts/2023-09-02/Texts"
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
            if post.endswith(".mp4"):
                mp4_file_path = f"{post_path}/{post}"
                mp4_output_path = f"{post_path}/{post.split('.')[0]}F.mp4"
                text_input = []
                non_empty_char_count = 0
                text_file_path = f"{post_path}/{post.split('.')}.txt"
                # Open the file for reading
                with open(text_file_path, 'r', encoding='utf-8') as file:
                    # Read each line and add it to the list
                    for line in file:
                        # Remove leading and trailing whitespace from the line
                        line = line.strip()
                        text_input.append(line)

                        # Remove spaces from the line and count non-empty characters
                        line = line.replace(" ", "")  # This removes spaces
                        if line:
                            non_empty_char_count += len(line)
                    characters_per_second = non_empty_char_count / get_mp3_length(mp3_file_path)
                textOverlay(mp4_file_path, text_input, characters_per_second, mp4_output_path)

    # mp4_file_path = "AmItheAsshole1.mp4"
    # mp4_output_path = "AmItheAsshole1F.mp4"
    # mp3_file_path = "AmItheAsshole1.mp3"
    # text_file_path = "AmItheAsshole1.txt"
    
    # non_empty_char_count = 0
    # # Open the file for reading
    # with open(text_file_path, 'r', encoding='utf-8') as file:
    #     # Read each line and add it to the list
    #     for line in file:
    #         # Remove leading and trailing whitespace from the line
    #         line = line.strip()
    #         text_input.append(line)

    #         # Remove spaces from the line and count non-empty characters
    #         line = line.replace(" ", "")  # This removes spaces
    #         if line:
    #             non_empty_char_count += len(line)

    # characters_per_second = non_empty_char_count / get_mp3_length(mp3_file_path)

    # textOverlay(mp4_file_path, text_input, characters_per_second, mp4_output_path)
