from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('doc-1.pdf')

docs  = loader.load()

print (len(docs))

print(type(docs))

print(docs[1].page_content)
