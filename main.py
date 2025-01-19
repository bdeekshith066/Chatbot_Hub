
import streamlit as st

from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="Chatbot_Hub",page_icon="🤖",)

import home , Chatbot_Hub.rule_based_chatbot as rule_based_chatbot, Chatbot_Hub.keyword_based_chatbot as keyword_based_chatbot, Chatbot_Hub.api_based_chatbot as api_based_chatbot, Chatbot_Hub.multi_lingual_chatbot as multi_lingual_chatbot, Chatbot_Hub.data_analysis_chatbot as data_analysis_chatbot, Chatbot_Hub.rag_chatbot as rag_chatbot, Chatbot_Hub.voice_chatbot as voice_chatbot, Chatbot_Hub.multi_modal_chatbot as multi_modal_chatbot


# Reducing whitespace on the top of the page
st.markdown("""
<style>

.block-container
{
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-top: 1rem;
}

</style>
""", unsafe_allow_html=True)



class MultiApp:
    def __init__(self):
        self.app = []

    def add_app(self, title, func):
        self.app.append({
            "title": title,
            "function": func
        })   

    def run(self):
        with st.sidebar:
            st.markdown("""
          <style>
            .gradient-text {
              margin-top: -20px;
            }
          </style>
        """, unsafe_allow_html=True)
            
            typing_animation = """
            <h3 style="text-align: left;">
            <img src="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=30&Left=true&vLeft=true&width=250&height=80&lines=The Chatbot Hub" alt="Typing Animation" />
            </h3>
            """
            st.markdown(typing_animation, unsafe_allow_html=True)
            st.sidebar.write("")
            
            app = option_menu(
                menu_title='Sections',
                options=['Home','Keyword-Based Chatbot','Rule-Based Chatbot','API-Based Chatbot','Analytical-Chatbot','RAG-Chatbot','MultiLingual Chatbot','Voice-Chatbot', 'MultiModal-Chatbot'],
                default_index=0,
            )
            
        if app == "Home":
            home.app()
        elif app == "Keyword-Based Chatbot":
            keyword_based_chatbot.app()
        elif app == "Rule-Based Chatbot":
            rule_based_chatbot.app()
        elif app == "API-Based Chatbot":
            api_based_chatbot.app()
        elif app == "Analytical-Chatbot":
            data_analysis_chatbot.app()
        elif app == "RAG-Chatbot":
            rag_chatbot.app()
        elif app == "MultiLingual Chatbot":
            multi_lingual_chatbot.app()
        elif app == "Voice-Chatbot":
            voice_chatbot.app()
        elif app == "MultiModal-Chatbot":
            multi_modal_chatbot.app()

MultiApp().run()
