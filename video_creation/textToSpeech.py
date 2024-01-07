import os
import time
from datetime import date
from pydub import utils, AudioSegment, effects
from pydub.utils import mediainfo
from pydub.effects import speedup
from fileDetails import get_mp3_length, add_mp3_padding
import pyttsx3
from tiktokvoice import tts
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
    original_bitrate = mediainfo(path)['bit_rate']
    audio = AudioSegment.from_file(path)

    audio = speedup(audio, 1.2) # use either 1.25 or 1.3

    # Calculate the dB adjustment
    print("Audio Level (dBFS):", audio.dBFS)
    effects.normalize(audio)  
    dB_adjustment = min(-14 - audio.dBFS, -1 * audio.max_dBFS)
    audio = audio + dB_adjustment 
    effects.normalize(audio)  

    print("Audio Level (dBFS):", audio.dBFS)
    audio.export(path, format="mp3", bitrate=original_bitrate) # export to mp3

def convert(filename, folder_path):
    text_file_path = os.path.join(folder_path, filename)
    output_file = os.path.join(folder_path, f"{filename.split('.')[0]}.mp3")
    output_title_file = os.path.join(folder_path, f"{filename.split('.')[0]}_title.mp3")

    # Initialize pyttsx3
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")[1] 
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate)
    engine.setProperty('voice', voices)
    
    try:
        with open(text_file_path, 'r', encoding='utf-8') as file:
            title = file.readline().strip()

            # tiktok tts
            tts(title, "en_us_010", output_title_file, play_sound=False)

            if filename.startswith("askreddit"):
                num_comments = 0
                for line in file:
                    if not line.isspace():
                        print(line.strip())
                        tts(line.strip(), "en_us_010", f"{output_file.split('.')[0]}_{num_comments}.mp3", play_sound=False)
                        num_comments += 1
            else:
                lines = file.read()
                tts(lines, "en_us_010", output_file, play_sound=False)

            # openai tts
            # response = client.audio.speech.create(
            # model="tts-1",
            # voice="onyx",
            # input=lines
            # )
            # response.stream_to_file(output_file)

            # pyttsx3 tts
            # engine.save_to_file(title, output_title_file)
            # engine.runAndWait()
            # engine.save_to_file(lines, output_file)
            # engine.runAndWait()

            output_directory = f"{folder_path}/{filename.split('.')[0]}"
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            with open(f"{output_directory}/videoTitle.txt", 'w', encoding='utf-8') as file:
                file.write(title)
        
        print(f"mp3 creation successful. Saved as {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File not found error")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    today = "2024-01-06"
    # today = "Test"

    folder_path = f"RedditPosts/{today}/Texts"
    # Iterate through all files in the folder
    for subreddit in os.listdir(folder_path):
        subreddit_path = f"{folder_path}/{subreddit}"
        print(f"Currently processing {subreddit}")
        for filename in os.listdir(subreddit_path):
            if filename.split('.')[-1] == "txt" and not filename.endswith("_line_times.txt"):# and filename.startswith("askreddit"):
                convert(filename, subreddit_path)
                print(f"Processed {filename}")
                
    for subreddit in os.listdir(folder_path):
        subreddit_path = f"{folder_path}/{subreddit}"
        for filename in os.listdir(subreddit_path):
            mp3_file_path = f"{subreddit_path}/{filename}"
            if filename.split('.')[-1] == "mp3" and get_mp3_length(mp3_file_path) == 0:
                os.remove(mp3_file_path)
                print(f"Deleted {filename} for 0s length")
            elif filename.split('.')[-1] == "mp3":
                # speedup if using gtts or openai
                speedup_audio(filename, subreddit_path)
                print(f"Spedup and Increased Volume of {filename}")

                
