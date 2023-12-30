import os
import time
from gtts import gTTS
from datetime import date
from pydub import utils, AudioSegment
from pydub.effects import speedup
import pyttsx3

speed = 1.5  # Adjust this value to change the speed (1.0 is the default)
# Get the current working directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the relative path to ffmpeg.exe
ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg-2023-08-30-git-7aa71ab5c0-full_build", "bin", "ffmpeg.exe")
AudioSegment.converter = ffmpeg_exe_path
def get_prob_path():
    return os.path.join(script_dir, "ffmpeg-2023-08-30-git-7aa71ab5c0-full_build", "bin", "ffprobe.exe")
utils.get_prober_name = get_prob_path

def speedup_audio(filename, subreddit_path):
    path = os.path.join(subreddit_path, f"{filename.split('.')[0]}.mp3")
    audio = AudioSegment.from_mp3(path)
    spedup_audio = speedup(audio, 1.3, 130) # speed up by 2x
    spedup_audio.export(path, format="mp3") # export to mp3

def convert(filename, folder_path):
    text_file_path = os.path.join(folder_path, filename)
    
    try:
        # Initialize an empty AudioSegment to store the concatenated speech
        combined_audio = AudioSegment.empty()
        
        # Create a file to write line durations
        line_times_file = open(f"{folder_path}/{filename.split('.')[0]}_line_times.txt", 'w', encoding='utf-8')

        # Initialize pyttsx3
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")[0] 
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate)#-25)
        engine.setProperty('voice', voices)

        with open(text_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            for line_number, line in enumerate(lines, start=1):
                # Remove leading and trailing whitespace from the line
                line = line.strip()
                if not line:
                    continue

                # Save the speech to a temporary file (using line number)
                temp_output_file = os.path.join(folder_path, f"temp_{line_number}.mp3")
                
                # Convert text to speech using pyttsx3
                engine.save_to_file(line, temp_output_file)  # Save the speech to a temporary file
                # Wait until above command is not finished.
                engine.runAndWait()

                # Add this line before the while loop inside the for loop
                print(f"Checking for file existence: {temp_output_file}")
                # Wait for the file to be written (check if it exists)
                while not os.path.exists(temp_output_file):
                    time.sleep(1)  # Sleep for 1 second

                # Read the temporary file as an AudioSegment
                AudioSegment.from_file(temp_output_file).export(temp_output_file, format="mp3") # audio file in mp3 format 
                audio_segment = AudioSegment.from_mp3(temp_output_file)
                # audio_segment = audio_segment[:-200] # cut off last 0.20 seconds

                # Measure the duration of the generated speech
                duration = len(audio_segment)

                # Concatenate the speech for this line with the combined_audio
                combined_audio += audio_segment

                # Remove the temporary file
                os.remove(temp_output_file)

                # Write the line duration to the line_times_file and print for debugging
                line_times_file.write(f"Line {line_number} duration (seconds): {duration / 1000}\n")
                print(f"Line duration: {duration / 1000} seconds")
        
        # Specify the output file (e.g., an MP3 file)
        output_file = os.path.join(folder_path, f"{filename.split('.')[0]}.mp3")
        
        # Save the concatenated speech to the output file
        combined_audio.export(output_file, format="mp3")
        print(f"Concatenation successful. Saved as {output_file}")

        # Close the line_time_file
        line_times_file.close()
    
    except FileNotFoundError:
        print(f"Error: File not found error")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # today = date.today().strftime("%Y-%m-%d")
    today = "2023-12-29"
    folder_path = f"RedditPosts/{today}/Texts"
    # Iterate through all files in the folder
    for subreddit in os.listdir(folder_path):
        subreddit_path = f"{folder_path}/{subreddit}"
        print(f"Currently processing {subreddit}")
        for filename in os.listdir(subreddit_path):
            if filename.split('.')[-1] == "txt" and not filename.endswith("_line_times.txt"):
                convert(filename, subreddit_path)
                # speedup_audio(filename, subreddit_path)
                print(f"Processed {filename}")
                