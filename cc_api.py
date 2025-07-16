# cc_api.py

from utils.stt import capture_speech_auto
from utils.grammar import correct_grammar
from utils.translator import ai_translate

def process_live_input(source_lang: str, target_lang: str):
    """
    Captures live speech, detects language, applies grammar correction,
    and translates from source_lang to target_lang.
    """
    try:
        raw_text, detected_lang = capture_speech_auto()
        if not raw_text.strip():
            return "❌ No speech detected.", detected_lang

        print(f"🗣️ Recognized: {raw_text} | 🏷️ Detected: {detected_lang}")

        # Grammar correction based on detected language
        corrected_text = correct_grammar(raw_text, detected_lang)
        print(f"✅ Grammar Corrected: {corrected_text}")

        # Translate to target language
        translated_text = ai_translate(corrected_text, source_lang, target_lang)
        print(f"🌐 Translated: {translated_text}")

        return translated_text, detected_lang

    except Exception as e:
        return f"❌ Error in live input processing: {e}", ""








