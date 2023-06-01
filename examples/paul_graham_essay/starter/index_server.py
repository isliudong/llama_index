import os
import pickle

# NOTE: for local testing only, do NOT deploy with your key hardcoded
os.environ['OPENAI_API_KEY'] = "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"

from multiprocessing import Lock
from multiprocessing.managers import BaseManager

from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, StorageContext, load_index_from_storage

os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"

index = None
stored_docs = {}
lock = Lock()

index_dir = "./storage"
index_name = "./storage/index.json"
pkl_name = "./stored_documents.pkl"


def list_files(root_dir):
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            all_files.append(os.path.join(root, file))
    for file in all_files:
        print(file)
    return all_files

def initialize_index():
    """Create a new global index, or load one from the pre-set path."""
    global index, stored_docs
    storage_context = StorageContext.from_defaults()
    with lock:
        if bool(0):
            index = load_index_from_storage(storage_context)
        else:
            files = list_files("./documents")
            documents = SimpleDirectoryReader(input_files=files).load_data()
            index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context)
            storage_context.persist(index_dir)
        if os.path.exists(pkl_name):
            with open(pkl_name, "rb") as f:
                stored_docs = pickle.load(f)

def query_index(query_text):
    """Query the global index."""
    global index
    query_engine = index.as_query_engine()
    response = query_engine.query(query_text)
    return response


def insert_into_index(doc_file_path, doc_id=None):
    """Insert new document into global index."""
    global index, stored_docs
    document = SimpleDirectoryReader(input_files=[doc_file_path]).load_data()[0]
    if doc_id is not None:
        document.doc_id = doc_id

    with lock:
        # Keep track of stored docs -- llama_index doesn't make this easy
        stored_docs[document.doc_id] = document.text[0:200]  # only take the first 200 chars

        index.insert(document)
        index.storage_context.persist()
        ##index.save_to_disk(index_name)

        with open(pkl_name, "wb") as f:
            pickle.dump(stored_docs, f)

    return


def get_documents_list():
    """Get the list of currently stored documents."""
    global stored_doc
    documents_list = []
    for doc_id, doc_text in stored_docs.items():
        documents_list.append({"id": doc_id, "text": doc_text})

    return documents_list


if __name__ == "__main__":
    # init the global index
    print("initializing index...")
    initialize_index()

    # setup server
    # NOTE: you might want to handle the password in a less hardcoded way
    manager = BaseManager(('', 5602), b'password')
    manager.register('query_index', query_index)
    manager.register('insert_into_index', insert_into_index)
    manager.register('get_documents_list', get_documents_list)
    server = manager.get_server()

    print("server started...")
    server.serve_forever()
