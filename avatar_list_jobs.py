#!/usr/bin/env python
  # coding: utf-8
  
  # Copyright (c) Microsoft. All rights reserved.
  # Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
  
import json
import logging
import os
import sys
import requests

logging.basicConfig(stream=sys.stdout, level=logging.INFO,  # set to logging.DEBUG for verbose output
        format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)


SPEECH_ENDPOINT = os.getenv('SPEECH_ENDPOINT',"https://swedencentral.api.cognitive.microsoft.com/")
API_VERSION = "2024-04-15-preview"

def _authenticate():
    SUBSCRIPTION_KEY = os.getenv("AZURE_SPEECH_KEY")
    return {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}


def list_synthesis_jobs(skip: int = 0, max_page_size: int = 100):
    """List all batch synthesis jobs in the subscription"""
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses?api-version={API_VERSION}&skip={skip}&maxpagesize={max_page_size}'
    header = _authenticate()

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.info(f'List batch synthesis jobs successfully, got {len(response.json()["value"])} jobs')
        # Pretty print the JSON data
        pretty_json = json.dumps(response.json(), indent=4)
        print(pretty_json)
    else:
        logger.error(f'Failed to list batch synthesis jobs: {response.text}')


if __name__ == '__main__':
    list_synthesis_jobs(0, 100)