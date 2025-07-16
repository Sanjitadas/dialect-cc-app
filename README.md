# 🗣️ Dialect CC - Real-Time Multilingual Meeting Subtitles

**Dialect CC** is an AI-enhanced live subtitle system for Microsoft Teams, Webex, and other virtual meetings — built to enable **real-time translation and grammar correction** for all participants, without needing to know their identities or languages in advance.

---

## 💡 Key Features

- 🎙️ **Live Speech Detection** — Captures participants' voice in real time.
- 🌍 **Multilingual Translation** — Each user can select their preferred language to see others' speech translated.
- ✨ **AI Grammar Correction** — Transforms sentences like "I passed out in 2019" → "I graduated in 2019".
- 💬 **Real-Time Subtitles Overlay** — Participants see translated live captions (CC-style).
- ⚡ **Dynamic User Handling** — Works for `n` number of users, with real-time language switching.
- 🧠 **Speaker Detection (via ECAPA-TDNN)** — Automatically identifies who is speaking.

---

## 👥 How It Works

You **don’t know who the users are**, or **what language they’ll use** — and that’s exactly the point!

Users can:

1. **Click the "Dialect CC" button** (via browser extension or Teams app)
2. **Enter a name or use automatic voice detection**
3. **Choose their preferred language** from a dropdown
4. ✅ **Start seeing live subtitles** — everyone’s speech, translated into their own language

No setup needed in advance. No hardcoding of users.

---

## 🛠️ Tech Stack

- 🐍 Python (FastAPI for backend)
- 🔊 `speechbrain` + `ECAPA-TDNN` for speaker clustering
- 🎙️ `speech_recognition` + `whisper` for STT fallback
- 🤖 `language_tool_python` or `OpenAI` / `Cohere` for grammar correction
- 🌐 Streamlit + HTML/JS overlays for subtitle display
- ☁️ Deployable on **Streamlit Cloud**, **Hugging Face Spaces**, or **internal servers**

---

## 🚀 How to Use

### ▶️ Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Launch backend server
python app.py

# Launch subtitle overlay (Streamlit)
streamlit run subtitle_overlay.py

