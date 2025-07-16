# app.py — Streamlit UI client for Dialect CC
import streamlit as st
import requests
import json
import asyncio
import websockets
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Replace with actual cloud-hosted backend when ready
BACKEND_URL = "https://japanese-disagree-champion-ministries.trycloudflare.com"
WS_URL = "wss://japanese-disagree-champion-ministries.trycloudflare.com"


# 🌐 Supported Languages
supported_languages = [
    {"name_en": "English", "native": "English", "code": "en"},
    {"name_en": "Hindi", "native": "हिन्दी", "code": "hi"},
    
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
    {"name_en": "Dhivehi", "native": "ދިވެހި", "code": "dv"},
    {"name_en": "Dogri", "native": "डोगरी", "code": "doi"},
    {"name_en": "Dutch", "native": "Nederlands", "code": "nl"},
    {"name_en": "English", "native": "English", "code": "en"},
    {"name_en": "Esperanto", "native": "Esperanto", "code": "eo"},
    {"name_en": "Estonian", "native": "Eesti", "code": "et"},
    {"name_en": "Ewe", "native": "Eʋegbe", "code": "ee"},
    {"name_en": "Filipino", "native": "Filipino", "code": "tl"},
    {"name_en": "Finnish", "native": "Suomi", "code": "fi"},
    {"name_en": "French", "native": "Français", "code": "fr"},
    {"name_en": "Frisian", "native": "Frysk", "code": "fy"},
    {"name_en": "Galician", "native": "Galego", "code": "gl"},
    {"name_en": "Georgian", "native": "ქართული", "code": "ka"},
    {"name_en": "German", "native": "Deutsch", "code": "de"},
    {"name_en": "Greek", "native": "Ελληνικά", "code": "el"},
    {"name_en": "Guarani", "native": "Avañe’ẽ", "code": "gn"},
    {"name_en": "Gujarati", "native": "ગુજરાતી", "code": "gu"},
    {"name_en": "Haitian Creole", "native": "Kreyòl ayisyen", "code": "ht"},
    {"name_en": "Hausa", "native": "Hausa", "code": "ha"},
    {"name_en": "Hawaiian", "native": "ʻŌlelo Hawaiʻi", "code": "haw"},
    {"name_en": "Hebrew", "native": "עברית", "code": "he"},
    {"name_en": "Hindi", "native": "हिन्दी", "code": "hi"},
    {"name_en": "Hmong", "native": "Hmoob", "code": "hmn"},
    {"name_en": "Hungarian", "native": "Magyar", "code": "hu"},
    {"name_en": "Icelandic", "native": "Íslenska", "code": "is"},
    {"name_en": "Igbo", "native": "Asụsụ Igbo", "code": "ig"},
    {"name_en": "Ilocano", "native": "Ilokano", "code": "ilo"},
    {"name_en": "Indonesian", "native": "Bahasa Indonesia", "code": "id"},
    {"name_en": "Irish", "native": "Gaeilge", "code": "ga"},
    {"name_en": "Italian", "native": "Italiano", "code": "it"},
    {"name_en": "Japanese", "native": "日本語", "code": "ja"},
    {"name_en": "Javanese", "native": "Basa Jawa", "code": "jv"},
    {"name_en": "Kannada", "native": "ಕನ್ನಡ", "code": "kn"},
    {"name_en": "Kazakh", "native": "Қазақ тілі", "code": "kk"},
    {"name_en": "Khmer", "native": "ភាសាខ្មែរ", "code": "km"},
    {"name_en": "Kinyarwanda", "native": "Kinyarwanda", "code": "rw"},
    {"name_en": "Konkani", "native": "कोंकणी", "code": "gom"},
    {"name_en": "Korean", "native": "한국어", "code": "ko"},
    {"name_en": "Krio", "native": "Krio", "code": "kri"},
    {"name_en": "Kurdish (Kurmanji)", "native": "Kurmancî", "code": "ku"},
    {"name_en": "Kurdish (Sorani)", "native": "سۆرانی", "code": "ckb"},
    {"name_en": "Kyrgyz", "native": "Кыргызча", "code": "ky"},
    {"name_en": "Lao", "native": "ພາສາລາວ", "code": "lo"},
    {"name_en": "Latin", "native": "Latina", "code": "la"},
    {"name_en": "Latvian", "native": "Latviešu", "code": "lv"},
    {"name_en": "Lingala", "native": "Lingála", "code": "ln"},
    {"name_en": "Lithuanian", "native": "Lietuvių", "code": "lt"},
    {"name_en": "Luganda", "native": "Luganda", "code": "lg"},
    {"name_en": "Luxembourgish", "native": "Lëtzebuergesch", "code": "lb"},
    {"name_en": "Macedonian", "native": "Македонски", "code": "mk"},
    {"name_en": "Maithili", "native": "मैथिली", "code": "mai"},
    {"name_en": "Malagasy", "native": "Malagasy", "code": "mg"},
    {"name_en": "Malay", "native": "Bahasa Melayu", "code": "ms"},
    {"name_en": "Malayalam", "native": "മലയാളം", "code": "ml"},
    {"name_en": "Maltese", "native": "Malti", "code": "mt"},
    {"name_en": "Maori", "native": "Māori", "code": "mi"},
    {"name_en": "Marathi", "native": "मराठी", "code": "mr"},
    {"name_en": "Meiteilon (Manipuri)", "native": "ꯃꯤꯇꯩꯂꯣꯟ", "code": "mni-Mtei"},
    {"name_en": "Mizo", "native": "Mizo ṭawng", "code": "lus"},
    {"name_en": "Mongolian", "native": "Монгол", "code": "mn"},
    {"name_en": "Myanmar (Burmese)", "native": "မြန်မာ", "code": "my"},
    {"name_en": "Nepali", "native": "नेपाली", "code": "ne"},
    {"name_en": "Norwegian", "native": "Norsk", "code": "no"},
    {"name_en": "Odia (Oriya)", "native": "ଓଡ଼ିଆ", "code": "or"},
    {"name_en": "Oromo", "native": "Afaan Oromoo", "code": "om"},
    {"name_en": "Pashto", "native": "پښتو", "code": "ps"},
    {"name_en": "Persian", "native": "فارسی", "code": "fa"},
    {"name_en": "Polish", "native": "Polski", "code": "pl"},
    {"name_en": "Portuguese", "native": "Português", "code": "pt"},
    {"name_en": "Punjabi", "native": "ਪੰਜਾਬੀ", "code": "pa"},
    {"name_en": "Quechua", "native": "Runasimi", "code": "qu"},
    {"name_en": "Romanian", "native": "Română", "code": "ro"},
    {"name_en": "Russian", "native": "Русский", "code": "ru"},
    {"name_en": "Samoan", "native": "Gagana Samoa", "code": "sm"},
    {"name_en": "Sanskrit", "native": "संस्कृतम्", "code": "sa"},
    {"name_en": "Scots Gaelic", "native": "Gàidhlig", "code": "gd"},
    {"name_en": "Sepedi", "native": "Sesotho sa Leboa", "code": "nso"},
    {"name_en": "Serbian", "native": "Српски", "code": "sr"},
    {"name_en": "Sesotho", "native": "Sesotho", "code": "st"},
    {"name_en": "Shona", "native": "ChiShona", "code": "sn"},
    {"name_en": "Sindhi", "native": "سنڌي", "code": "sd"},
    {"name_en": "Sinhala", "native": "සිංහල", "code": "si"},
    {"name_en": "Slovak", "native": "Slovenčina", "code": "sk"},
    {"name_en": "Slovenian", "native": "Slovenščina", "code": "sl"},
    {"name_en": "Somali", "native": "Soomaaliga", "code": "so"},
    {"name_en": "Spanish", "native": "Español", "code": "es"},
    {"name_en": "Sundanese", "native": "Basa Sunda", "code": "su"},
    {"name_en": "Swahili", "native": "Kiswahili", "code": "sw"},
    {"name_en": "Swedish", "native": "Svenska", "code": "sv"},
    {"name_en": "Tajik", "native": "Тоҷикӣ", "code": "tg"},
    {"name_en": "Tamil", "native": "தமிழ்", "code": "ta"},
    {"name_en": "Tatar", "native": "Татарча", "code": "tt"},
    {"name_en": "Telugu", "native": "తెలుగు", "code": "te"},
    {"name_en": "Thai", "native": "ไทย", "code": "th"},
    {"name_en": "Tigrinya", "native": "ትግርኛ", "code": "ti"},
    {"name_en": "Tsonga", "native": "Xitsonga", "code": "ts"},
    {"name_en": "Turkish", "native": "Türkçe", "code": "tr"},
    {"name_en": "Turkmen", "native": "Türkmençe", "code": "tk"},
    {"name_en": "Twi", "native": "Twi", "code": "ak"},
    {"name_en": "Ukrainian", "native": "Українська", "code": "uk"},
    {"name_en": "Urdu", "native": "اردو", "code": "ur"},
    {"name_en": "Uyghur", "native": "ئۇيغۇرچە", "code": "ug"},
    {"name_en": "Uzbek", "native": "Oʻzbekcha", "code": "uz"},
    {"name_en": "Vietnamese", "native": "Tiếng Việt", "code": "vi"},
    {"name_en": "Welsh", "native": "Cymraeg", "code": "cy"},
    {"name_en": "Xhosa", "native": "isiXhosa", "code": "xh"},
    {"name_en": "Yiddish", "native": "ייִדיש", "code": "yi"},
    {"name_en": "Yoruba", "native": "Yorùbá", "code": "yo"},
    {"name_en": "Zulu", "native": "isiZulu", "code": "zu"},
]

