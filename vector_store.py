"""Small helper for loading the vector database.

LangChain recently moved most of its HuggingFace-related
embeddings to the `langchain_community` package.  The top-level
``langchain.embeddings`` namespace still exists for backwards
compatibility but no longer exports ``HuggingFaceEmbeddings``; trying
to import it from there raises the ``ImportError`` seen in the
traceback.

Importing from ``langchain_community.embeddings`` fixes the problem
and matches the location used internally by the library.  We also
provide an explicit ``model_name`` so users aren't hit by the deprecation
warning about the default value being removed in a future release.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_vector_db():
    with open("knowledge.txt") as f:
        docs = f.readlines()

    # ``model_name`` used here mirrors the default in the upstream
    # implementation; providing it explicitly avoids a deprecation
    # warning that will be raised once the package drops the default.
    # Feel free to change this to any other sentence-transformers model
    # you prefer.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    db = FAISS.from_texts(docs, embeddings)
    return db