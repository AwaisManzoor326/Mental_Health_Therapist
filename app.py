import streamlit as st
from chatbot import MentalHealthChatbot
from file_handler import extract_text_from_pdf, extract_text_from_docx, extract_text_from_audio
from dashboard import show_dashboard
import json
import os
from datetime import datetime
import speech_recognition as sr

GROQ_API_KEY = None    # Replace with your actual API key
chatbot = MentalHealthChatbot(GROQ_API_KEY)

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

session_file = "data/sessions.json"
if not os.path.exists(session_file):
    with open(session_file, "w") as f:
        json.dump([], f)

with open(session_file, "r") as f:
    session_history = json.load(f)

st.set_page_config(page_title="Mental Health Therapist Chatbot 🌸")
st.sidebar.title("Menu")
menu = st.sidebar.radio("Navigate", ["New Session", "History", "Dashboard"])

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now")
        audio = r.listen(source, phrase_time_limit=10)
    try:
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        return f"[STT Error: {e}]"

if menu == "New Session":
    st.title("Mental Health Therapist Chatbot 🌸")
    st.write("Describe your problem below. You can type or speak your message.")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload PDF, DOCX, or Audio/Video file (optional)", 
        type=["pdf","docx","mp4","wav","mp3"]
    )
    if uploaded_file:
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        if uploaded_file.name.endswith(".pdf"):
            file_text = extract_text_from_pdf(file_path)
        elif uploaded_file.name.endswith(".docx"):
            file_text = extract_text_from_docx(file_path)
        elif uploaded_file.name.endswith((".mp4", ".wav", ".mp3")):
            file_text = extract_text_from_audio(file_path)
        else:
            file_text = "[Unsupported file type]"
        st.info(f"Extracted content:\n{file_text}")
    else:
        file_text = ""

    # Chat input
    user_input = st.text_input("Type your message:")
    if st.button("Send") and user_input.strip() != "":
        combined_input = f"{user_input}\n{file_text}" if file_text else user_input
        response = chatbot.ask(combined_input)
        risk = chatbot.assess_risk(combined_input)
        hospitals = chatbot.recommend_hospital(risk)
        st.markdown(f"**AI Therapist:** {response}")
        st.markdown(f"**Risk Level:** {risk}")
        st.markdown(f"**Hospital Recommendations:** {', '.join(hospitals)}")

        # Save session
        session_history.append({
            "date": str(datetime.now()),
            "input": combined_input,
            "response": response,
            "risk_level": risk,
            "recommended_hospitals": hospitals,
            "session_type": "text",
            "mood": 5
        })
        with open(session_file, "w") as f:
            json.dump(session_history, f)

    # Voice input
    if st.button("Record Voice"):
        voice_text = record_audio()
        st.info(f"Transcribed: {voice_text}")
        if voice_text.strip() != "":
            response = chatbot.ask(voice_text)
            risk = chatbot.assess_risk(voice_text)
            hospitals = chatbot.recommend_hospital(risk)
            st.markdown(f"**AI Therapist:** {response}")
            st.markdown(f"**Risk Level:** {risk}")
            st.markdown(f"**Hospital Recommendations:** {', '.join(hospitals)}")

            # Save session
            session_history.append({
                "date": str(datetime.now()),
                "input": voice_text,
                "response": response,
                "risk_level": risk,
                "recommended_hospitals": hospitals,
                "session_type": "voice",
                "mood": 5
            })
            with open(session_file, "w") as f:
                json.dump(session_history, f)

elif menu == "History":
    st.title("Session History")
    if session_history:
        st.dataframe(session_history)
    else:
        st.info("No sessions yet.")

elif menu == "Dashboard":
    show_dashboard(session_history)
