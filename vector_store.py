from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_vector_db():
    with open("knowledge.txt") as f:
        docs = f.readlines()

    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_texts(docs, embeddings)
    return db