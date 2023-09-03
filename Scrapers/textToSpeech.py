import os
from gtts import gTTS

speed = 1.5  # Adjust this value to change the speed (1.0 is the default)

def convert(filename, folder_path, text_file_path):
    # Read text from the file
    with open(text_file_path, 'r') as file:
        text = file.read()

    # Initialize the gTTS object and convert text to speech
    tts = gTTS(text)

    # Specify the output file (e.g., an MP3 file)
    output_file = f'{folder_path}/{filename}.mp3'

    # Save the speech to the output file
    tts.save(output_file)

if __name__ == "__main__":
    folder_path = "RedditPosts/2023-09-02/Texts"
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        convert(filename.split('.')[0], folder_path, file_path)
        print(f"Processed {filename}")
