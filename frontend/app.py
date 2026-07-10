import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import uuid
from agent.agent_core import chat
from agent.voice import transcribe_voice_realtime

st.set_page_config(
    page_title="YAPEX",
    page_icon="🏎️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

.stApp {
    background: radial-gradient(ellipse at top, #1a0000 0%, #0d0d0d 50%, #000000 100%);
    color: #f0f0f0;
}

/* YAPEX Logo */
.yapex-logo {
    text-align: center;
    margin: 20px 0 5px 0;
}

.yapex-y { color: #ff2020; font-size: 3.5em; }
.yapex-a { color: #ff6600; font-size: 4em; }
.yapex-p { color: #ffcc00; font-size: 3.5em; }
.yapex-e { color: #ff2020; font-size: 4.2em; }
.yapex-x { color: #ff4444; font-size: 3.5em; }

.yapex-letters {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    letter-spacing: 12px;
    line-height: 1;
    display: inline-block;
}

.yapex-subtitle {
    text-align: center;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85em;
    letter-spacing: 4px;
    color: #555555;
    margin-bottom: 25px;
    text-transform: uppercase;
}

/* Animated divider */
.divider {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0 auto 25px auto;
    max-width: 500px;
}

.divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, transparent, #ff2020);
}

.divider-line-right {
    flex: 1;
    height: 1px;
    background: linear-gradient(to left, transparent, #ff2020);
}

.divider-dot {
    width: 6px;
    height: 6px;
    background: #ff2020;
    border-radius: 50%;
    box-shadow: 0 0 8px #ff2020;
}

/* Chat messages */
.stChatMessage {
    background-color: #111111 !important;
    border-radius: 10px !important;
    margin-bottom: 8px !important;
    border: 1px solid #222222 !important;
}

/* Input */
.stChatInputContainer {
    border-radius: 12px !important;
}

/* Voice button */
.stButton > button {
    background: linear-gradient(135deg, #ff2020, #cc0000) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1em !important;
    letter-spacing: 2px !important;
    width: 100% !important;
    padding: 12px !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ff4444, #ff2020) !important;
    transform: scale(1.02) !important;
}

/* Live box */
.live-box {
    background-color: #111111;
    border-left: 3px solid #ff2020;
    border-radius: 6px;
    padding: 10px 15px;
    color: #888888;
    font-style: italic;
    margin-top: 8px;
    font-family: 'Rajdhani', sans-serif;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(#ff2020, #ff6600);
    border-radius: 2px;
}

/* Spinner color */
.stSpinner > div {
    border-top-color: #ff2020 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── LOGO ──────────────────────────────────────────────────────
st.markdown("""
<div class="yapex-logo">
    <span class="yapex-letters">
        <span class="yapex-y">Y</span><span class="yapex-a">A</span><span class="yapex-p">P</span><span class="yapex-e">E</span><span class="yapex-x">X</span>
    </span>
</div>
<div class="yapex-subtitle">Voice · Memory · Intelligence</div>
<div class="divider">
    <div class="divider-line"></div>
    <div class="divider-dot"></div>
    <div class="divider-dot" style="width:10px;height:10px;background:#ff6600;box-shadow:0 0 8px #ff6600;"></div>
    <div class="divider-dot"></div>
    <div class="divider-line-right"></div>
</div>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── CHAT HISTORY ──────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ─── INPUT AREA ────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])

with col2:
    if st.button("🎙️ Voice"):
        live_placeholder = st.empty()
        live_placeholder.markdown(
            '<div class="live-box">🎙️ Listening...</div>',
            unsafe_allow_html=True
        )
        user_input = transcribe_voice_realtime(live_placeholder)

        if user_input and "error" not in user_input.lower():
            live_placeholder.markdown(
                f'<div class="live-box">✅ You said: {user_input}</div>',
                unsafe_allow_html=True
            )
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                response = chat(user_input, st.session_state.session_id)
            st.session_state.messages.append(
                {"role": "assistant", "content": response})
            st.rerun()
        else:
            live_placeholder.markdown(
                f'<div class="live-box">❌ {user_input}</div>',
                unsafe_allow_html=True
            )

with col1:
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("Thinking..."):
            response = chat(prompt, st.session_state.session_id)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)