def get_user_info():
    st.sidebar.title("🗣️ Dialect CC - Live Subtitle")
    user_id = st.sidebar.text_input("🧑 Your Name", value=f"user-{uuid.uuid4().hex[:6]}")
    
    options = [f"{lang['native']} ({lang['name_en']})" for lang in supported_languages]
    selected = st.sidebar.selectbox("🌐 Your Preferred Language", options, index=0)
    lang_code = supported_languages[options.index(selected)]["code"]

    return user_id.strip(), lang_code

def connect_user(user_id, lang_code):
    try:
        res = requests.post(f"{BACKEND_URL}/connect_user", params={"user_id": user_id, "language": lang_code})
        return res.status_code == 200
    except:
        return False

async def subtitle_loop(user_id, lang_code):
    placeholder = st.empty()
    uri = f"{WS_URL}/{user_id}"

    try:
        async with websockets.connect(uri) as ws:
            while True:
                await ws.send(f"{user_id}::Hello from frontend::{lang_code}")
                response = await ws.recv()
                data = json.loads(response)
                lines = [f"**{sub['user']}**: {sub['translated']}" for sub in data.get("subtitles", [])]
                placeholder.markdown("\n\n".join(lines))
                await asyncio.sleep(1)
    except Exception as e:
        st.error(f"WebSocket error: {e}")

def main():
    st.set_page_config(layout="wide", page_title="Dialect CC - Real-time Subtitles")
    st.title("📡 Dialect CC — Real-Time Multilingual Live Subtitles")

    user_id, lang_code = get_user_info()

    if connect_user(user_id, lang_code):
        st.success(f"✅ Connected as **{user_id}** with subtitles in `{lang_code}`")
        asyncio.run(subtitle_loop(user_id, lang_code))
    else:
        st.error("❌ Failed to connect to backend.")

if __name__ == "__main__":
    main()
    