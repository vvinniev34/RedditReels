import os
import time
from datetime import date
from pydub import utils, AudioSegment, effects
from pydub.utils import mediainfo
# from pydub.effects import speedup
# from fileDetails import get_mp3_length, add_mp3_padding
from fileDetails import get_wav_length
# import pyttsx3
# from deprecated.tiktokvoice import tts
# from openai import OpenAI
# from accountCredentials.openai_key import OPENAI_API_KEY
from speech_synthesis import synth_speech

# client = OpenAI(api_key=OPENAI_API_KEY)

# Construct the relative path to ffmpeg.exe
script_dir = os.path.dirname(os.path.abspath(__file__))
# ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg-2023-08-30-git-7aa71ab5c0-full_build", "bin", "ffmpeg.exe")
ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg.exe")

AudioSegment.converter = ffmpeg_exe_path
def get_prob_path():
    return os.path.join(script_dir, "ffmpeg-2023-08-30-git-7aa71ab5c0-full_build", "bin", "ffprobe.exe")
utils.get_prober_name = get_prob_path

MAX_PART_TIME = 59

def speedup_audio(filename, subreddit_path):
    path = os.path.join(subreddit_path, f"{filename.split('.')[0]}.wav")
    media_info = mediainfo(path)
    original_bitrate = media_info.get('bit_rate')
    if original_bitrate is None:
        original_bitrate = "352k"
    audio = AudioSegment.from_file(path)

    # audio = speedup(audio, 1.2) # use either 1.25 or 1.3

    # Calculate the dB adjustment
    print("Audio Level (dBFS):", audio.dBFS)
    effects.normalize(audio)  
    dB_adjustment = min(-14 - audio.dBFS, -1 * audio.max_dBFS)
    audio = audio + dB_adjustment 
    effects.normalize(audio)  

    print("Audio Level (dBFS):", audio.dBFS)
    audio.export(path, format="wav", bitrate=original_bitrate) # export to wav

def convert(filename, folder_path):
    text_file_path = os.path.join(folder_path, filename)
    output_file = os.path.join(folder_path, f"{filename.split('.')[0]}.wav")
    output_title_file = os.path.join(folder_path, f"{filename.split('.')[0]}_title.wav")

    # Initialize pyttsx3
    # engine = pyttsx3.init("sapi5")
    # voices = engine.getProperty("voices")[1] 
    # rate = engine.getProperty('rate')
    # engine.setProperty('rate', rate)
    # engine.setProperty('voice', voices)
    max_video_time = MAX_PART_TIME
    try:
        with open(text_file_path, 'r', encoding='utf-8') as file:
            title = file.readline().replace("&", "and").strip()

            output_directory = f"{folder_path}/{filename.split('.')[0]}"
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            with open(f"{output_directory}/videoTitle.txt", 'w', encoding='utf-8') as title_file:
                title_file.write(title)

            if filename.startswith("askreddit"):
                swoosh_transition = AudioSegment.from_file("static/audio/swoosh_transition.mp3")
                swoosh_transition_length = len(swoosh_transition) / 1000

                title_synthesized = synth_speech(title, output_title_file)
                while not title_synthesized:
                    print("Title not synthesized, trying again...")
                    time.sleep(3)
                    title_synthesized = synth_speech(title, output_title_file)
                
                segment_files = []
                total_time = []
                cur_time = 0
                num_comments = 0
                for line in file:
                    if not line.isspace() and cur_time < max_video_time:
                        segment_file = f"{output_file.split('.')[0]}_seg{num_comments}.wav"
                        segment_synthesized = synth_speech(line.strip().replace("&", "and"), segment_file)
                        while not segment_synthesized:
                            print("Segment not synthesized, trying again...")
                            time.sleep(3)
                            segment_synthesized = synth_speech(line.strip().replace("&", "and"), segment_file)
                        
                        new_segment_time = get_wav_length(segment_file)
                        if cur_time + new_segment_time >= max_video_time and cur_time != 0:
                            os.remove(segment_file)
                            break
                        elif cur_time + new_segment_time >= max_video_time and cur_time == 0:
                            total_time.append((cur_time + (swoosh_transition_length + new_segment_time)))
                            segment_files.append(segment_file)
                            break
                        cur_time += (swoosh_transition_length + new_segment_time)
                        total_time.append(cur_time)
                        segment_files.append(segment_file)
                        num_comments += 1

                # concatenate audio into single audio
                askreddit_segments = [AudioSegment.from_wav(segment_file) for segment_file in segment_files]
                askreddit_audio = AudioSegment.empty()
                first = True
                for segment in askreddit_segments:
                    askreddit_audio += segment if first else (swoosh_transition + segment)
                    first = False
                askreddit_audio.export(output_file, format="wav")
                with open(f"{output_directory}/comment_times.txt", 'w', encoding='utf-8') as comment_time_file:
                    comment_time_file.write(','.join(map(str, total_time)))

                # cleanup individual comment files
                for segment_file in segment_files:
                    try:
                        os.remove(segment_file)
                    except OSError as e:
                        print(f"Error deleting file {segment_file}")
            else:
                lines = file.read().replace("&", "and")
                if len(lines) > 4000:
                    print(f"Exiting file tts, {filename} too large")
                    return False
                
                # tiktok TTS
                # tts(lines, "en_us_010", output_file, play_sound=False)

                # Microsoft Azure tts
                title_synthesized = synth_speech(title, output_title_file)
                while not title_synthesized:
                    print("Title not synthesized, trying again...")
                    time.sleep(3)
                    title_synthesized = synth_speech(title, output_title_file)
               
                body_synthesized = synth_speech(lines, output_file)
                while not body_synthesized:
                    print("Body not synthesized, trying again...")
                    time.sleep(3)
                    body_synthesized = synth_speech(lines, output_file)

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
        
        print(f"wav creation successful. Saved as {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File not found error")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    # today = "2024-01-06"
    # today = "Custom"
    # processed = ["AmItheAsshole", "AITAH"]

    folder_path = f"RedditPosts/{today}/Texts"
    # Iterate through all files in the folder
    for subreddit in os.listdir(folder_path):
        subreddit_path = f"{folder_path}/{subreddit}"
        print(f"Currently processing {subreddit}")
        for filename in os.listdir(subreddit_path):
            if filename.split('.')[-1] == "txt":# and subreddit not in processed:
                convert(filename, subreddit_path)
                print(f"Processed {filename}")
                
    for subreddit in os.listdir(folder_path):
        subreddit_path = f"{folder_path}/{subreddit}"
        for filename in os.listdir(subreddit_path):
            wav_file_path = f"{subreddit_path}/{filename}"
            if filename.split('.')[-1] == "wav":# and subreddit not in processed:
                # speedup_audio(filename, subreddit_path)
                print(f"Increased Volume of {wav_file_path}")

                
