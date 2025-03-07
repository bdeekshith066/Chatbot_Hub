import streamlit as st
import os
import time
import toml
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API Key from config
toml_config = toml.load('config.toml')
api_key = toml_config['api_keys']['gemini']

# Configure Google Gemini API
os.environ["GOOGLE_API_KEY"] = api_key
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

# Run the Streamlit app
def app():

    col01, col02 = st.columns([1, 0.4])
    with col01:
        #for title styling -- blue gradient.
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
            <div class="gradient-text">RAG Chatbot</div>
            """

        st.markdown(gradient_text_html, unsafe_allow_html=True)

    
        st.write("Upload a PDF and get accurate responses from its contents.")

        # Function to process and embed PDF
        def vector_embedding(uploaded_file):
            if "vectors" not in st.session_state:
                with open("temp_uploaded_file.pdf", "wb") as temp_file:
                    temp_file.write(uploaded_file.read())
                
                # Load and process the document
                st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                st.session_state.loader = PyPDFLoader("temp_uploaded_file.pdf")
                st.session_state.docs = st.session_state.loader.load()
                st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:20])
                st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
                os.remove("temp_uploaded_file.pdf")

        # Upload PDF
        uploaded_file = st.file_uploader("📂 Upload a PDF", type=["pdf"], help="Upload a document to process")

        if st.button("🔍 Process Document") and uploaded_file:
            vector_embedding(uploaded_file)
            st.success("✅ Document has been embedded and is ready for queries!")

        # Question Input
        prompt1 = st.text_input("💬 Ask a question from the document")

        if prompt1:
            if "vectors" in st.session_state:
                prompt = ChatPromptTemplate.from_template(
                    """
                    You are an AI assistant that helps users extract information from uploaded documents.
                    Provide accurate responses based on the context provided and avoid adding external knowledge.
                    <context>
                    {context}
                    </context>
                    Question: {input}
                    """
                )
                document_chain = create_stuff_documents_chain(llm, prompt)
                retriever = st.session_state.vectors.as_retriever()
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                
                start = time.process_time()
                response = retrieval_chain.invoke({'input': prompt1})
                st.write("⏳ Response time:", round(time.process_time() - start, 2), "seconds")
                st.write("### 🤖 Answer:", response['answer'])

                with st.expander("🔍 Document Similarity Search"):
                    for i, doc in enumerate(response["context"]):
                        st.write(f"**Chunk {i+1}:**")
                        st.write(doc.page_content)
                        st.write("---")
            else:
                st.warning("⚠️ Please embed the document first by clicking 'Process Document'.")

    with col02:

        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        with st.form('Question2'):
            st.write("  - :orange[About this Chatbot]")
            st.write("This chatbot helps users extract information from PDFs using Retrieval-Augmented Generation (RAG). Users can upload a document, and the chatbot will process its contents, allowing them to ask questions and receive precise answers based only on the document's data. It ensures accuracy by embedding text and retrieving relevant sections before generating a response.")
            if st.form_submit_button("Hope it helped"):
                st.write("Feel free to customise and use it. Push any improvements to the repo!")
                linkedin_url = "https://www.linkedin.com/in/deekshith2912/"
                linkedin_link = f"[Deekshith B]({linkedin_url})"
                st.markdown(f"###### Developed by {linkedin_link}")
        
        with st.form('Question3'):
            st.write("  - :orange[How It Works]")
            st.write("The chatbot uses vector embedding to process PDFs efficiently. When a document is uploaded, its content is split into smaller chunks, which are converted into numerical vectors using Google Gemini embeddings. These vectors are stored allowing quick and accurate retrieval of relevant information. When a user asks a question, the chatbot searches for the most relevant document chunks, ensuring responses are based strictly on the provided content.")
            if st.form_submit_button("Hope it helped"):
                st.write("Feel free to customise and use it. Push any improvements to the repo!")
                linkedin_url = "https://www.linkedin.com/in/deekshith2912/"
                linkedin_link = f"[Deekshith B]({linkedin_url})"
                st.markdown(f"###### Developed by {linkedin_link}")

if __name__ == "__main__":
    app()
