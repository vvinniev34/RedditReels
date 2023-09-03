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

                    # Check if the line is not empty
                    if line:
                        # Count the non-empty characters in the line
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
    # Example usage:
    directory_path = 'RedditPosts/2023-09-02/Texts'  # Replace with the path to your directory
    output_file = "RedditPosts/2023-09-02/postDetails.txt"
    all_files = []
    for subreddit in os.listdir(directory_path):
        all_files.append(count_non_empty_characters_in_directory(f"{directory_path}/{subreddit}", output_file))

    average_per_second = 0
    most_per_second = 0
    least_per_second = float('inf')

    average_per_3_second = 0
    most_per_3_second = 0
    least_per_3_second = float('inf')

    average_per_5_second = 0
    most_per_5_second = 0
    least_per_5_second = float('inf')

    longest = 0
    shortest = float('inf')

    num_files = 0
    for files in all_files:
        for post in files:
            shortest = min(shortest, post[1])
            longest = max(longest, post[1])

            average_per_second += post[2]
            least_per_second = min(least_per_second, post[2])
            most_per_second = max(most_per_second, post[2])

            average_per_3_second += post[3]
            least_per_3_second = min(least_per_3_second, post[3])
            most_per_3_second = max(most_per_3_second, post[3])

            average_per_5_second += post[4]
            least_per_5_second = min(least_per_5_second, post[4])
            most_per_5_second = max(most_per_5_second, post[4])

            num_files += 1

    print(f"video -- shortest : {shortest}; longest: {longest}")
    print(f"1 -- average: {average_per_second / num_files}; least: {least_per_second}; most: {most_per_second}")
    print(f"3 -- average: {average_per_3_second / num_files}; least: {least_per_3_second}; most: {most_per_3_second}")
    print(f"5 -- average: {average_per_5_second / num_files}; least: {least_per_5_second}; most: {most_per_5_second}")

# video -- shortest : 60.29; longest: 345.0
# 1 -- average: 14.123736865087512; least: 12.83466740270494; most: 15.492711115002407
# 3 -- average: 42.371210595262525; least: 38.50400220811482; most: 46.47813334500722
# 5 -- average: 70.61868432543753; least: 64.1733370135247; most: 77.46355557501204