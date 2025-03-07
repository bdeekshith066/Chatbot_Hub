import streamlit as st
import pandas as pd
import google.generativeai as genai
import toml
import json
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_lottie import st_lottie

# Load the API key from the config file
config = toml.load('config.toml')
api_key = config['api_keys']['gemini']
def load_lottie_animation(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
    
animation1 = load_lottie_animation("assets/dataanalysis3.json")
animation2 = load_lottie_animation("assets/dataanalysis1.json")
animation3 = load_lottie_animation("assets/dataanalysis2.json")

    
def app():

    col11 , col12 = st.columns([1,1.3])
    with col11:

        gradient_text_html = """
            <style>
            .gradient-text {
                font-weight: bold;
                background: -webkit-linear-gradient(left, #07539e, #4fc3f7, #ffffff);
                background: linear-gradient(to right, #07539e, #4fc3f7, #ffffff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                display: inline;
                font-size: 3em;
            }
            </style>
            <div class="gradient-text">Data Analysis Chatbot</div>
            """

        st.markdown(gradient_text_html, unsafe_allow_html=True)
    
    # File upload section
        uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

    with col12:
        col111 , col122, col123 = st.columns([1,1,1])
        with col111:
            st_lottie(animation1, height=210, key="animation1")
        with col122:
            st_lottie(animation2, height=210, key="animation2")
        with col123:
            st_lottie(animation3, height=210, key="animation3")        

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Display dataset details
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(" #### Distribution of Customers by Place")
            st.write('')
            plt.figure(figsize=(10, 5))
            sns.countplot(y=df['Place'], order=df['Place'].value_counts().index, palette='coolwarm')
            plt.xlabel("Count")
            plt.ylabel("Place")
            st.pyplot(plt)
            st.subheader("Dataset Info")
            st.dataframe(df.head(10))

        with col2:
            st.subheader("Total Bill Amount vs Age")
            plt.figure(figsize=(10, 5))
            sns.scatterplot(x=df['Age'], y=df['Total Bill Amount'], alpha=0.7, color='blue')
            plt.xlabel("Age")
            plt.ylabel("Total Bill Amount")
            st.pyplot(plt)
            col11, col22 =  st.columns(2)
            with col11:
                st.subheader("Data type Info")
                st.write()
                st.write(df.dtypes)
                st.write(f"Number of Rows: {df.shape[0]}")
                
            with col22:
                st.subheader("Missing Values")
                st.write()
                st.write(df.isnull().sum())
                st.write(f"NUmber of Columns: {df.shape[1]}")

        with col3:
            st.subheader("Total Bill Amount by Day")
            plt.figure(figsize=(10, 5))
            sns.boxplot(x=df['Day'], y=df['Total Bill Amount'], palette='coolwarm')
            plt.xlabel("Day")
            plt.ylabel("Total Bill Amount")
            st.pyplot(plt)
            st.subheader("Statistics Summary ")
            st.write(df.describe())

    # Chatbot section
    st.subheader(":orange[Chat with your Data]")
    user_input = st.text_input("Ask a question about your dataset:")

    if user_input and uploaded_file is not None:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        chat = model.start_chat()

        def analyze_dataset_question(df, user_input):
            prompt = f"""
            Analyze the following dataset and answer the question:
            {user_input}

            Dataset:
            {df.head(10).to_csv(index=False)}
            """
            full_response = ""
            try:
                for chunk in chat.send_message(prompt, stream=True):
                    full_response += chunk.text
            except genai.types.generation_types.BlockedPromptException as e:
                st.error(f"Blocked Prompt: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            return full_response

        if st.button("Get Analysis"):
            st.spinner("Generating response...")
            response = analyze_dataset_question(df, user_input)
            if response:
                st.write("Response:")
                st.write(response)

if __name__ == "__main__":
    app()
