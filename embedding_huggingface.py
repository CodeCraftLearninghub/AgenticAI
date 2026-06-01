# pip install -U langchain langchain-openai


from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    check_embedding_ctx_length=False
)

vector = embeddings.embed_query(
    "What is Retrieval Augmented Generation?"
)

print(vector[:10])