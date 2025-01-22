# openai_api/openai_helper.py

import os
import sys
import openai
import json

# If using Azure OpenAI:
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE", "https://YOUR-RESOURCE-NAME.openai.azure.com/")
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_AZURE_OPENAI_KEY")
openai.api_version = os.getenv("OPENAI_API_VERSION", "2023-03-15-preview")

AZURE_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME", "YOUR_MODEL_DEPLOYMENT_NAME")


def transcribe_audio_via_openai(audio_file_path: str) -> str:
    """
    Uses OpenAI’s Whisper model to transcribe the audio at audio_file_path.
    Make sure ffmpeg is installed. 
    For Azure's audio endpoint, usage may differ; this is the openai.com approach.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript_obj = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
            transcript_text = transcript_obj["text"]
        return transcript_text
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        return ""


def get_emotion_scores(text: str) -> dict:
    """
    Sends text to Azure OpenAI with a prompt to identify 9 emotions on a 0-10 scale.
    Returns a dict like:
      { 'anger': 5.0, 'sadness': 3.0, ... }
    """
    try:
        prompt = (
            "Identify the severity of the following 9 emotions on a scale of 0 to 10, "
            "based on this text:\n\n"
            f"\"{text}\"\n\n"
            "Emotions: anger, sadness, fear, shame, guilt, jealousy, envy, joy, love.\n"
            "Respond ONLY in the following JSON format:\n"
            "{\n"
            "  \"anger\": <number>,\n"
            "  \"sadness\": <number>,\n"
            "  \"fear\": <number>,\n"
            "  \"shame\": <number>,\n"
            "  \"guilt\": <number>,\n"
            "  \"jealousy\": <number>,\n"
            "  \"envy\": <number>,\n"
            "  \"joy\": <number>,\n"
            "  \"love\": <number>\n"
            "}"
        )

        response = openai.ChatCompletion.create(
            engine=AZURE_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=200
        )

        raw_text = response["choices"][0]["message"]["content"]
        scores = json.loads(raw_text)

        # Safely convert to floats
        emotion_scores = {
            "anger": float(scores.get("anger", 0)),
            "sadness": float(scores.get("sadness", 0)),
            "fear": float(scores.get("fear", 0)),
            "shame": float(scores.get("shame", 0)),
            "guilt": float(scores.get("guilt", 0)),
            "jealousy": float(scores.get("jealousy", 0)),
            "envy": float(scores.get("envy", 0)),
            "joy": float(scores.get("joy", 0)),
            "love": float(scores.get("love", 0)),
        }
        return emotion_scores

    except Exception as e:
        print(f"Error getting emotion scores: {e}", file=sys.stderr)
        return {
            "anger": 0, "sadness": 0, "fear": 0, "shame": 0, "guilt": 0,
            "jealousy": 0, "envy": 0, "joy": 0, "love": 0
        }
