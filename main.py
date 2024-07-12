import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip

# Load the .env file
load_dotenv()

# Set vars
audio_file_name="output_audio.wav"

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
    model=os.getenv("AZURE_OPENAI_TRANSCRIPTION_DEPLOYMENT")
)

print(transcription_result)