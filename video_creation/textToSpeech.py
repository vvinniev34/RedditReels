import os
import time
from gtts import gTTS
from datetime import date
from pydub import utils, AudioSegment
from pydub.effects import speedup
from fileDetails import add_mp3_padding
import pyttsx3

from openai import OpenAI
from accountCredentials.openai_key import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# Construct the relative path to ffmpeg.exe
script_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg-2023-08-30-git-7aa71ab5c0-full_build", "bin", "ffmpeg.exe")
AudioSegment.converter = ffmpeg_exe_path
def get_prob_path():
    return os.path.join(script_dir, "ffmpeg-2023-08-30-git-7aa71ab5c0-full_build", "bin", "ffprobe.exe")
utils.get_prober_name = get_prob_path

def speedup_audio(filename, subreddit_path):
    path = os.path.join(subreddit_path, f"{filename.split('.')[0]}.mp3")
    audio = AudioSegment.from_mp3(path)
    spedup_audio = speedup(audio, 1.2, 120)
    spedup_audio.export(path, format="mp3") # export to mp3

def convert(filename, folder_path):
    text_file_path = os.path.join(folder_path, filename)
    output_file = os.path.join(folder_path, f"{filename.split('.')[0]}.mp3")
    
    try:
        with open(text_file_path, 'r', encoding='utf-8') as file:
            lines = file.read()

            response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=lines
            )
            response.stream_to_file(output_file)

        
        print(f"mp3 creation successful. Saved as {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File not found error")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")

    folder_path = f"RedditPosts/{today}/Texts"
    # Iterate through all files in the folder
    for subreddit in os.listdir(folder_path):
        subreddit_path = f"{folder_path}/{subreddit}"
        print(f"Currently processing {subreddit}")
        for filename in os.listdir(subreddit_path):
            if filename.split('.')[-1] == "txt" and not filename.endswith("_line_times.txt"):
                convert(filename, subreddit_path)
                # speedup if using gtts or openai
                speedup_audio(filename, subreddit_path)
                print(f"Processed {filename}")
                break
                