#!/usr/bin/env python
  # coding: utf-8
  
  # Copyright (c) Microsoft. All rights reserved.
  # Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
  
import json
import logging
import os
import sys
import time
import uuid
import requests
import argparse
from dotenv import load_dotenv

def _authenticate():
    SUBSCRIPTION_KEY = os.getenv("AZURE_SPEECH_KEY")
    return {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}


def submit_synthesis(job_id: str):
    # Get the input text
    with open(args.inputtranscriptionfilename, "r") as file:
        # Read the entire content of the file
        input_text_from_file = file.read()

    url = f'https://{SPEECH_REGION}.api.cognitive.microsoft.com/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = {
        'Content-Type': 'application/json'
    }
    header.update(_authenticate())

    payload = {
        'synthesisConfig': {
            "voice": f'{args.voice}',
        },
        "inputKind": "plainText",
        "inputs": [
            {
                "content": input_text_from_file
            },
        ],
        "avatarConfig": {
            "talkingAvatarCharacter": f'{args.character}',
            "talkingAvatarStyle": f'{args.style}',#f'business', # API is rejecting args.style for some reason. Not sure why. Have not investigated
            "videoFormat": "mp4",  # mp4 or webm, webm is required for transparent background
            "videoCodec": "h264",  # hevc, h264 or vp9, vp9 is required for transparent background; default is hevc
            "subtitleType": "soft_embedded",
            "backgroundColor": "#FFFFFFFF", # background color in RGBA format, default is white; can be set to 'transparent' for transparent background
        }
    }

    response = requests.put(url, json.dumps(payload), headers=header)
    if response.status_code < 400:
        print('Batch avatar synthesis job submitted successfully')
        print(f'Job ID: {response.json()["id"]}')
        return True
    else:
        print(f'Failed to submit batch avatar synthesis job: [{response.status_code}], {response.text}')


def get_synthesis(job_id):
    url = f'https://{SPEECH_REGION}.api.cognitive.microsoft.com/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = _authenticate()

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        if response.json()['status'] == 'Succeeded':
            print(f'Batch synthesis job succeeded, download URL: {response.json()["outputs"]["result"]}')

            # Download the video
            download_response = requests.get(response.json()["outputs"]["result"], stream=True)
            if download_response.status_code == 200:
                # Open a local file with write-binary mode
                with open(args.outputvideofilename, 'wb') as file:
                    # Iterate over the response data in chunks
                    for chunk in download_response.iter_content(chunk_size=8192):
                        # Write each chunk to the file
                        file.write(chunk)
                print(f"File downloaded successfully: {args.outputvideofilename}")
            else:
                print(f"Failed to download file. Status code: {response.status_code}")
        elif response.json()['status'] == 'Failed':
            print(f'Batch synthesis job failed')
            print(f'error.message: {response.json()["properties"]["error"]["message"]}')

        return response.json()['status']
    else:
        print(f'Failed to get batch synthesis job: {response.text}')

# MAIN
# Parse the arguments
parser = argparse.ArgumentParser(
    description='avatar.py - Create a video (Mp4) featuring an AI generated avatar with AI generated voice based on text file input. Output files will be in /output/avatar.'
)

parser.add_argument(
    '-it', '--inputtranscriptionfilename',
    type=str, 
    help='Required. The path of the input transcription file (TXT).'
)

parser.add_argument(
    '-ov', '--outputvideofilename',
    nargs='?', 
    default='output/avatar/output_avatar.mp4', 
    type=str, 
    help='The path of the output video file (MP4). Defaults to "output/avatar/output_avatar.mp4"'
)

parser.add_argument(
    '-v', '--voice',
    nargs='?', 
    default='en-US-FableMultilingualNeural', 
    type=str, 
    help='Which voice to use. Can be one of the many Azure Speech Service voices. Defaults to "en-US-FableMultilingualNeural". See https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts'
)

parser.add_argument(
    '-c', '--character',
    nargs='?', 
    default='harry', 
    type=str, 
    help='The Azure Speech Avatar character to use. Defaults to "harry". See https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/avatar-gestures-with-ssml#supported-prebuilt-avatar-characters-styles-and-gestures'
)

parser.add_argument(
    '-s', '--style',
    nargs='?', 
    default='business', 
    type=str, 
    help='The Azure Speech Avatar character style to use. Defaults to "business". See https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/avatar-gestures-with-ssml#supported-prebuilt-avatar-characters-styles-and-gestures'
)

args = parser.parse_args()

# Show help message if no arguments are provided
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

print("Starting")

# Load the .env file
load_dotenv()

# Get env vars
SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')
API_VERSION = os.getenv('AZURE_AVATAR_API_VERSION')

job_id = uuid.uuid4()
if submit_synthesis(job_id):
    while True:
        status = get_synthesis(job_id)
        if status == 'Succeeded':
            print('Batch avatar synthesis job succeeded')
            break
        elif status == 'Failed':
            print('Batch avatar synthesis job failed')
            break
        else:
            print(f'Batch avatar synthesis job is still running, status [{status}]')
            time.sleep(10)

print("Done")