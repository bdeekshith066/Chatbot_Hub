import streamlit as st

def app():
    
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
        <div class="gradient-text">Welcome to The Chatbot Hub</div>
        """

    st.markdown(gradient_text_html, unsafe_allow_html=True)
    st.write('')
    st.write(
    "Discover the fascinating world of conversational AI with our :orange[Chatbot Hub, a unique compilation featuring over 10 types of chatbots].  \n"
    "This project showcases diverse chatbot designs, from rule-based systems to advanced AI-powered models, each tailored for different applications.  \n"
    "Explore, interact, and learn how these virtual assistants enhance communication, streamline processes, and redefine user experiences across industries."
    )

    st.markdown(" #### Introduction to  Chatbots")
    st.write(" -  A chatbot is a computer program that mimics human conversation, allowing people to interact with digital systems through text or voice.  \n -   It can answer questions, provide information, or help complete tasks, making communication with technology easier and more natural.  \n -  Chatbots are widely used in industries like customer support, healthcare, and education to streamline processes and improve user engagement.")


    st.markdown(" #### A Brief History of Chatbots")
    st.write("  - The first chatbot, :orange[ELIZA, was developed in the 1960s by Joseph Weizenbaum].  \n -  ELIZA used basic pattern matching techniques to simulate a conversation, but it could only respond to specific inputs.  \n  -  1970s-1990s: Chatbots continued to develop, with bots like :orange[PARRY (a simulation of a person with paranoid schizophrenia) and ALICE],   \n  which used pattern recognition and could hold more complex conversations.")
    

    st.markdown("#### Recent Developments")
    st.write("  - Chatbots evolved from basic rules-based systems to more sophisticated AI-powered bots.  \n  This was driven by advancements in :orange[Natural Language Processing (NLP) and machine learning], making bots more conversational and adaptable.")
    st.write("  - :orange[Libraries] like spaCy, Rasa, and Haystack empower developers to build bots that understand context and respond naturally.  \n   :orange[Frameworks] like LangChain and TensorFlow enable advanced AI-powered chatbots by chaining responses, maintaining context, and leveraging dynamic inputs.  \n :orange[Tools] like Hugging Face Transformers allow developers to fine-tune pre-trained models for domain-specific applications, making bots smarter and more versatile.")
    st.write("  - AI models such as OpenAI's GPT, Google's Gemini, Meta's LLaMA, and Anthropic's Claude offer  APIs that enable seamless integration.  \n These models have revolutionized chatbots by providing real-time services, driving widespread adoption, and  enhancing user engagement across various industries")
    
    st.write('---')
    col1,col2,col3 = st.columns([0.5,1,0.2])
    with col2:
        
        linkedin_url = "https://www.linkedin.com/in/deekshith2912/"
        linkedin_link = f"[Deekshith B]({linkedin_url})"
        st.markdown(f"## Developed by {linkedin_link}")

    
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    
