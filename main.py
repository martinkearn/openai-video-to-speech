import os
import requests
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip

# Load the .env file
load_dotenv()

# Set vars
audio_file_name="output_audio.wav"
audio_tts_file_name="output_tts_audio.mp3"

# Get the audio from the video
print("Getting the audio from the video")
video = VideoFileClip("video.mp4")
audio = video.audio
audio.write_audiofile(audio_file_name)

# Get the audio as a transcript via OpenAI
print("Transcribing the audio")
transcription_client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version = "2024-02-15-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)
transcription_result = transcription_client.audio.transcriptions.create(
    file=open("./"+audio_file_name, "rb"),            
    model=os.getenv("AZURE_OPENAI_WHISPER_DEPLOYMENT")
)
print(transcription_result.text)

# Get the speech audio from transcription
print("Converting the transcription to AI speech audio")
tts_url = os.getenv("AZURE_OPENAI_ENDPOINT") +"/openai/deployments/" +os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT") +"/audio/speech?api-version=2024-02-15-preview"
tts_headers_list = {
 "api-key": os.getenv("AZURE_OPENAI_API_KEY"),
 "Content-Type": "application/json" 
}
tts_payload = json.dumps({
    "model": "tts-1-hd",
    "input": str(transcription_result.text),
    "voice": os.getenv("AZURE_OPENAI_TTS_VOICE")
})
tts_response = requests.request("POST", tts_url, data=tts_payload,  headers=tts_headers_list)
if tts_response.status_code == 200:
    # Save the binary content to a file
    with open(audio_tts_file_name, 'wb') as file:
        file.write(tts_response.content)
    print("TTS output file saved successfully as " +audio_tts_file_name)
else:
    print(f"Failed to retrieve content. Status code: {tts_response.status_code}")
    print(f"Response content: {tts_response.content}")