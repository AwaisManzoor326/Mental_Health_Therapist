import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import playsound

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        return f"[STT Error: {e}]"

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    playsound.playsound(temp_file.name)
    os.remove(temp_file.name)
