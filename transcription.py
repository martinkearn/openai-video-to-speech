import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip

# Load the .env file
load_dotenv()

# Set vars
video_file_name="video.mov"
audio_file_name="output_original_audio.wav"
transcription_file_name="output_transcription.txt"

# Get the audio from the video
print("Getting the audio from the video " +video_file_name)
video = VideoFileClip(video_file_name)
audio = video.audio
audio.write_audiofile(audio_file_name)
print()

# Get the audio as a transcript via OpenAI
print("Transcribing the audio")
transcription_client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version = "2024-02-15-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)
transcription_result = transcription_client.audio.transcriptions.create(
    file=open("./"+audio_file_name, "rb"),            
    model=os.getenv("AZURE_OPENAI_WHISPER_DEPLOYMENT"),
    language="en")

with open(transcription_file_name, "w") as file:
    file.write(transcription_result.text)
print()

print("We have a transcription result (has also been written to " +transcription_file_name +")")
print()

print(transcription_result.text)