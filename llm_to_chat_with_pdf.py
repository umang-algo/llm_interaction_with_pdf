import os
import sqlite3
import streamlit as st
from datetime import datetime
from langchain.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import fitz  # PyMuPDF
from PIL import Image
import io

# Initialize the database
def init_db():
    conn = sqlite3.connect('chat_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS interactions
                 (id INTEGER PRIMARY KEY, username TEXT, question TEXT, answer TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

# Function to save interaction to the database
def save_interaction(username, question, answer):
    conn = sqlite3.connect('chat_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO interactions (username, question, answer, timestamp) VALUES (?, ?, ?, ?)",
              (username, question, answer, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

# Function to load PDF content
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

# Function to initialize the vector store and QA chain
def initialize_qa_chain(documents):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings)
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
    return qa_chain, vectorstore

# Function to convert PDF to images with improved quality
def convert_pdf_to_images(file_path):
    doc = fitz.open(file_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Increase the DPI for better quality
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append(img)
    return images

# Login page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Simple authentication (for demonstration purposes only)
        if username and password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
        else:
            st.error("Please enter both username and password")

# Streamlit app
def main():
    init_db()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()
    else:
        st.title("Umang's PaperPal: Your Trusted Companion for PDF Queries")

        # Input OpenAI API key
        api_key = st.text_input("Enter your OpenAI API key", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        # File uploader
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        
        if uploaded_file is not None:
            # Save uploaded file to a temporary location
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Load PDF content
            documents = load_pdf("temp.pdf")
            
            # Initialize QA chain
            try:
                qa_chain, vectorstore = initialize_qa_chain(documents)
                st.success("PDF loaded and QA chain initialized successfully!")
            except Exception as e:
                st.error(f"Error initializing QA chain: {e}")
                return
            
            # Layout for side by side view
            col1, col2 = st.columns(2)
            
            with col1:
                # Display PDF pages using PyMuPDF with improved quality
                st.write("## PDF Viewer")
                pdf_images = convert_pdf_to_images("temp.pdf")
                for img in pdf_images:
                    st.image(img, use_column_width=True)
            
            with col2:
                # Chat interface
                user_input = st.text_area("Ask a question about the uploaded PDF (Shift + Enter for new line, Enter to submit)", height=300)
                if st.button("Submit"):
                    try:
                        response = qa_chain({"query": user_input})

                        # Extract answer
                        answer = response.get('result', 'No answer available')

                        st.write("Answer:", answer)

                        save_interaction(st.session_state['username'], user_input, answer)
                    except Exception as e:
                        st.error(f"Error getting response: {e}")

if __name__ == "__main__":
    main()
