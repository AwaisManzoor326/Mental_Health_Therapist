import os
from PyPDF2 import PdfReader
import docx
from pydub import AudioSegment
import speech_recognition as sr

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(docx_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text

def extract_text_from_audio(audio_path):
    """Extract text from an audio file (WAV, MP3, etc.)."""
    # Convert to WAV if needed
    if not audio_path.endswith(".wav"):
        sound = AudioSegment.from_file(audio_path)
        audio_path = "temp_audio.wav"
        sound.export(audio_path, format="wav")

    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
        try:
            return r.recognize_google(audio)
        except:
            return "[Could not transcribe audio]"
