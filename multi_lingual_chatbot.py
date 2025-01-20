import google.generativeai as genai # for connecting to the Gemini API for generating responses.
import streamlit as st
import googletrans
from googletrans import Translator  #for translating text between languages.
import toml

# Load API key from config file
config = toml.load('config.toml')
api_key = config['api_keys']['gemini']
genai.configure(api_key=api_key)

# Supported languages -  language codes based on the ISO 639-1 standard, which assigns two-letter abbreviations to each language. Helps in identifying the input and output languages during translation.
supported_languages = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mr': 'Marathi',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'ur': 'Urdu',
    'pa': 'Punjabi',
    'ml': 'Malayalam',
    'or': 'Odia',
    'kn': 'Kannada',
    'as': 'Assamese',
    'kok': 'Konkani',
    'ne': 'Nepali',
    'sd': 'Sindhi',
    'mni': 'Manipuri',
    'doi': 'Dogri',
    'mai': 'Maithili',
    'bho': 'Bhojpuri',
    'sat': 'Santali',
    'ks': 'Kashmiri',
    'chr': 'Chhattisgarhi',
    'new': 'Newari',
    'awa': 'Awadhi',
}

# Translator instance
translator = Translator()

def translate_text(text, src_lang, dest_lang):
    """Translate text from source language to destination language."""
    try:
        # Translate the given text from `src_lang` to `dest_lang`.
        translated = translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return ""

def generate_response(input_text):
    """Generate response from Gemini API."""
    chat = genai.GenerativeModel('gemini-pro').start_chat()
    prompt = f"""
    {input_text}
    Act as a professional assistant skilled in multiple languages.
    Respond comprehensively to the user's query.
    """
    full_response = ""
    try:
        for chunk in chat.send_message(prompt, stream=True):
            full_response += chunk.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
    return full_response

def app():
    
    gradient_text_html = """
    <style>
    .gradient-text {
        font-weight: bold;
        background: -webkit-linear-gradient(left, #FF9933, #ffffff, #138808, #000080);
        background: linear-gradient(to right, #FF9933, #ffffff, #138808, #000080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
        font-size: 3em;
    }
    </style>
    <div class="gradient-text">BharatBot 🇮🇳</div>
"""

    st.markdown(gradient_text_html, unsafe_allow_html=True)

    
    st.write("Get answers to any question in any Indian language and choose your preferred output language. :orange[LearningHasNoBarriers]")

    # Input and Output Language Selection
    st.write("#### Language Selection")
    col1, col2 = st.columns(2)
    with col1:
        input_lang = st.selectbox("Select Input Language", list(supported_languages.values()), key="input_lang")
    with col2:
        output_lang = st.selectbox("Select Output Language", list(supported_languages.values()), key="output_lang")

    # Get language codes for translation
    input_lang_code = list(supported_languages.keys())[list(supported_languages.values()).index(input_lang)]
    output_lang_code = list(supported_languages.keys())[list(supported_languages.values()).index(output_lang)]

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to BharatBot! Ask anything in any Indian language, and BharatBot will respond in your chosen language."}

        ]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input box for user questions
    if prompt := st.chat_input(" Ask anything in any Indian language, and BharatBot will respond in your chosen language."):
        # Adding user's message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Translate user input to English
        translated_input = translate_text(prompt, input_lang_code, 'en')

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("BharatBot is thinking..."):
                response_in_english = generate_response(translated_input)
                translated_response = translate_text(response_in_english, 'en', output_lang_code)
                st.markdown(translated_response)

        # Adding assistant's message to session state
        st.session_state.messages.append({"role": "assistant", "content": translated_response})

if __name__ == "__main__":
    app()
