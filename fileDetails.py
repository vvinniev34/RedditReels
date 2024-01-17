import os
import math
import shutil
import numpy as np
import pydub
import wave
from pydub import AudioSegment
from moviepy.editor import AudioFileClip, VideoFileClip

# Construct the relative path to ffmpeg.exe
script_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg.exe")
pydub.AudioSegment.ffmpeg = ffmpeg_exe_path
# pydub.AudioSegment.converter = ffmpeg_exe_path
# pydub.utils.get_prober_name = lambda: ffmpeg_exe_path

def get_wav_length(wav_file_path):
    try:
        with wave.open(wav_file_path, 'rb') as wav_file:
            # Get the duration in seconds
            duration_seconds = wav_file.getnframes() / float(wav_file.getframerate())
            return duration_seconds
    except Exception as e:
        print(f"Error: {e}")
        return 0

def get_mp3_length(mp3_file_path):
    try:
        audio_clip = AudioFileClip(mp3_file_path)
        duration_seconds = audio_clip.duration
        audio_clip.close()
        return duration_seconds
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def add_mp3_padding(file_path, padding_duration_seconds):
    audio = AudioSegment.from_file(file_path, format="mp3")
    padding_duration_ms = int(padding_duration_seconds * 1000)
    padding = AudioSegment.silent(duration=padding_duration_ms)
    extended_audio = audio + padding
    extended_audio.export(file_path, format="mp3")

def calculate_db(input_file):
    print(input_file)
    audio_segment = AudioSegment.from_file(input_file)
    rms = audio_segment.rms
    if rms == 0:
        return float('-inf')  # Avoid log(0)
    return 20 * math.log10(rms)

def make_mp3_audio_louder(input_audio_path, output_audio_path, volume_factor):
    audio_clip = AudioSegment.from_file(input_audio_path)
    loud_audio = audio_clip + volume_factor
    loud_audio.export(output_audio_path, format="mp3")

def convert_video_to_audio(input_video_path, output_audio_path):
    # Load the video clip
    video_clip = VideoFileClip(input_video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_audio_path, codec='mp3')
    video_clip.close()
    audio_clip.close()

def adjust_mp4_volume(file_path, target_dB):
    video_clip = VideoFileClip(file_path)
    mean_volume_dB = 20 * np.log10(np.sqrt(np.mean(video_clip.audio.to_soundarray()**2)))
    volume_factor = 10**((target_dB - mean_volume_dB) / 20)
    print(f"{volume_factor} {mean_volume_dB}")
    # new_video_clip = video_clip.volumex(volume_factor)
    new_video_clip = video_clip.multiply_volume(volume_factor).set_audio(video_clip.audio)

    print(f"Adjusting {file_path} to -14dB")
    temp_file_path = f"{file_path.split('.')[0]}_temp.mp4"
    # new_video_clip.write_videofile(temp_file_path, codec='libx264', audio_codec='aac', logger=None)
    new_video_clip.write_videofile(temp_file_path, codec='libx264', audio_codec='aac', logger=None, temp_audiofile="temp-audio.m4a", remove_temp=True)
    # shutil.move(temp_file_path, file_path)
    video_clip.close()
    new_video_clip.close()

if __name__ == "__main__":
    # date = "Test"    
    # directory_path = f'RedditPosts/{date}/Texts'  # Replace with the path to your directory
    # all_files = []
    # for subreddit in os.listdir(directory_path):
    #     subredditFolder = f"{directory_path}/{subreddit}"
    #     for post in os.listdir(subredditFolder):
    #         if post.endswith(".mp3"):
    #             postPath = f"{subredditFolder}/{post}"
    #             print(calculate_db(postPath))

    # input_video_path = 'audio/snowfall_volume_boosted.mp4'
    # output_audio_path = 'audio/snowfall_volume_boosted.mp3'

    # convert_video_to_audio(input_video_path, output_audio_path)

    # make_mp3_audio_louder("audio/snowfall.mp3", "audio/snowfall2x.mp3", 2.0)
    calculate_db("RedditPosts/2024-01-05/Texts/creepyencounters/creepyencounters1/part1.mp4")

    