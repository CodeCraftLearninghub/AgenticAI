from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document 
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

secret = os.getenv("GOOGLE_API_KEY")


docs = [
    "LangChain helps build LLM applications easily.",
    "FAISS is a vector database for similarity search.",
    "Google Gemini provides powerful embedding models.",
    "RAG combines retrieval and generation for AI systems."
]

documents = [Document(page_content=text) for text in docs]

embedding = GoogleGenerativeAIEmbeddings(
    google_api_key=secret,
    model="gemini-embedding-2",
)

vectorstore = FAISS.from_documents(documents, embedding)

q = "what is FAISS used for ?"

response = vectorstore.similarity_search(q, k=2)

print("Quer is : ", q);

print("\n\n  Matches : \nn")

for i, doc in enumerate( response, 1):
    print(doc.page_content)