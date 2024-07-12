# openai-video-to-speech
A Python script which converts an MP4 video to speech using Azure OpenAI services.

The script does the following:
1. Take an MP4 video as a input
1. Creates a transcription from the video's audio
1. Create an OpenAI text-to-speech version of the transcription

## Setup OpenAI Services
1. Create an Azure OpenAI service in the North Central US or Sweden Central regions using the steps outlined at https://learn.microsoft.com/en-gb/azure/ai-services/openai/whisper-quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-python 
1. Obtain the `Endpoint` and `Key` from [Azure Portal](https://portal.azure.com/) > The OpenAI service you just created > Keys and Endpoints
1. Using the [Azure OpenAI Studio](https://oai.azure.com/) > Deployments, deploy a `tts-hd` model using the steps outlined in https://learn.microsoft.com/en-gb/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model take a note of the deployment name
1. Using the [Azure OpenAI Studio](https://oai.azure.com/) > Deployments, deploy a `Whisper` model using the steps outlined in https://learn.microsoft.com/en-gb/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model take a note of the deployment name

## Setup Python Environment
1. Create an `.env` file which contains these env variables. Replace the real values with values from the steps above
```
AZURE_OPENAI_API_KEY=Key
AZURE_OPENAI_ENDPOINT=Endpoint
AZURE_OPENAI_TTS_DEPLOYMENT=TtsDeploymentName
AZURE_OPENAI_TTS_VOICE=alloy (or choose any of the OpenAI voice options see https://platform.openai.com/docs/guides/text-to-speech)
AZURE_OPENAI_WHISPER_DEPLOYMENT=WhisperDeploymentname
```
1. Create a Python Virtual Environment `python3 -m venv venv`
1. Activate virtual environment using `venv\Scripts\activate` for Windows or `source venv/bin/activate` on MacOS/Linux
1. Install dependencies `pip3 install -r requirements.txt`

## Create a transcription from a video
1. Add a file called `video.mp4` to the repository root
1. Run script `python transcription.py`
1. This will generate a file called `output_original_audio.wav` which is the original audio from the video
1. This will also generate a file called `output_transcription.txt` which is the transcription
1. You can optionally edit this transcription before converting it to AI speech

## Create AI speech audio from transcription
1. Run script `python tts.py`
1. This will generate a file called `output_tts_audio.mp3` which is the text-to-speech AI audio based on the contents of `output_transcription.txt`

