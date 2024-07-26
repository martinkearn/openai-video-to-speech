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

logging.basicConfig(stream=sys.stdout, level=logging.INFO,  # set to logging.DEBUG for verbose output
        format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)


SPEECH_ENDPOINT = os.getenv('SPEECH_ENDPOINT',"https://swedencentral.api.cognitive.microsoft.com/")
API_VERSION = "2024-04-15-preview"
AVATAR_VIDEO_OUTPUT_FILENAME = "output/output_avatar.mp4"
AVATAR_CHARACTER = "max" # talking avatar character
AVATAR_STYLE = "business",  # talking avatar style, required for prebuilt avatar, optional for custom avatar
AVATAR_VOICE = "en-US-OnyxMultilingualNeural"
INPUT_TEXT = "So, what is a workspace label? When we upload TDF files to C, we need a way to route the TDF file to the correct workspace. Traditionally, we'd use something like a UUID for this which is a long alphanumeric string. The problem with this approach is that the low side (C) is not connected to the high side (on premise). This makes it difficult for humans to remember and verbally share the ID. A Workspace Label is a word-based identifier using the approach popularised by the What3Words app. This means that while the label is still unique, it can be easily remembered and recalled by humans without the need for any kind of digital data transfer."


def _create_job_id():
    # the job ID must be unique in current speech resource
    # you can use a GUID or a self-increasing number
    return uuid.uuid4()

def _authenticate():
    SUBSCRIPTION_KEY = os.getenv("AZURE_SPEECH_KEY")
    return {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}


def submit_synthesis(job_id: str):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = {
        'Content-Type': 'application/json'
    }
    header.update(_authenticate())

    payload = {
        'synthesisConfig': {
            "voice": f'{AVATAR_VOICE}',
        },
        "inputKind": "plainText",
        "inputs": [
            {
                "content": INPUT_TEXT
            },
        ],
        "avatarConfig": {
            "talkingAvatarCharacter": f'{AVATAR_CHARACTER}',
            "talkingAvatarStyle": f'business', # API is rejecting f'{AVATAR_STYLE}' for some reason. Not sure why. Have not investigated
            "videoFormat": "mp4",  # mp4 or webm, webm is required for transparent background
            "videoCodec": "h264",  # hevc, h264 or vp9, vp9 is required for transparent background; default is hevc
            "subtitleType": "soft_embedded",
            "backgroundColor": "#FFFFFFFF", # background color in RGBA format, default is white; can be set to 'transparent' for transparent background
        }
    }

    response = requests.put(url, json.dumps(payload), headers=header)
    if response.status_code < 400:
        logger.info('Batch avatar synthesis job submitted successfully')
        logger.info(f'Job ID: {response.json()["id"]}')
        return True
    else:
        logger.error(f'Failed to submit batch avatar synthesis job: [{response.status_code}], {response.text}')


def get_synthesis(job_id):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = _authenticate()

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.debug('Get batch synthesis job successfully')
        logger.debug(response.json())
        if response.json()['status'] == 'Succeeded':
            logger.info(f'Batch synthesis job succeeded, download URL: {response.json()["outputs"]["result"]}')

            # Download the video
            download_response = requests.get(response.json()["outputs"]["result"], stream=True)
            if download_response.status_code == 200:
                # Open a local file with write-binary mode
                with open(AVATAR_VIDEO_OUTPUT_FILENAME, 'wb') as file:
                    # Iterate over the response data in chunks
                    for chunk in download_response.iter_content(chunk_size=8192):
                        # Write each chunk to the file
                        file.write(chunk)
                print(f"File downloaded successfully: {AVATAR_VIDEO_OUTPUT_FILENAME}")
            else:
                print(f"Failed to download file. Status code: {response.status_code}")
        elif response.json()['status'] == 'Failed':
            logger.info(f'Batch synthesis job failed')
            logger.info(f'error.message: {response.json()["properties"]["error"]["message"]}')

        return response.json()['status']
    else:
        logger.error(f'Failed to get batch synthesis job: {response.text}')


if __name__ == '__main__':
    job_id = _create_job_id()
    if submit_synthesis(job_id):
        while True:
            status = get_synthesis(job_id)
            if status == 'Succeeded':
                logger.info('batch avatar synthesis job succeeded')
                break
            elif status == 'Failed':
                logger.error('batch avatar synthesis job failed')
                break
            else:
                logger.info(f'batch avatar synthesis job is still running, status [{status}]')
                time.sleep(5)