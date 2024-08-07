# openai-video-to-speech
A Python script which converts an MP4 video to speech using Azure OpenAI services.

The script does the following:
1. Take an MP4 video as a input
1. Creates a transcription from the video's audio
1. Create an OpenAI text-to-speech version of the transcription

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
AZURE_SPEECH_REGION=uksouth
TTS_VOICE=alloy
```
1. Create a Python Virtual Environment `python3 -m venv venv`
1. Activate virtual environment using `venv\Scripts\activate` for Windows or `source venv/bin/activate` on MacOS/Linux
1. Install dependencies `pip3 install -r requirements.txt`

## Create a transcription from a video
1. Run script `python transcription.py --help` for arguments, options and usage

## Create AI speech audio from transcription
1. Run script `python tts.py`. You can optionally pass in a voice as a parameter, which can be one of the 6 OpenAI voices (`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`) or one of the many Azure Speech Service voices such as `en-GB-BellaNeural`. For example `python tts.py alloy` or `python tts.py en-GB-BellaNeural`. If nothing is passed, the script defaults to what is in the `.env` file under `TTS_VOICE` which is OpenAI Alloy.
1. This will generate a file called `output_tts_audio_VOICE.mp3` which is the text-to-speech AI audio based on the contents of `output_transcription.txt`

