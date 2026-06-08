import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq


import os
from dotenv import load_dotenv

load_dotenv()
secret = os.getenv("GROQ_API_KEY")


# Configuration
llm = ChatGroq(model='qwen/qwen3-32b', api_key=secret)
embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

# Functions
def Augmentation(pdf_path):
    """Process PDF and create vector database"""
    pdfload = PyPDFLoader(file_path=pdf_path)
    pdf_docs = pdfload.load()
    db = FAISS.from_documents(documents=pdf_docs, embedding=embedding)
    db.save_local('VectorDB')
    return True

def Retrieval(question):
    """Retrieve relevant documents from vector database"""
    db = FAISS.load_local('VectorDB', embedding, allow_dangerous_deserialization=True)
    refs = db.similarity_search(question, k=3)
    return refs

def Generation(question, refs):
    """Generate answer based on question and references"""
    answer = llm.invoke(f"Here is the user question: {question}\n\nHere are the references: {refs}")
    return answer.content

# Streamlit UI
st.set_page_config(page_title="RAG Q&A System", page_icon="📚", layout="wide")

st.title("📚 RAG-based Q&A System")
st.markdown("Upload a PDF document and ask questions about its content.")

# Sidebar for PDF Upload
with st.sidebar:
    st.header("📤 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("Process PDF", type="primary"):
            with st.spinner("Processing PDF and creating vector database..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Process the PDF
                    Augmentation(tmp_path)
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    st.success("✅ PDF processed successfully!")
                    st.session_state['pdf_processed'] = True
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
    
    st.divider()
    st.markdown("### About")
    st.markdown("""
    This application uses:
    - **LangChain** for document processing
    - **FAISS** for vector storage
    - **Groq** for LLM inference
    - **HuggingFace** embeddings
    """)

# Main area for Q&A
st.header("💬 Ask Questions")

if 'pdf_processed' not in st.session_state:
    st.info("👈 Please upload and process a PDF document first.")
else:
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if question := st.chat_input("Ask a question about the document..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Retrieve relevant documents
                    refs = Retrieval(question)
                    
                    # Generate answer
                    answer = Generation(question, refs)
                    
                    st.markdown(answer)
                    
                    # Show references in expander
                    with st.expander("📄 View References"):
                        for i, ref in enumerate(refs, 1):
                            st.markdown(f"**Reference {i}:**")
                            st.text(ref.page_content[:500] + "..." if len(ref.page_content) > 500 else ref.page_content)
                            st.divider()
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

