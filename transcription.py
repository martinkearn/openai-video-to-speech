import os
import sys
import argparse
from openai import AzureOpenAI
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip

print("Starting")

parser = argparse.ArgumentParser(
    description='transcription.py - Converts a video into an MP3 audio track and then produces TXT transcription based on the audio track. Output files will be in /output/transcription.'
)

parser.add_argument(
    '-v', '--videofilename',
    type=str, 
    help='The path and file name of the input video. Example input/video.mov'
)

# Parse the arguments
args = parser.parse_args()

# Show help message if no arguments are provided
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# Load the .env file
load_dotenv()

# Set vars
audio_file_name="output/transcription/output_original_audio.mp3"
transcription_file_name="output/transcription/output_transcription.txt"

# Get the audio from the video
print("1. Getting the audio from the video " +args.videofilename)
video = VideoFileClip(args.videofilename)
audio = video.audio
audio.write_audiofile(audio_file_name)

# Get the audio as a transcript via OpenAI
print("2. Transcribing the audio")
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

print("3. Written transcription to " +transcription_file_name)
print("Done")