from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def create_vector_store(docs):
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_texts(docs, embeddings)
    return db