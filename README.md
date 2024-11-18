# openai-video-to-speech
A set of Python scripts for working with Azure Speech Service and OpenAI for text to speech, and text to avatar.

Video to transcription (`transcription.py`)
1. Take an MP4 video as a input
1. Strip audio from input video
1. Creates a transcription from the audio

Text to speech (`tts.py`)
1. Create an text-to-speech audio file from the transcription (can use `transcription.py` to create the text or provide your own)

Text to avatar with speech (`avatar.py`)
1. Creates AI avatar (with speech) from a  transcription (can use `transcription.py` to create the text or provide your own)

## Setup OpenAI Service
If you want to use Azure OpenAI voices, you need to setup an Azure OpenAI service.

1. Create an Azure OpenAI service in the North Central US or Sweden Central regions using the steps outlined at https://learn.microsoft.com/en-gb/azure/ai-services/openai/whisper-quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-python 
1. Obtain the `Endpoint` and `Key` from [Azure Portal](https://portal.azure.com/) > The OpenAI service you just created > Keys and Endpoints
1. Using the [Azure OpenAI Studio](https://oai.azure.com/) > Deployments, deploy a `tts-hd` model using the steps outlined in https://learn.microsoft.com/en-gb/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model take a note of the deployment name
1. Using the [Azure OpenAI Studio](https://oai.azure.com/) > Deployments, deploy a `Whisper` model using the steps outlined in https://learn.microsoft.com/en-gb/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model take a note of the deployment name
1. Select a voice to use from https://platform.openai.com/docs/guides/text-to-speech. Use `alloy` if unsure

## Setup Azure Speech Service
If you want to use Azure Speech Service voices, you need to setup an Azure Speech service. These voices are not as natural as OpenAI but there is a much broader choice of languages, accents and controls.

> You do can do the same thing that this code is doing with the Azure Speech Service through the [Azure Speech Studio](https://speech.microsoft.com/portal)

1. Open the [Azure Speech Studio](https://speech.microsoft.com/portal)
1. Go to the Voice Gallery
1. Create a `Speech resource` and note the `region` and `resource key`

## Setup Python Environment
1. Create an `.env` file which contains these env variables. Replace the real values with values from the steps above
```
AZURE_OPENAI_API_KEY=Key
AZURE_OPENAI_ENDPOINT=Endpoint
AZURE_OPENAI_TTS_DEPLOYMENT=TtsDeploymentName
AZURE_OPENAI_WHISPER_DEPLOYMENT=WhisperDeploymentname
AZURE_SPEECH_KEY=Key
AZURE_SPEECH_REGION=swedencentral
AZURE_AVATAR_API_VERSION=2024-04-15-preview
```
1. Create a Python Virtual Environment `python3 -m venv venv`
1. Activate virtual environment using `venv\Scripts\activate` for Windows or `source venv/bin/activate` on MacOS/Linux
1. Install dependencies `pip3 install -r requirements.txt`

## Create a transcription from a video
1. Run script `python transcription.py --help` for arguments, options and usage

## Create AI speech audio from transcription
1. Run script `python tts.py --help` for arguments, options and usage

## Create AI avatar video from transcription
1. Run script `python avatar.py --help` for arguments, options and usage

