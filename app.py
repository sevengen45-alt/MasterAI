import streamlit as st
from groq import Groq
import time

st.set_page_config(page_title="MasterAI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    h1 { 
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00F5FF, #A020F0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 3rem;
    }
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("API Key belum ada di Secrets")
    st.stop()

st.title("MasterAI 🇮🇩")
st.caption("Tanya apa aja!🦾‼️")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Tanya sesuatu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            completion = client.chat.completions.create(
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
              model="openai/gpt-oss-20b",
            )
            response = completion.choices[0].message.content
            placeholder = st.empty()
            full = ""
            for c in response:
                full += c
                placeholder.markdown(full + "▌")
                time.sleep(0.008)
            placeholder.markdown(full)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
