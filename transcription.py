import os
import sys
import argparse
from openai import AzureOpenAI
from dotenv import load_dotenv
from moviepy import VideoFileClip

parser = argparse.ArgumentParser(
    description='transcription.py - Converts a video into an MP3 audio track and then produces TXT transcription based on the audio track. Output files will be in /output/transcription.'
)

parser.add_argument(
    '-i', '--inputvideofilename',
    type=str, 
    help='Required. The absolute path, including file name to the input video.'
)

# Parse the arguments
args = parser.parse_args()

# Show help message if no arguments are provided
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

print("Starting")

# Set paths
output_audio_path = os.path.splitext(args.inputvideofilename)[0] + "_audio.mp3"
output_transcription_path = os.path.splitext(args.inputvideofilename)[0] + "_transcription.txt"

# Load the .env file
load_dotenv()

# Get the audio from the video
print("1. Getting the audio from the video " +args.inputvideofilename)
video = VideoFileClip(args.inputvideofilename)
audio = video.audio
audio.write_audiofile(output_audio_path)
video.close()
audio.close()

# Get the audio as a transcript via OpenAI
print("2. Transcribing the audio")
transcription_client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version = "2024-02-15-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)
transcription_result = transcription_client.audio.transcriptions.create(
    file=open(output_audio_path, "rb"),           
    model=os.getenv("AZURE_OPENAI_WHISPER_DEPLOYMENT"),
    language="en")

with open(output_transcription_path, "w") as file:
    file.write(transcription_result.text)

print("Transcription.py is complete")