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
    '-iv', '--inputvideofilename',
    type=str, 
    help='The path and file name of the input video. Example input/video.mov'
)

parser.add_argument(
    '-oa', '--outputaudiofilename',
    nargs='?', 
    default='output/transcription/output_original_audio.mp3', 
    type=str, 
    help='The path of the output audio file (MP3). Defaults to output/transcription/output_original_audio.mp3'
)

parser.add_argument(
    '-ot', '--outputtranscriptionfilename',
    nargs='?', 
    default='output/transcription/output_transcription.txt', 
    type=str, 
    help='The path of the output transcription file (TXT). Defaults to output/transcription/output_transcription.txt'
)

# Parse the arguments
args = parser.parse_args()

# Show help message if no arguments are provided
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# Load the .env file
load_dotenv()

# Get the audio from the video
print("1. Getting the audio from the video " +args.inputvideofilename)
video = VideoFileClip(args.inputvideofilename)
audio = video.audio
audio.write_audiofile(args.outputaudiofilename)

# Get the audio as a transcript via OpenAI
print("2. Transcribing the audio")
transcription_client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version = "2024-02-15-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)
transcription_result = transcription_client.audio.transcriptions.create(
    file=open("./"+args.outputaudiofilename, "rb"),           
    model=os.getenv("AZURE_OPENAI_WHISPER_DEPLOYMENT"),
    language="en")

with open(args.outputtranscriptionfilename, "w") as file:
    file.write(transcription_result.text)

print("3. Written transcription to " +args.outputtranscriptionfilename)
print("Done")