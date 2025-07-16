# ✅ utils/translator.py — AI-enhanced translation via Cohere

import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)


async def smart_translate(text: str, source_lang: str = "en", target_lang: str = "en") -> str:
    if source_lang == target_lang or not text.strip():
        return text

    try:
        prompt = (
            f"You are a professional translator. Your task is to translate this text from {source_lang} to {target_lang}. "
            f"Ensure the translation is fluent, grammatically correct, and contextually accurate. Only output the translated text.\n\n"
            f"Text: {text}"
        )

        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=0.4
        )

        return response.text.strip()
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return text





