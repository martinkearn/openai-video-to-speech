import os
import requests
import json
import sys
import argparse
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Process OpenAI Voice
def openai():
    print("1. Converting " +args.inputtranscriptionfilename +" with the Azure OpenAI and the " +args.voice +" voice")

    # Make API call
    tts_url = os.getenv("AZURE_OPENAI_ENDPOINT") +"/openai/deployments/" +os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT") +"/audio/speech?api-version=2025-01-01-preview"
    tts_headers_list = {
    "api-key": os.getenv("AZURE_OPENAI_API_KEY"),
    "Content-Type": "application/json" 
    }
    tts_payload = json.dumps({
        "model": "tts-1-hd",
        "input": str(transcription_from_file),
        "voice": args.voice
    })
    tts_response = requests.request("POST", tts_url, data=tts_payload,  headers=tts_headers_list)

    if tts_response.status_code == 200:
        # Save the binary content to a file
        with open(output_audio_path, 'wb') as file:
            file.write(tts_response.content)
        print("2. TTS output file saved successfully as " +output_audio_path)
    else:
        print(f"Failed to retrieve content. Status code: {tts_response.status_code}")
        print(f"Response content: {tts_response.content}")


# Process Azure Speech Service Voice
def azurespeech():
    print("1. Converting " +args.inputtranscriptionfilename +" with Azure Speech Service and the " +args.voice +" voice")

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_service_key = os.getenv("AZURE_SPEECH_KEY")
    speech_service_region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = speechsdk.SpeechConfig(subscription=speech_service_key, region=speech_service_region)
    speech_config.speech_synthesis_voice_name = args.voice
    audio_output = speechsdk.audio.AudioOutputConfig(filename=output_audio_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    # Perform the speech synthesis
    result = synthesizer.speak_text_async(str(transcription_from_file)).get()

    # Check result status
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("2. TTS output file saved successfully as " +output_audio_path)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

parser = argparse.ArgumentParser(
    description='tts.py - Create an audio file using text-to-speech based on the text in an input TXT file. Output files will be in /output/tts.'
)

parser.add_argument(
    '-i', '--inputtranscriptionfilename',
    type=str, 
    required=True,
    help='Required. The path of the input transcription file (TXT).'
)

parser.add_argument(
    '-v', '--voice',
    nargs='?', 
    default='alloy', 
    type=str, 
    required=True,
    help='Which voice to use. Can be one of the 6 OpenAI voices (alloy, echo, fable, onyx, nova, shimmer) or one of the many Azure Speech Service voices such as `en-GB-BellaNeural`. Defaults to alloy'
)

# Parse the arguments
args = parser.parse_args()

# Show help message if no arguments are provided
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# Set paths
output_audio_path = os.path.splitext(args.inputtranscriptionfilename)[0] + "_aiaudio.mp3"

print("Starting")

# Load the .env file
load_dotenv()

# Set OpenAI voice dictionary. Available voices from https://platform.openai.com/docs/guides/text-to-speech/quickstart
open_ai_voices = {
    "alloy": 1,
    "ash": 2,
    "coral": 3,
    "echo": 4,
    "fable": 5,
    "onyx": 6,
    "nova": 6,
    "sage": 6,
    "shimmer": 6
}

# Get the transcription
with open(args.inputtranscriptionfilename, "r") as file:
    # Read the entire content of the file
    transcription_from_file = file.read()

# If the voice is an OpenAI voice, use that service, otherwise process as a Azure Speech voice
if args.voice in open_ai_voices:
    openai()
else:
    azurespeech()

print("Tts.py is complete")












