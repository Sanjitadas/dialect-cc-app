# utils/grammar.py

from language_tool_python import LanguageToolPublicAPI

def correct_grammar(text: str, lang_code: str = "en-US") -> str:
    """
    Applies grammar correction based on given language code using LanguageToolPublicAPI.
    """
    try:
        tool = LanguageToolPublicAPI(lang_code)
        matches = tool.check(text)
        corrected = tool.correct(text)
        return corrected.strip()
    except Exception as e:
        print(f"❌ Grammar correction failed: {e}")
        return text



