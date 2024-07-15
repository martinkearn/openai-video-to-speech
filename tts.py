import os
import requests
import json
import sys
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get args if they exist
if len(sys.argv) > 1:
    voice = sys.argv[1]
else:
    voice = os.getenv("AZURE_OPENAI_TTS_VOICE")

# Set vars
transcription_file_name="output_transcription.txt"
audio_tts_file_name="output_tts_audio_" +voice +".mp3"

# Get the speech audio from transcription
print("Converting " +transcription_file_name +" to AI text-to-speech audio with the " +voice +" voice")
with open(transcription_file_name, "r") as file:
    # Read the entire content of the file
    transcription_from_file = file.read()
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