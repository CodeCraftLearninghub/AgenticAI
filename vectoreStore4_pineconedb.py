# pip install langchain langchain-community langchain-google-genai pinecone pypdf python-dotenv
# pip install -U langchain-pinecone pinecone
from dotenv import load_dotenv
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
import pinecone
from pinecone import Pinecone, ServerlessSpec


# -------------------------
# Load env
# -------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# -------------------------
# 1. Load PDF
# -------------------------
loader = PyPDFLoader("doc-1.pdf")
docs = loader.load()

# -------------------------
# 2. Chunking
# -------------------------
splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0
)

chunks = splitter.split_documents(docs)

# -------------------------
# 3. Embeddings (Google)
# -------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=GOOGLE_API_KEY,
    model="gemini-embedding-2",
)

# -------------------------
# 4. Initialize Pinecone
# -------------------------

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "rag-demo-index"

# Create index if not exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,  # Google embeddings dimension
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)

# -------------------------
# 5. Vector Store (Pinecone)
# -------------------------
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="text"
)

# -------------------------
# 6. Insert data into Pinecone
# -------------------------
vectorstore.add_documents(chunks)

print("Data inserted into Pinecone!")

# -------------------------
# 7. Gemini LLM
# -------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)

# -------------------------
# 8. RAG function
# -------------------------
def get_answer(question):

    # Retrieve from Pinecone
    docs = vectorstore.similarity_search(question, k=3)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are a helpful assistant.
Answer ONLY using the context below.

Context:
{context}

Question:
{question}

If not found, say "I don't know based on the document."
"""

    response = llm.invoke(prompt)

    return response.content

# -------------------------
# 9. Chat loop
# -------------------------
print("\n🚀 Pinecone RAG Chatbot Ready!")

while True:
    q = input("\nYou: ")

    if q.lower() == "exit":
        break

    answer = get_answer(q)

    print("\n🤖 Bot:", answer)