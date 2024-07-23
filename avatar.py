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


# The endpoint (and key) could be gotten from the Keys and Endpoint page in the Speech service resource.
# The endpoint would be like: https://<region>.api.cognitive.microsoft.com or https://<custom_domain>.cognitiveservices.azure.com
# If you want to use passwordless authentication, custom domain is required.
SPEECH_ENDPOINT = os.getenv('SPEECH_ENDPOINT',"https://northeurope.api.cognitive.microsoft.com")
# We recommend to use passwordless authentication with Azure Identity here; meanwhile, you can also use a subscription key instead
API_VERSION = "2024-04-15-preview"


def _create_job_id():
    # the job ID must be unique in current speech resource
    # you can use a GUID or a self-increasing number
    return uuid.uuid4()

def _authenticate():
    SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY", '7f5b6098b9744f6d9f2c9da08d8bd343')
    return {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}


def submit_synthesis(job_id: str):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = {
        'Content-Type': 'application/json'
    }
    header.update(_authenticate())

    payload = {
        'synthesisConfig': {
            "voice": 'en-GB-RyanNeural',
        },
        "inputKind": "plainText",
        "inputs": [
            {
                "content": "So what is a workspace label? When we upload TDF files to C, we need a way to route the TDF file to the correct workspace. Traditionally, we'd use something like a UUID for this which is a long alphanumeric string. The problem with this approach is that the high side (C) is not connected to the high side on premise. This makes it difficult for humans to remember and verbally share the ID. ",
            },
        ],
        "avatarConfig": {
            "talkingAvatarCharacter": "max",  # talking avatar character
            "talkingAvatarStyle": "business",  # talking avatar style, required for prebuilt avatar, optional for custom avatar
            "videoFormat": "webm",  # mp4 or webm, webm is required for transparent background
            "videoCodec": "vp9",  # hevc, h264 or vp9, vp9 is required for transparent background; default is hevc
            "subtitleType": "soft_embedded",
            "backgroundColor": "transparent"
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
        return response.json()['status']
    else:
        logger.error(f'Failed to get batch synthesis job: {response.text}')


def list_synthesis_jobs(skip: int = 0, max_page_size: int = 100):
    """List all batch synthesis jobs in the subscription"""
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses?api-version={API_VERSION}&skip={skip}&maxpagesize={max_page_size}'
    header = _authenticate()

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.info(f'List batch synthesis jobs successfully, got {len(response.json()["values"])} jobs')
        logger.info(response.json())
    else:
        logger.error(f'Failed to list batch synthesis jobs: {response.text}')


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