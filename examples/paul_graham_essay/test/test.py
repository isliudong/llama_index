from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader('../data').load_data()
index = GPTVectorStoreIndex.from_documents(documents)

