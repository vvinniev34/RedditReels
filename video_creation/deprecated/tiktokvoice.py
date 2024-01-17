# author: GiorDior aka Giorgio
# date: 12.06.2023
# topic: TikTok-Voice-TTS
# version: 1.0
# credits: https://github.com/oscie57/tiktok-voice

import threading, requests, base64
from playsound import playsound
import re

VOICES = [
    # ENGLISH VOICES
    'en_us_001',                  # English US - Female (Int. 1)
    'en_us_002',                  # English US - Female (Int. 2)
    'en_us_006',                  # English US - Male 1
    'en_us_007',                  # English US - Male 2
    'en_us_009',                  # English US - Male 3
    'en_us_010',                  # English US - Male 4
]

ENDPOINTS = ['https://tiktok-tts.weilnet.workers.dev/api/generation', "https://tiktoktts.com/api/tiktok-tts"]
current_endpoint = 0
# in one conversion, the text can have a maximum length of 300 characters
TEXT_BYTE_LIMIT = 270

# create a list by splitting a string, every element has n chars
# def split_string(string: str, chunk_size: int) -> list[str]:
#     words = string.split()
#     result = []
#     current_chunk = ''
#     for word in words:
#         if len(current_chunk) + len(word) + 1 <= chunk_size:  # Check if adding the word exceeds the chunk size
#             current_chunk += ' ' + word
#         else:
#             if current_chunk:  # Append the current chunk if not empty
#                 result.append(current_chunk.strip())
#             current_chunk = word
#     if current_chunk:  # Append the last chunk if not empty
#         result.append(current_chunk.strip())
#     return result

def split_string(text, max_length=TEXT_BYTE_LIMIT):
    parts = []
    current_part = ""

    # Split sentences using regular expression to handle "?", ".", and "!"
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sentence in sentences:
        # fits
        if len(current_part) + len(sentence) + 1 < max_length:
            current_part += sentence + ' '
        # new sentence too long, split up into fragments by ","
        elif len(sentence) >= max_length:
            if current_part:
                parts.append(current_part.strip())
                current_part = ""

            sentence_parts = sentence.split(',')
            current_fragment = ""
            for part in sentence_parts:
                if len(current_fragment) + len(part) + 1 <= max_length:
                    current_fragment += part + ' '
                else:
                    parts.append(current_fragment.strip())
                    current_fragment = part + ' '
            if current_fragment:
                parts.append(current_fragment.strip())

        # new sentence fits within max length, but not with old sentences
        else:
            parts.append(current_part.strip())
            current_part = sentence + ' '

    if current_part:
        parts.append(current_part.strip())
    return parts

# checking if the website that provides the service is available
def get_api_response() -> requests.Response:
    url = f'{ENDPOINTS[current_endpoint].split("/a")[0]}'
    response = requests.get(url)
    return response

# saving the audio file
def save_audio_file(base64_data: str, filename: str = "output.mp3") -> None:
    audio_bytes = base64.b64decode(base64_data)
    with open(filename, "wb") as file:
        file.write(audio_bytes)

# def write_wav_file(output_path, audio_bytes, sample_width, channels, framerate):
#     with wave.open(output_path, 'wb') as wav_file:
#         wav_file.setnchannels(channels)
#         wav_file.setsampwidth(sample_width)
#         wav_file.setframerate(framerate)
#         wav_file.writeframes(audio_bytes)

# send POST request to get the audio data
def generate_audio(text: str, voice: str) -> bytes:
    url = f'{ENDPOINTS[current_endpoint]}'
    headers = {'Content-Type': 'application/json'}
    data = {'text': text, 'voice': voice}
    response = requests.post(url, headers=headers, json=data)
    return response.content

# creates an text to speech audio file
def tts(text: str, voice: str = "none", filename: str = "output.mp3", play_sound: bool = False) -> None:
    # checking if the website is available
    global current_endpoint

    # if get_api_response().status_code == 200:
    #     print("Service available!")
    # else:
    if not get_api_response().status_code == 200:
        current_endpoint = (current_endpoint + 1) % 2
        # if get_api_response().status_code == 200:
        #     print("Service available!")
        # else:
        if not get_api_response().status_code == 200:
            print(f"Service not available and probably temporarily rate limited, try again later...")
            return
    
    # checking if arguments are valid
    if voice == "none":
        print("No voice has been selected")
        return
    
    if not voice in VOICES:
        print("Voice does not exist")
        return

    if len(text) == 0:
        print("Insert a valid text")
        return
    
    # creating the audio file
    try:
        if len(text) < TEXT_BYTE_LIMIT:
            audio = generate_audio((text), voice)
            if current_endpoint == 0:
                audio_base64_data = str(audio).split('"')[5]
            else:
                audio_base64_data = str(audio).split('"')[3].split(",")[1]
            
            if audio_base64_data == "error":
                print("This voice is unavailable right now")
                return
                
        else:
            # Split longer text into smaller parts
            text_parts = split_string(text, TEXT_BYTE_LIMIT)
            audio_base64_data = [None] * len(text_parts)
            
            # Define a thread function to generate audio for each text part
            def generate_audio_thread(text_part, index):
                audio = generate_audio(text_part, voice)
                if current_endpoint == 0:
                    base64_data = str(audio).split('"')[5]
                else:
                    base64_data = str(audio).split('"')[3].split(",")[1]

                if audio_base64_data == "error":
                    print("This voice is unavailable right now")
                    return "error"
                
                audio_base64_data[index] = base64_data

            threads = []
            for index, text_part in enumerate(text_parts):
                # Create and start a new thread for each text part
                thread = threading.Thread(target=generate_audio_thread, args=(text_part, index))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            # Concatenate the base64 data in the correct order
            audio_base64_data = "".join(audio_base64_data)
            
        save_audio_file(audio_base64_data, filename)
        print(f"Audio file saved successfully as '{filename}'")
        if play_sound:
            playsound(filename)

    except Exception as e:
        print("Error occurred while generating audio:", str(e))