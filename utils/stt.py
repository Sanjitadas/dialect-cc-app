# utils/stt.py

import speech_recognition as sr
import os
from langid.langid import LanguageIdentifier, model
import whisper

identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
recognizer = sr.Recognizer()

def capture_speech_auto(timeout=4, phrase_time_limit=10):
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            lang = identifier.classify(text)[0]
            return text, lang
    except sr.WaitTimeoutError:
        print("⌛ Timeout: No speech detected.")
        return whisper_fallback()
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return whisper_fallback()
    except Exception as e:
        print(f"🔥 Error: {e}")
        return whisper_fallback()

def whisper_fallback():
    try:
        print("🎙️ Using Whisper fallback...")
        model = whisper.load_model("base")
        audio_file = "temp.wav"

        with sr.Microphone() as source:
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            with open(audio_file, "wb") as f:
                f.write(audio_data.get_wav_data())

        result = model.transcribe(audio_file)
        text = result["text"]
        lang = result["language"]
        return text.strip(), lang
    except Exception as e:
        print(f"❌ Whisper fallback failed: {e}")
        return "", ""













