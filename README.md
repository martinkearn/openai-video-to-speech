# openai-video-to-speech
A Python script which converts an MP4 video to speech using Azure OpenAI services.

The script does the following:
1. Take an MP4 video as a input
1. Extracts the audio track as an MP3

## Get Started
1. Create an Azure OpenAI service in the North Central US or Sweden Central regions using the steps outlined at https://learn.microsoft.com/en-gb/azure/ai-services/openai/whisper-quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-python 
1. Obtain the `Endpoint` and `Key` from [Azure Portal](https://portal.azure.com/) > The OpenAI service you just created > Keys and Endpoints
1. Using the [Azure OpenAI Studio](https://oai.azure.com/) > Deployments, deploy a `tts-hd` model using the steps outlined in https://learn.microsoft.com/en-gb/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model take a note of the deployment name
1. Using the [Azure OpenAI Studio](https://oai.azure.com/) > Deployments, deploy a `Whisper` model using the steps outlined in https://learn.microsoft.com/en-gb/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model take a note of the deployment name
1. Create an `.env` file which contains these env variables. Replace the real values with values from the steps above
```
AZURE_OPENAI_API_KEY=Key
AZURE_OPENAI_ENDPOINT=Endpoint
AZURE_OPENAI_TTS_DEPLOYMENT=TtsDeploymentName
AZURE_OPENAI_TTS_VOICE=alloy (or choose any of the OpenAI voice options see https://platform.openai.com/docs/guides/text-to-speech)
AZURE_OPENAI_WHISPER_DEPLOYMENT=WhisperDeploymentname
```
1. Add a file called `video.mp4` to the repository root
1. Create a Python Virtual Environment `python3 -m venv venv`
1. Activate virtual environment using `venv\Scripts\activate` for Windows or `source venv/bin/activate` on MacOS/Linux
1. Install dependencies `pip3 install -r requirements.txt`
1. Run script `python main.py`
