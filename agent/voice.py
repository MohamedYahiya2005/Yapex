import speech_recognition as sr

def transcribe_voice_realtime(live_placeholder=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            if live_placeholder:
                live_placeholder.markdown("🎙️ Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
            if live_placeholder:
                live_placeholder.markdown("⚙️ Processing...")
            text = recognizer.recognize_google(audio, language="en")
            return text
    except sr.WaitTimeoutError:
        return "No speech detected. Try again."
    except sr.UnknownValueError:
        return "Could not understand. Please speak clearly."
    except Exception as e:
        return f"Voice error: {str(e)}"