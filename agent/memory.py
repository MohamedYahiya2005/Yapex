import uuid
import chromadb
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# SHORT-TERM MEMORY
session_store = {}

def save_to_redis(session_id: str, role: str, content: str):
    if session_id not in session_store:
        session_store[session_id] = []
    if len(session_store[session_id]) > 10:
        session_store[session_id].pop(0)
    session_store[session_id].append(f"{role}: {content}")

def get_from_redis(session_id: str):
    if session_id not in session_store:
        return ""
    return "\n".join(session_store[session_id])

# LONG-TERM MEMORY — ChromaDB's own built-in embedder (no langchain, no torch)
@st.cache_resource
def get_collection():
    client = chromadb.PersistentClient(path=".chroma")
    return client.get_or_create_collection(name="long_term_memory")

def save_to_chroma(text: str, metadata: dict = {}):
    try:
        collection = get_collection()
        collection.add(documents=[text], metadatas=[metadata], ids=[str(uuid.uuid4())])
    except Exception:
        pass

def search_chroma(query: str, k: int = 2):
    try:
        collection = get_collection()
        results = collection.query(query_texts=[query], n_results=k)
        return results.get("documents", [[]])[0]
    except Exception:
        return []