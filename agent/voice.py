import os
import streamlit as st
import speech_recognition as sr

@st.cache_resource
def get_recognizer():
    r = sr.Recognizer()
    r.energy_threshold = 200
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    return r

def transcribe_voice_realtime(live_placeholder=None):
    r = get_recognizer()
    try:
        with sr.Microphone() as source:
            if live_placeholder:
                live_placeholder.markdown(
                    '<div class="live-box">🎙️ Listening... Speak now!</div>',
                    unsafe_allow_html=True
                )
            r.adjust_for_ambient_noise(source, duration=0.3)
            audio = r.listen(source, timeout=10, phrase_time_limit=20)

            if live_placeholder:
                live_placeholder.markdown(
                    '<div class="live-box">⚙️ Processing...</div>',
                    unsafe_allow_html=True
                )

            # Try Google first (needs little internet)
            try:
                text = r.recognize_google(
                    audio,
                    language="en-IN"  # Indian English!
                )
                return text

            # If no internet, fall back to offline
            except sr.RequestError:
                try:
                    text = r.recognize_sphinx(audio)
                    return text
                except:
                    return "No internet for voice. Please type instead."

    except sr.WaitTimeoutError:
        return "No speech detected. Try again."
    except sr.UnknownValueError:
        return "Could not understand. Please speak clearly."
    except Exception as e:
        return f"Voice error: {str(e)}"