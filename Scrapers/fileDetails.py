import os
from pydub import AudioSegment
from moviepy.editor import AudioFileClip

def get_mp3_length(mp3_file_path):
    try:
        audio_clip = AudioFileClip(mp3_file_path)
        duration_seconds = audio_clip.duration
        audio_clip.close()
        return duration_seconds
    except Exception as e:
        print(f"Error: {e}")
        return None

def count_non_empty_characters_in_directory(directory_path, output_file):
    # Initialize a counter for non-empty characters
    total_non_empty_char_count = 0

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

                    # Check if the line is not empty
                    if line:
                        # Count the non-empty characters in the line
                        non_empty_char_count += len(line)

                # Add the non-empty character count of this file to the total
                total_non_empty_char_count += non_empty_char_count

                mp3_file_path = f"{directory_path}/{filename.split('.')[0]}.mp3"
                length_seconds = get_mp3_length(mp3_file_path)
                with open(output_file, 'a') as file:
                    file.write(f"{filename}\n\n")
                    file.write(f"Non-empty characters: {non_empty_char_count}\n")
                    file.write(f"Length of MP3 file: {length_seconds:.2f} seconds\n")
                    file.write(f"Average characters per second: {non_empty_char_count / length_seconds:.2f}\n")
                    file.write(f"Average characters per 3 seconds: {3 * non_empty_char_count / length_seconds:.2f}\n")
                    file.write(f"Average characters per 5 seconds: {5 * non_empty_char_count / length_seconds:.2f}\n\n")
            
    return total_non_empty_char_count


if __name__ == "__main__":
    # Example usage:
    directory_path = 'RedditPosts/2023-09-02/Texts'  # Replace with the path to your directory
    output_file = "RedditPosts/2023-09-02/postDetails.txt"
    for subreddit in os.listdir(directory_path):
        total_count = count_non_empty_characters_in_directory(f"{directory_path}/{subreddit}", output_file)