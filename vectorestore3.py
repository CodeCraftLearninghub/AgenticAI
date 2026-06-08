
# This example demostrates the below flow
#       PDF
#       ↓
#     Loader
#        ↓
#    Chunking
#        ↓
#    Embeddings (Google)
#        ↓
#    FAISS Vector Store
#         ↓
#    User Query
#         ↓
#    Similarity Search
#        ↓
#    Relevant Text Output
#        ↓
#       LLM
#        ↓
#    Final Output







from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

import os
from dotenv import load_dotenv

load_dotenv()
secret = os.getenv("GOOGLE_API_KEY")



# -----------------------------
# 1. Read the Documents from Document Loader
# -----------------------------


loader = PyPDFLoader('doc-1.pdf')

docs  = loader.load()


# -----------------------------
# 2. split the docs to chunks
# -----------------------------


splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0
)

chunks = splitter.split_documents(docs)



# -----------------------------
# 3. Create Embeddings Model
# -----------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=secret,
    model="gemini-embedding-2",
)

# -----------------------------
# 4. Create Vector Store (FAISS) and store 
# -----------------------------
vectorstore = FAISS.from_documents(chunks, embeddings)

# ------------------------
# 5. Gemini LLM
# ------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=secret,
    temperature=0.2
)


def getRagResponse(query):
    # Retrueve relevant chunks

    docs = vectorstore.similarity_search(query, k=2)

    context = "\n\n".join([d.page_content for d in docs])

     # Step c: Build prompt
    prompt = f"""
        You are a helpful AI assistant.
        Answer the question based ONLY on the context below.

    Context:    {context}

    Question:   {query}

    If the answer is not in the context, say "I don't know based on the document."
    """

    response = llm.invoke(prompt)
    return response.content


answer = getRagResponse(" give me something about http status codes  ")

final_result = [item["text"] for item in answer]

print(final_result)