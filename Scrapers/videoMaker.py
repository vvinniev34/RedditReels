import random
import os
import subprocess
import time
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoClip, TextClip, VideoFileClip, AudioFileClip, clips_array
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
    # Loop through the text_array and overlay text every 5 seconds
    for i, text in enumerate(text_input):
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"drawtext=text='{text}':x=10:y=10:fontsize=24:fontcolor=white",
            "-c:a", "copy",
            "-y",
            output_video_path
        ]

        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Sleep for time it takes to read the sentence, adjust as needed
        time.sleep(len(text) / characters_per_second)

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

