import google.generativeai as genai
import streamlit as st
import time
import toml
import pytesseract
from PIL import Image
import re

import json
from streamlit_lottie import st_lottie


def load_lottie_animation(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
    
animation1 = load_lottie_animation("assets/api_animation.json")
animation2 = load_lottie_animation("assets/apichatbot.json")


# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the API key from the config file
config = toml.load('config.toml')
api_key = config['api_keys']['gemini']

def app():
    
    col01, col02 = st.columns([1, 0.5])
    with col01:
        gradient_text_html = """
            <style>
            .gradient-text {
                font-weight: bold;
                background: -webkit-linear-gradient(left, #07539e, #4fc3f7, #ffffff);
                background: linear-gradient(to right, #07539e, #4fc3f7, #ffffff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                display: inline;
                font-size: 2.4em;
            }
            </style>
            <div class="gradient-text">AI-Powered Neurorehabilitation Assistant</div>
            """

        st.markdown(gradient_text_html, unsafe_allow_html=True)

        st.write("""
        Please provide your details in the text area below or upload your prescription. Rest assured, your confidential information will remain secure.:
        1. Age, Gender, and date of diagnosis or injury
        2. Current Symptoms, medical history including chronic conditions, past injuries.
        3. Pre-condition activity level, specific physical goals, and any short-term or long-term recovery goals.
        4. Current level of mobility and any aids being used (e.g., cane, walker, wheelchair).
        5. Assessment of memory, attention, executive function, and any difficulties with speech or language.
        6. Mood, anxiety, depression, or other psychological concerns.
        7. Availability of support from family, friends, and any modifications made to the home to support recovery.
        8. Previous rehabilitation therapies undergone and their outcomes, and use of any specific neurorehabilitation devices.

        For sample details -> www.nologin.in and domain name -> apichatbot
        """)

        # Text area for user input
        user_input = st.text_area("Enter your details here:")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat()

        # Generate neurorehabilitation plan
        def generate_neurorehab_plan(user_input):
            prompt = f"""
            Patient Information:
            {user_input}

            Please act as a professional neurorehabilitation therapist and provide the following:
            1. A brief assessment based on the provided information.
            2. A detailed neurorehabilitation plan in a table format for daily exercises and activities, including descriptions and durations.
            3. Recommendations and precautions for the patient to ensure a safe and effective recovery process.

            The plan should cover:
            - Initial phase (weeks 1-2)
            - Intermediate phase (weeks 3-6)
            - Advanced phase (weeks 7-12)

            Ensure that the exercises and activities are appropriate for someone recovering from a neurological condition and that they progressively increase in intensity as the patient heals.
            """

            full_response = ""
            try:
                for chunk in chat.send_message(prompt, stream=True):
                    full_response += chunk.text
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)

            return full_response

        # Upload Prescription Image
        st.write("### Upload Prescription Image")
        uploaded_file = st.file_uploader("Upload an image of the prescription", type=['jpg', 'png', 'jpeg'])

        # Initialize text for redacted text and image display
        text = ""
        redacted_text = ""
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            # Perform OCR on the uploaded image
            text = pytesseract.image_to_string(image)

            # Redact sensitive information
            redacted_text = re.sub(r'[0-9]{10}', '[REDACTED]', text)  # Redact phone numbers
            

            # Display the columns for image preview, extracted text, and redacted text
            col11, col22, col33 = st.columns(3)

            with col11:
                st.write("**Image Preview:**")
                st.image(uploaded_file, use_column_width=True)

            with col22:
                st.write(":orange[Extracted Text]:")
                st.text(text)

            with col33:
                st.write("**:orange[Redacted Text]:**")
                st.text(redacted_text)

        # Always show the submit button
        submit_button = st.button("Submit for Plan Generation")

        if submit_button:
            # Use the user input from the text area or the redacted text from image
            input_text = user_input if user_input else redacted_text
            if input_text:
                with st.spinner("Generating Neurorehabilitation Plan..."):
                    time.sleep(4)
                    neurorehab_plan = generate_neurorehab_plan(input_text)
                    st.success(neurorehab_plan)
            else:
                st.warning("Please provide details in the text area or upload a prescription.")
    
    with col02:
        col111 , col122 = st.columns([1,1])
        with col111:
            st_lottie(animation1, height=135, key="animation1")
        with col122:
            st_lottie(animation2, height=135, key="animation2")
    
        with st.form('Question2'):
            st.write("  - :orange[About this Chatbot]")
            st.write("""
            This chatbot is powered by the Gemini API, which enables it to generate intelligent and context-aware responses.    
            This chatbot acts as a professional neurorehabilitation therapist and provides answers as a professional neurorehabilitation therapist no matter what question you ask.
        
            It leverages Google Bard, a powerful LLM to understand and generate human-like responses, making it highly adaptable to various cases.
            Prompt engineering plays a crucial role, as it tailors the AI's behavior by providing clear and specific instructions.
            
            This system redacts sensitive info like phone numbers from prescription images to protect user privacy while providing useful text.
            This way you can make the chatbot for a specific case and for general case visit the multilingual chatbot
            """)

            if st.form_submit_button("Hope it helped"):
                st.write("Feel free to customise and use it. Push any improvements to the repo!")
                linkedin_url = "https://www.linkedin.com/in/deekshith2912/"
                linkedin_link = f"[Deekshith B]({linkedin_url})"
                st.markdown(f"###### Developed by {linkedin_link}")
            
        

if __name__ == "__main__":
    app()
