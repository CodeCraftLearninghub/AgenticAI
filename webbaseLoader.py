from langchain_community.document_loaders import WebBaseLoader

url = "http://codecraftlearning.net"

loader = WebBaseLoader(url)
docs = loader.load()

print(docs[0].page_content)
