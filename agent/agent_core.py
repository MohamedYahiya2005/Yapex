import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from agent.memory import save_to_redis, get_from_redis, save_to_chroma, search_chroma
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )

def chat(user_input: str, session_id: str = "default") -> str:
    # Only search memory if conversation is long enough
    recent_history = get_from_redis(session_id)
    
    # Skip ChromaDB for short simple messages — makes it super fast!
    short_messages = ["hi", "hello", "hey", "ok", "okay", 
                      "thanks", "bye", "yes", "no", "cool"]
    
    if user_input.lower().strip() in short_messages:
        # Skip memory search — reply instantly!
        memory_context = ""
    else:
        # Only search memory for real questions
        past_memories = search_chroma(user_input)
        memory_context = "\n".join(past_memories) if past_memories else ""

    system_prompt = f"""You are YAPEX, a smart and friendly AI assistant.
Be conversational and natural. For simple greetings reply shortly and instantly.

{f"Past context: {memory_context}" if memory_context else ""}
{f"Recent chat: {recent_history}" if recent_history else ""}
"""
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    llm = get_llm()
    response = llm.invoke(messages)
    answer = response.content

    # Save to memory in background
    save_to_redis(session_id, "user", user_input)
    save_to_redis(session_id, "assistant", answer)
    
    # Only save important conversations to ChromaDB
    if user_input.lower().strip() not in short_messages:
        save_to_chroma(
            f"User: {user_input}\nAssistant: {answer}",
            metadata={"session": session_id}
        )

    return answer