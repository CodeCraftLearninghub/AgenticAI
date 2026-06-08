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

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()
secret = os.getenv("GOOGLE_API_KEY")



loader = PyPDFLoader('doc-1.pdf')
docs = loader.load()

splitters = CharacterTextSplitter (
    chunk_size=1000,
    chunk_overlap=0
)

chunks = splitters.split_documents(docs)


embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=secret,
    model="gemini-embedding-2", 
)

vectorstore = FAISS.from_documents(chunks, embeddings)

query = "what are the http status codes we have ?"


response = vectorstore.similarity_search(query, k=2 )

print("\n Quer : \n\n")

for i, result in enumerate(response, 1):
    print("----- chunk {i}------")
    print(result.page_content)


