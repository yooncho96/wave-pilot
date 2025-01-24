# openai_api/openai_helper.py

import os
import sys
import openai
import json
import data.db_helper as db

from dotenv import load_dotenv
load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_MODEL_NAME = os.getenv("AZURE_MODEL_NAME")

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
    
    if db.get_current_idx() > 1:
        previous_data = db.get_all_emotion_data()
        additional_info = (
            "For your information, the user's previous transcripts, AI analysis results, and corrections are here:\n"
            f"{previous_data}\n"
            "Fine tune the results accordingly."
        )
        prompt = prompt + additional_info
        
    else:
        prompt = prompt
    
    try:
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

        # Safely convert to floats, rounded to 1 decimal place
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
