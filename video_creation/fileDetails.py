import os
import math
import pydub
from pydub import AudioSegment
from moviepy.editor import AudioFileClip

# Construct the relative path to ffmpeg.exe
script_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_exe_path = os.path.join(script_dir, "ffmpeg.exe")
pydub.AudioSegment.ffmpeg = ffmpeg_exe_path

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


def count_non_empty_characters_in_directory(directory_path, output_file):
    # Initialize a counter for non-empty characters
    files = []

    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file has a .txt extension
        if filename.endswith(".txt"):
            # Get the full file path
            file_path = os.path.join(directory_path, filename)

            # Open the file for reading
            with open(file_path, 'r', encoding='utf-8') as file:
                # Initialize a counter for non-empty characters in the file
                non_empty_char_count = 0
                # Iterate through each line in the file
                for line in file:
                    # Remove leading and trailing whitespace from the line
                    line = line.strip()
                    # Remove spaces from the line and count non-empty characters
                    line = line.replace(" ", "")  # This removes spaces
                    if line:
                        non_empty_char_count += len(line)


                mp3_file_path = f"{directory_path}/{filename.split('.')[0]}.mp3"
                length_seconds = get_mp3_length(mp3_file_path)
                with open(output_file, 'a') as file:
                    file.write(f"{filename}\n\n")
                    file.write(f"Non-empty characters: {non_empty_char_count}\n")
                    file.write(f"Length of MP3 file: {length_seconds:.2f} seconds\n")
                    file.write(f"Average characters per second: {non_empty_char_count / length_seconds:.2f}\n")
                    file.write(f"Average characters per 3 seconds: {3 * non_empty_char_count / length_seconds:.2f}\n")
                    file.write(f"Average characters per 5 seconds: {5 * non_empty_char_count / length_seconds:.2f}\n\n")

                files.append([non_empty_char_count, length_seconds, (non_empty_char_count / length_seconds),
                              3 * non_empty_char_count / length_seconds, 5 * non_empty_char_count / length_seconds])
            
    return files


if __name__ == "__main__":
    date = "Test"    
    directory_path = f'RedditPosts/{date}/Texts'  # Replace with the path to your directory
    all_files = []
    for subreddit in os.listdir(directory_path):
        subredditFolder = f"{directory_path}/{subreddit}"
        for post in os.listdir(subredditFolder):
            if post.endswith(".mp3"):
                postPath = f"{subredditFolder}/{post}"
                print(calculate_db(postPath))

    