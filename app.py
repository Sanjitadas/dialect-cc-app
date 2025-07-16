import streamlit as st
import requests
import json
import asyncio
import websockets

# 🌐 Supported Languages (full A–Z list)
supported_languages = [
    {"name_en": "Afrikaans", "native": "Afrikaans", "code": "af"},
    {"name_en": "Albanian", "native": "Shqip", "code": "sq"},
    {"name_en": "Amharic", "native": "አማርኛ", "code": "am"},
    {"name_en": "Arabic", "native": "العربية", "code": "ar"},
    {"name_en": "Armenian", "native": "Հայերեն", "code": "hy"},
    {"name_en": "Assamese", "native": "অসমীয়া", "code": "as"},
    {"name_en": "Aymara", "native": "Aymar aru", "code": "ay"},
    {"name_en": "Azerbaijani", "native": "Azərbaycan dili", "code": "az"},
    {"name_en": "Bambara", "native": "Bamanankan", "code": "bm"},
    {"name_en": "Basque", "native": "Euskara", "code": "eu"},
    {"name_en": "Belarusian", "native": "Беларуская", "code": "be"},
    {"name_en": "Bengali", "native": "বাংলা", "code": "bn"},
    {"name_en": "Bhojpuri", "native": "भोजपुरी", "code": "bho"},
    {"name_en": "Bosnian", "native": "Bosanski", "code": "bs"},
    {"name_en": "Bulgarian", "native": "Български", "code": "bg"},
    {"name_en": "Catalan", "native": "Català", "code": "ca"},
    {"name_en": "Cebuano", "native": "Bisaya", "code": "ceb"},
    {"name_en": "Chichewa", "native": "ChiCheŵa", "code": "ny"},
    {"name_en": "Chinese (Simplified)", "native": "简体中文", "code": "zh-CN"},
    {"name_en": "Chinese (Traditional)", "native": "繁體中文", "code": "zh-TW"},
    {"name_en": "Corsican", "native": "Corsu", "code": "co"},
    {"name_en": "Croatian", "native": "Hrvatski", "code": "hr"},
    {"name_en": "Czech", "native": "Čeština", "code": "cs"},
    {"name_en": "Danish", "native": "Dansk", "code": "da"},
    {"name_en": "Dutch", "native": "Nederlands", "code": "nl"},
    {"name_en": "English", "native": "English", "code": "en"},
    {"name_en": "French", "native": "Français", "code": "fr"},
    {"name_en": "German", "native": "Deutsch", "code": "de"},
    {"name_en": "Gujarati", "native": "ગુજરાતી", "code": "gu"},
    {"name_en": "Hindi", "native": "हिन्दी", "code": "hi"},
    {"name_en": "Italian", "native": "Italiano", "code": "it"},
    {"name_en": "Japanese", "native": "日本語", "code": "ja"},
    {"name_en": "Kannada", "native": "ಕನ್ನಡ", "code": "kn"},
    {"name_en": "Korean", "native": "한국어", "code": "ko"},
    {"name_en": "Malayalam", "native": "മലയാളം", "code": "ml"},
    {"name_en": "Marathi", "native": "मराठी", "code": "mr"},
    {"name_en": "Odia (Oriya)", "native": "ଓଡ଼ିଆ", "code": "or"},
    {"name_en": "Portuguese", "native": "Português", "code": "pt"},
    {"name_en": "Punjabi", "native": "ਪੰਜਾਬੀ", "code": "pa"},
    {"name_en": "Russian", "native": "Русский", "code": "ru"},
    {"name_en": "Spanish", "native": "Español", "code": "es"},
    {"name_en": "Tamil", "native": "தமிழ்", "code": "ta"},
    {"name_en": "Telugu", "native": "తెలుగు", "code": "te"},
    {"name_en": "Turkish", "native": "Türkçe", "code": "tr"},
    {"name_en": "Urdu", "native": "اردو", "code": "ur"},
    {"name_en": "Vietnamese", "native": "Tiếng Việt", "code": "vi"},
    {"name_en": "Xhosa", "native": "isiXhosa", "code": "xh"},
    {"name_en": "Yoruba", "native": "Yorùbá", "code": "yo"},
    {"name_en": "Zulu", "native": "isiZulu", "code": "zu"},
]

# ⚙️ Backend URLs
BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

# 🧠 Get user identity and language
def get_user_info():
    st.sidebar.title("🎙️ Dialect CC - Setup")
    user_id = st.sidebar.text_input("🧑 Your Name (auto assigned if empty)")
    
    lang_labels = [f"{lang['native']} ({lang['name_en']})" for lang in supported_languages]
    default_index = next(i for i, l in enumerate(supported_languages) if l['code'] == "en")
    
    selected_label = st.sidebar.selectbox("🌍 Preferred Language", lang_labels, index=default_index)
    selected_code = supported_languages[lang_labels.index(selected_label)]["code"]

    return user_id.strip() or None, selected_code

# 📡 Register user on backend
def connect_user(user_id, lang_code):
    res = requests.post(f"{BACKEND_URL}/connect_user", params={"user_id": user_id, "language": lang_code})
    return res.status_code == 200

# 🔁 Stream subtitles over WebSocket
async def subtitle_loop(user_id, lang_code):
    subtitle_area = st.empty()
    uri = f"{WS_URL}/ws/{user_id}"
    
    try:
        async with websockets.connect(uri) as ws:
            while True:
                await ws.send("ping")
                data = await ws.recv()
                decoded = json.loads(data)

                subtitle_md = ""
                for entry in decoded.get("subtitles", []):
                    subtitle_md += f"**{entry['user']}**: {entry['translated']}  \n"

                subtitle_area.markdown(subtitle_md)
                await asyncio.sleep(1)
    except Exception as e:
        st.error(f"WebSocket error: {e}")

# 🏁 App Start
def main():
    st.set_page_config(page_title="Dialect CC", layout="wide")
    st.title("🌐 Dialect CC – Real-Time Live Subtitles")
    
    user_id, lang_code = get_user_info()

    if user_id:
        if connect_user(user_id, lang_code):
            st.success(f"Connected as **{user_id}** [{lang_code}]")
            asyncio.run(subtitle_loop(user_id, lang_code))
        else:
            st.error("❌ Backend connection failed.")
    else:
        st.warning("Please enter your name to continue.")

if __name__ == "__main__":
    main()






