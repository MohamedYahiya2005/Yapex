import os
import io
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio_bytes(audio_bytes):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "voice.wav"

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            language="en"
        )
        return transcription.text.strip()
    except Exception as e:
        return f"Voice error: {str(e)}"