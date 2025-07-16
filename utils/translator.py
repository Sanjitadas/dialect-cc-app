# utils/translator.py

import os
import requests

def ai_translate(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates given text from source_lang to target_lang using a context-aware AI.
    Uses local Hugging Face, Cohere, or other API integration as needed.
    """
    if source_lang == target_lang or not text.strip():
        return text

    try:
        # Template prompt for AI-based context-aware translation
        prompt = (
            f"Translate this sentence from {source_lang} to {target_lang}. "
            f"Respond only with the final translated sentence:\n\n{text}"
        )

        # Example using OpenAI-compatible local endpoint
        endpoint = os.getenv("AI_TRANSLATION_ENDPOINT", "http://localhost:11434/v1/chat/completions")

        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "llama3",  # or your configured Ollama model
            "messages": [
                {"role": "system", "content": "You are a smart translator."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = requests.post(endpoint, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()

        result = data['choices'][0]['message']['content']
        return result.strip()

    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return text



