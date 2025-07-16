# utils/stt.py

import speech_recognition as sr
from langid.langid import LanguageIdentifier, model
import socket

# Initialize
recognizer = sr.Recognizer()
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

def has_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Check if internet connection is available.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def capture_speech_auto(timeout=4, phrase_time_limit=10):
    """
    Captures microphone input and transcribes using Google's STT (requires internet).
    Returns: (text, language_code) or ("", "") if failed.
    """
    if not has_internet():
        print("⚠️ No internet connection.")
        return "Please check your internet connection.", "en"

    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            lang = identifier.classify(text)[0]
            return text.strip(), lang
    except sr.WaitTimeoutError:
        print("⌛ Timeout: No speech detected.")
        return "No speech detected. Please try again.", "en"
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return "Could not understand audio. Try again.", "en"
    except Exception as e:
        print(f"🔥 Error: {e}")
        return f"Error: {e}", "en"















