import streamlit as st
st.set_page_config(page_title="MASTER AI - LIVE V2", page_icon="🔥", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0B0B14 !important; }
    .glowing-title {
        font-size: 4rem; font-weight: 800; text-align: center; margin-top: 70px;
        background: linear-gradient(90deg, #00F5FF, #7F00FF, #FF006A, #FF8A00);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-size: 200% 200%; animation: move 3s ease infinite;
    }
    @keyframes move { 0%{background-position:0%} 100%{background-position:200%} }
    section[data-testid="stSidebar"] { background: #111119 !important; }

    /* V2 - CONIC RAINBOW MUTER 360 DERAJAT */
    [data-testid="stChatInput"] {
        position: relative;
        border-radius: 20px !important;
        padding: 2px !important;
        background: transparent !important;
        overflow: hidden !important;
    }
    [data-testid="stChatInput"]:before {
        content: "";
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background: conic-gradient(from 0deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000);
        animation: rotateRainbow 2s linear infinite;
        z-index: 0;
    }
    @keyframes rotateRainbow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    [data-testid="stChatInput"] > div {
        background: #1A1A2E !important;
        border-radius: 18px !important;
        position: relative; z-index: 1;
        margin: 2px;
    }
    [data-testid="stChatInput"] textarea { color: white !important; }
    [data-testid="stChatInput"] button {
        background: linear-gradient(90deg, #FF006A, #7F00FF) !important;
        color: white !important; border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown("### 🔥 MASTER AI v9.3 - V2 LIVE")
    nama = st.text_input("Nama lu siapa bang?", placeholder="Bintang")
    if st.button("➕ Obrolan Baru", type="primary", use_container_width=True):
        st.session_state.messages = []; st.rerun()

if not st.session_state.messages:
    st.markdown('<div class="glowing-title">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Tanya apa saja! 🌈 LIVE MUTER 360°"):
    st.session_state.messages.append({"role":"user","content":p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"): st.markdown(f"Oke bang {nama if nama else ''}, gue jawab dengan santai ya! Soal '{p}'")
    st.session_state.messages.append({"role":"assistant","content":f"Jawaban {p}"})
