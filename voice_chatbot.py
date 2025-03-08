import streamlit as st
import os
import toml
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import tempfile
from playsound import playsound

# Load API Key from config
toml_config = toml.load('config.toml')
api_key = toml_config['api_keys']['gemini']

# Configure Google Gemini API
os.environ["GOOGLE_API_KEY"] = api_key
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def speak(text):
    tts = gTTS(text=text, lang="en")
    
    temp_audio_path = os.path.join(tempfile.gettempdir(), "response.mp3")

    # Ensure file is deleted before saving
    if os.path.exists(temp_audio_path):
        
        try:
            os.remove(temp_audio_path)
        except PermissionError:
            print("File is in use and cannot be deleted.")
            return

    tts.save(temp_audio_path)
    playsound(temp_audio_path)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "Speech service unavailable"

def app():
    st.markdown("""
        <style>
            .container {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                height: 70vh;
            }
            .ball {
                width: 220px;
                height:220px;
                background-color: #ff5733;
                border-radius: 50%;
                animation: pulse 1.5s infinite;
                margin-bottom: 30px;
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.5); }
                100% { transform: scale(1); }
            }
            
            .user-msg, .bot-msg {
                display: flex;
                align-items: center;
                padding: 10px;
                border-radius: 10px;
                margin: 8px 0;
                width: fit-content;
                max-width: 80%;
            }
            .user-msg {
                background: #3b82f6;
                color: white;
                align-self: flex-end;
                margin-left: auto;
            }
            .bot-msg {
                background: #22c55e;
                color: white;
                align-self: flex-start;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🎙️ Voice-to-Voice Chatbot")
    

    col1, col2,col_div,col3 = st.columns([0.3,1.4,0.1, 2])

    
    with col2:
        st.subheader('')
        st.subheader('')
        st.write('')    
        st.markdown('<div class="ball"></div>', unsafe_allow_html=True)
        st.subheader('')
        st.write('')
        st.write('')
        st.write('')
        st.markdown(
            """
            <style>
                .stButton>button {
                    font-size: 20px !important;
                    padding: 15px 25px !important;
                    font-weight: bold
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        start_chat = st.button("🔊 Tap to Start")

        st.markdown('</div>', unsafe_allow_html=True)
    
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    with col_div:
        st.write('')
        st.markdown(
            '''
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 3px solid #FFFFFF; 
                    height: 620px;
                    margin: auto;
                }
            </style>
            ''',
            unsafe_allow_html=True
        )
    
    with col3:

        if start_chat:
            st.write("🎤 Say something...")
            user_input = listen()
            if user_input:
                st.session_state.chat_history.append(("You", user_input))
                st.write("🤖 Chatbot is thinking...")
                response = model.generate_content(user_input).text
                st.session_state.chat_history.append(("Chatbot", response))
                speak(response)
        
        for role, text in st.session_state.chat_history:
            if role == "You":
                st.markdown(f'<div class="user-msg">🗨️ {text}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">🤖 {text}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    app()
