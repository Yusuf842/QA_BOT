import streamlit as st
import pdfplumber
import json
import os
import sys
import warnings
warnings.filterwarnings("ignore")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.main import QA

def process_pdf_and_save_to_json(uploaded_pdf, output_json_path='data/data.json'):
    data = []
    
    with pdfplumber.open(uploaded_pdf) as pdf:
        total_pages = len(pdf.pages)
        progress_bar = st.progress(0)
        
        for i in range(total_pages):
            page = pdf.pages[i]
            text = page.extract_text()
            lines = text.split('\n')
            entry = {}
            for line in lines:
                if line.startswith("ID: "):
                    entry['id'] = line.replace("ID: ", "").strip()
                elif line.startswith("Title: "):
                    entry['title'] = line.replace("Title: ", "").strip()
                elif line.startswith("Context: "):
                    entry['context'] = line.replace("Context: ", "").strip()
                elif line.startswith("Question: "):
                    entry['question'] = line.replace("Question: ", "").strip()
                elif line.startswith("Answer: "):
                    if 'answers' not in entry:
                        entry['answers'] = {'text': []}
                    entry['answers']['text'].append(line.replace("Answer: ", "").strip())
            
            # Only add entry if it has an 'id' and other required fields are present
            if entry.get('id') and entry.get('title') and entry.get('context') and entry.get('question'):
                data.append(entry)
            
            # Update progress bar
            progress_percentage = (i + 1) / total_pages
            progress_bar.progress(progress_percentage)
        
    # Write data to JSON file after processing all pages
    with open(output_json_path, 'w') as f:
        json.dump(data, f, indent=4)
        
    st.success(f"PDF data saved to {output_json_path}")


def main():
    st.title("Upload File and Generate QA Data")
    
    # Check and initialize session state
    if 'pinecone_api_key' not in st.session_state:
        st.session_state.pinecone_api_key = ''
    if 'cohere_api_key' not in st.session_state:
        st.session_state.cohere_api_key = ''
    if 'qa' not in st.session_state:
        st.session_state.qa = QA()
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file and not st.session_state.pdf_processed:
        process_pdf_and_save_to_json(uploaded_file)
        st.session_state.pdf_processed = True
        st.success("Now you can run the QA setup.")
    
    # API key inputs
    st.session_state.pinecone_api_key = st.text_input("Enter Pinecone API key", type="password", value=st.session_state.pinecone_api_key)
    st.session_state.cohere_api_key = st.text_input("Enter Cohere API key", type="password", value=st.session_state.cohere_api_key)
    
    # QA setup button
    if st.button("Run QA Setup"):
        if st.session_state.pinecone_api_key and st.session_state.cohere_api_key:
            qa = st.session_state.qa  
            qa.qa_setup(PINECONE_API_KEY=st.session_state.pinecone_api_key, COHERE_API_KEY=st.session_state.cohere_api_key)
            st.success("QA Setup completed. You can now ask questions.")
    
    # Query input
    if 'question' not in st.session_state:
        st.session_state.question = ''
    
    st.session_state.question = st.text_input("Ask a question", value=st.session_state.question)
    if st.session_state.question:
        qa = st.session_state.qa  
        answer = qa.answer(query=st.session_state.question)
        st.write(f"Answer: {answer}")

if __name__ == "__main__":
    main()
