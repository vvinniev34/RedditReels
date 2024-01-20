import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()
speech_key = os.environ.get('SPEECH_KEY')
speech_region = os.environ.get('SPEECH_REGION')

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

# The language of the voice that speaks.
speech_config.speech_synthesis_language = "en-US" 
speech_config.speech_synthesis_voice_name='en-US-RyanMultilingualNeural'

def synth_speech(text, output_file):
    ssml_text = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                    <voice name="en-US-RyanMultilingualNeural">
                        <prosody pitch="-3.5%" rate="+25.0%" volume="+100.0%">
                            {text}
                        </prosody>
                    </voice>
                </speak>"""

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = speech_synthesizer.speak_ssml_async(ssml_text).get()
    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file(output_file)
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                return False
    return True