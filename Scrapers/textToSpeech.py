import os
from gtts import gTTS
from datetime import date

speed = 1.5  # Adjust this value to change the speed (1.0 is the default)

def convert(filename, folder_path):
    text_file_path = os.path.join(folder_path, filename)
    # Read text from the file
    with open(text_file_path, 'r') as file:
        text = file.read()

    # Initialize the gTTS object and convert text to speech
    tts = gTTS(text)

    # Specify the output file (e.g., an MP3 file)
    output_file = f"{folder_path}/{filename.split('.')[0]}.mp3"

    # Save the speech to the output file
    tts.save(output_file)

if __name__ == "__main__":
    today = date.today().strftime("%Y-%m-%d")
    folder_path = f"RedditPosts/{today}/Texts"
    # Iterate through all files in the folder
    for subreddit in os.listdir(folder_path):
        subreddit_path = f"{folder_path}/{subreddit}"
        for filename in os.listdir(folder_path):
            if filename.split('.')[-1] == "txt":
                convert(filename, subreddit_path)
                print(f"Processed {filename}")