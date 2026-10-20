import streamlit as st
st.set_page_config(page_title="MASTER AI - V4 LASER", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0A0A12 !important; }
    .glowing-title {
        font-size: 4rem; font-weight: 800; text-align: center; margin-top: 70px;
        background: linear-gradient(90deg, #00F5FF, #7F00FF, #FF006A);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: hue 3s linear infinite;
    }
    @keyframes hue { 0%{filter:hue-rotate(0deg)} 100%{filter:hue-rotate(360deg)} }
    section[data-testid="stSidebar"] { background: #11111F !important; }

    /* V4 - LASER LIGHT YANG LARI KELILING */
    [data-testid="stChatInput"] {
        background: #1A1A2E !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        position: relative;
        overflow: hidden !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.1) !important;
    }
    /* Garis laser atas */
    [data-testid="stChatInput"]::before {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 50%; height: 2px;
        background: linear-gradient(90deg, transparent, #00F5FF, #7F00FF, #FF006A, transparent);
        animation: laserTop 2s linear infinite;
        z-index: 2;
    }
    /* Garis laser bawah */
    [data-testid="stChatInput"]::after {
        content: "";
        position: absolute;
        bottom: 0; right: -100%;
        width: 50%; height: 2px;
        background: linear-gradient(90deg, transparent, #FF8A00, #FFD600, #00FF88, transparent);
        animation: laserBottom 2s linear infinite;
        animation-delay: 1s;
        z-index: 2;
    }
    @keyframes laserTop {
        0% { left: -50%; }
        100% { left: 100%; }
    }
    @keyframes laserBottom {
        0% { right: -50%; }
        100% { right: 100%; }
    }
    /* Border luar ikut glow */
    [data-testid="stChatInput"] > div {
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stChatInput"] textarea { color: white !important; }
    [data-testid="stChatInput"] button {
        background: linear-gradient(90deg, #00F5FF, #FF006A) !important;
        animation: hue 2s linear infinite;
        border-radius: 10px !important; color: white !important;
    }
    /* Tambahan aura keliling */
    [data-testid="stChatInput"] {
        animation: borderGlow 2s ease-in-out infinite alternate;
    }
    @keyframes borderGlow {
        0% { box-shadow: 0 0 10px rgba(0,245,255,0.3), inset 0 0 10px rgba(0,245,255,0.1); border-color: rgba(0,245,255,0.5) !important; }
        100% { box-shadow: 0 0 20px rgba(255,0,106,0.5), inset 0 0 15px rgba(255,0,106,0.1); border-color: rgba(255,0,106,0.5) !important; }
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown("### ⚡ MasterAI")
    nama = st.text_input("Nama lu siapa bang?", placeholder="Bintang")
    if st.button("➕ Obrolan Baru", type="primary", use_container_width=True):
        st.session_state.messages = []; st.rerun()

if not st.session_state.messages:
    st.markdown('<div class="glowing-title">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666;'>Dibuat oleh Jonathan Kristian sergio Marut</p>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Tanya apa saja! ⚡ Laser"):
    st.session_state.messages.append({"role":"user","content":p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"): st.markdown(f"Oke bang {nama or ''}, gue jawab santai ya! '{p}'")
    st.session_state.messages.append({"role":"assistant","content":f"Jawab {p}"})
