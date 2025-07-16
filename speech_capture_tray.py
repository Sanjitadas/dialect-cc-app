import sys
import os
import time
import threading
import speech_recognition as sr
import requests
import torch
import torchaudio
from speechbrain.pretrained import SpeakerRecognition # type: ignore

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu

# === Configuration ===
BACKEND_URL = "http://localhost:8000/live_speak"

# === Speaker Recognition Setup ===
recognizer = sr.Recognizer()
speaker_model = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_ecapa")
speaker_profiles = {}  # Stores {"user_id": embedding_vector}
default_lang = "en"

# === Microphone Listener Thread ===
def listen_and_send():
    mic = sr.Microphone()
    print("🎤 Microphone activated. Listening...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        with mic as source:
            print("🔊 Listening...")
            try:
                audio = recognizer.listen(source, phrase_time_limit=5)
                print("📼 Got audio")

                # Save audio chunk to temp file
                with open("temp.wav", "wb") as f:
                    f.write(audio.get_wav_data())

                # Speaker embedding
                embedding = speaker_model.encode_batch("temp.wav").squeeze().detach().cpu().numpy()

                # Match or assign speaker ID
                user_id = match_or_create_speaker(embedding)

                # Recognize speech
                text = recognizer.recognize_google(audio)
                print(f"🗣️ [{user_id}]: {text}")

                # Send to backend
                requests.post(BACKEND_URL, params={"user_id": user_id, "text": text, "lang": default_lang})

            except Exception as e:
                print(f"❌ Error: {e}")

# === Speaker Clustering ===
def match_or_create_speaker(new_emb, threshold=0.75):
    from scipy.spatial.distance import cosine

    for user_id, saved_emb in speaker_profiles.items():
        if cosine(new_emb, saved_emb) < threshold:
            return user_id

    # New speaker
    new_id = f"user{len(speaker_profiles)+1}"
    speaker_profiles[new_id] = new_emb
    print(f"👤 New speaker identified: {new_id}")
    return new_id

# === Tray App ===
class CCTrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QtGui.QIcon("icons/icon128.png"))
        self.tray.setVisible(True)

        self.menu = QMenu()
        self.start_action = self.menu.addAction("Start CC")
        self.quit_action = self.menu.addAction("Quit")
        self.tray.setContextMenu(self.menu)

        self.start_action.triggered.connect(self.start_listening)
        self.quit_action.triggered.connect(self.quit_app)

    def start_listening(self):
        print("✅ CC Started")
        self.tray.showMessage("Dialect CC", "Live transcription started.")
        t = threading.Thread(target=listen_and_send, daemon=True)
        t.start()

    def quit_app(self):
        print("👋 Exiting CC app")
        self.tray.hide()
        QtWidgets.qApp.quit()

    def run(self):
        self.app.exec_()

# === Start Tray ===
if __name__ == '__main__':
    tray_app = CCTrayApp()
    tray_app.run()



