import os
from gtts import gTTS
from datetime import date
from pydub import AudioSegment

speed = 1.5  # Adjust this value to change the speed (1.0 is the default)


def speedup():
    today = date.today().strftime("%Y-%m-%d")
    path = f"RedditPosts/{today}/Texts" + "/AITAfortellingmywifethelockonm.mp3"
    # export to mp3
    sound = AudioSegment.from_file(path)
    velocidad_X = 1.25 
    so = sound.speedup(velocidad_X, 150, 25)
    so.export(path[:-4] + '_Out.mp3', format = 'mp3')


def convert(filename, folder_path):
    text_file_path = os.path.join(folder_path, filename)
    # Read text from the file
    print(text_file_path)
    with open(text_file_path, 'r', encoding='utf-8') as file:
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
        print(f"Currently processing {subreddit}")
        for filename in os.listdir(subreddit_path):
            if filename.split('.')[-1] == "txt":
                convert(filename, subreddit_path)
                print(f"Processed {filename}")