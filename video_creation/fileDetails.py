import os
import math
import pydub
from pydub import AudioSegment
from moviepy.editor import AudioFileClip, VideoFileClip

# Construct the relative path to ffmpeg.exe
script_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg.exe")
pydub.AudioSegment.ffmpeg = ffmpeg_exe_path
# pydub.AudioSegment.converter = ffmpeg_exe_path
# pydub.utils.get_prober_name = lambda: ffmpeg_exe_path

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
    # Load the input MP3 file
    audio = AudioSegment.from_file(file_path, format="mp3")

    # Calculate the duration of the padding in milliseconds
    padding_duration_ms = int(padding_duration_seconds * 1000)

    # Create a silent audio segment for padding
    padding = AudioSegment.silent(duration=padding_duration_ms)

    # Concatenate the original audio with the padding
    extended_audio = audio + padding

    # Overwrite the original file with the extended audio
    extended_audio.export(file_path, format="mp3")

def calculate_db(input_file):
    print(input_file)
    audio_segment = AudioSegment.from_file(input_file)
    # Calculate the dB level of an audio segment
    rms = audio_segment.rms
    if rms == 0:
        return float('-inf')  # Avoid log(0)
    return 20 * math.log10(rms)

def increase_volume(input_file, output_file, gain_db):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Print the original dB level
    original_db = calculate_db(audio)
    print(f"Original dB level: {original_db:.2f} dB")

    # Increase the volume
    audio = audio + gain_db

    # Export the modified audio to a new file
    audio.export(output_file, format="mp3")

    # Print the new dB level
    new_db = calculate_db(audio)
    print(f"New dB level: {new_db:.2f} dB")

def convert_video_to_audio(input_video_path, output_audio_path):
    # Load the video clip
    video_clip = VideoFileClip(input_video_path)

    # Extract the audio from the video
    audio_clip = video_clip.audio

    # Write the audio to an MP3 file
    audio_clip.write_audiofile(output_audio_path, codec='mp3')

    # Close the clips
    video_clip.close()
    audio_clip.close()

def make_mp4_audio_louder(video_path, audio_path, volume_factor):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Load the audio clip
    audio_clip = AudioFileClip(audio_path)

    # Adjust the volume
    loud_audio = audio_clip.volumex(volume_factor)

    # Set the loud audio to the video clip
    video_clip = video_clip.set_audio(loud_audio)

    # Return the modified video clip
    return video_clip

def make_mp3_audio_louder(input_audio_path, output_audio_path, volume_factor):
    audio_clip = AudioSegment.from_file(input_audio_path)
    loud_audio = audio_clip + volume_factor
    loud_audio.export(output_audio_path, format="mp3")

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

    input_video_path = 'audio/snowfall_volume_boosted.mp4'
    output_audio_path = 'audio/snowfall_volume_boosted.mp3'

    convert_video_to_audio(input_video_path, output_audio_path)

    # make_mp3_audio_louder("audio/snowfall.mp3", "audio/snowfall2x.mp3", 2.0)

    