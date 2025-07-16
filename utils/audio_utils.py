import tkinter as tk
from tkinter import filedialog

def adjust_mic_sensitivity():
    # Placeholder: can be linked to audio calibration logic
    return 300

def choose_audio_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an audio file",
        filetypes=[("Audio Files", "*.wav *.mp3 *.mp4")]
    )
    return file_path

