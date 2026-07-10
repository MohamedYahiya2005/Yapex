import chromadb
import os
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# SHORT-TERM MEMORY
session_store = {}

def save_to_redis(session_id: str, role: str, content: str):
    if session_id not in session_store:
        session_store[session_id] = []
    # Keep only last 10 messages — faster!
    if len(session_store[session_id]) > 10:
        session_store[session_id].pop(0)
    session_store[session_id].append(f"{role}: {content}")

def get_from_redis(session_id: str):
    if session_id not in session_store:
        return ""
    return "\n".join(session_store[session_id])

# LONG-TERM MEMORY — cached so loads only once!
@st.cache_resource
def get_vectorstore():
    print("Loading memory... (only once!)")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    chroma_client = chromadb.PersistentClient(path=".chroma")
    vectorstore = Chroma(
        client=chroma_client,
        collection_name="long_term_memory",
        embedding_function=embeddings
    )
    return vectorstore

def save_to_chroma(text: str, metadata: dict = {}):
    try:
        vectorstore = get_vectorstore()
        vectorstore.add_texts([text], metadatas=[metadata])
    except:
        pass

def search_chroma(query: str, k: int = 2):
    try:
        vectorstore = get_vectorstore()
        results = vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
    except:
        return [] 