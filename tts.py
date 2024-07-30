import os
import requests
import json
import sys
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get args if they exist
if len(sys.argv) > 1:
    voice = sys.argv[1]
else:
    voice = os.getenv("TTS_VOICE")

# Set vars
transcription_file_name="output/tts/output_transcription.txt"
audio_tts_file_name="output/tts/output_tts_audio_" +voice +".mp3"

# Set OpenAI voice dicyionary. Avaliable voices from https://platform.openai.com/docs/guides/text-to-speech/quickstart
open_ai_voices = {
    "alloy": 1,
    "echo": 2,
    "fable": 3,
    "onyx": 4,
    "nova": 5,
    "shimmer": 6
}

# Get the transcription
with open(transcription_file_name, "r") as file:
    # Read the entire content of the file
    transcription_from_file = file.read()

# Process OpenAI Voice
def openai():
    print("Converting " +transcription_file_name +" with the Azure OpenAI and the " +voice +" voice")

    # Make API call
    tts_url = os.getenv("AZURE_OPENAI_ENDPOINT") +"/openai/deployments/" +os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT") +"/audio/speech?api-version=2024-02-15-preview"
    tts_headers_list = {
    "api-key": os.getenv("AZURE_OPENAI_API_KEY"),
    "Content-Type": "application/json" 
    }
    tts_payload = json.dumps({
        "model": "tts-1-hd",
        "input": str(transcription_from_file),
        "voice": voice
    })
    tts_response = requests.request("POST", tts_url, data=tts_payload,  headers=tts_headers_list)
    print()

    if tts_response.status_code == 200:
        # Save the binary content to a file
        with open(audio_tts_file_name, 'wb') as file:
            file.write(tts_response.content)
        print("TTS output file saved successfully as " +audio_tts_file_name)
    else:
        print(f"Failed to retrieve content. Status code: {tts_response.status_code}")
        print(f"Response content: {tts_response.content}")


# Process Azure Speech Service Voice
def azurespeech():
    print("Converting " +transcription_file_name +" with Azure Speech Service and the " +voice +" voice")

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_service_key = os.getenv("AZURE_SPEECH_KEY")
    speech_service_region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = speechsdk.SpeechConfig(subscription=speech_service_key, region=speech_service_region)
    speech_config.speech_synthesis_voice_name = voice
    audio_output = speechsdk.audio.AudioOutputConfig(filename=audio_tts_file_name)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    # Perform the speech synthesis
    result = synthesizer.speak_text_async(str(transcription_from_file)).get()

    # Check result status
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("TTS output file saved successfully as " +audio_tts_file_name)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

# If the voice is an OpenAI voice, use that service, otherwise process as a Azure Speech voice
if voice in open_ai_voices:
    openai()
else:
    azurespeech()













