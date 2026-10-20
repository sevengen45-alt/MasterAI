import streamlit as st

st.set_page_config(page_title="MASTER AI - LIVE RAINBOW", page_icon="🌈", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: #0B0B14 !important;
        background-image: 
            radial-gradient(at 30% 20%, rgba(0, 245, 255, 0.15) 0px, transparent 50%),
            radial-gradient(at 80% 0%, rgba(127, 0, 255, 0.25) 0px, transparent 50%),
            radial-gradient(at 100% 80%, rgba(255, 0, 106, 0.15) 0px, transparent 50%) !important;
    }
    .glowing-title {
        font-size: 4rem; font-weight: 800; text-align: center; margin-top: 80px;
        background: linear-gradient(90deg, #FFFFFF, #00F5FF, #7F00FF, #FF006A, #FF8A00);
        background-size: 300% 300%;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease infinite, neonGlow 1.5s ease-in-out infinite alternate;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; }
    }
    @keyframes neonGlow {
        0% { filter: drop-shadow(0 0 20px #00F5FF); } 100% { filter: drop-shadow(0 0 30px #FF006A); }
    }
    section[data-testid="stSidebar"] {
        background: rgba(17, 17, 25, 0.85) !important; backdrop-filter: blur(20px);
    }

    /* === LIVE RAINBOW TABLE - GERAK TERUS!!! === */
    div[data-testid="stChatInput"] {
        position: relative !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        overflow: visible !important;
    }
    /* Border pelangi yang gerak */
    div[data-testid="stChatInput"]::before {
        content: "" !important;
        position: absolute !important;
        top: -3px !important; left: -3px !important; right: -3px !important; bottom: -3px !important;
        background: linear-gradient(90deg, 
            #ff0000, #ff8000, #ffff00, #00ff00, #00ffff, #0000ff, #8000ff, #ff0080, #ff0000) !important;
        background-size: 200% 100% !important;
        border-radius: 20px !important;
        animation: rainbowRun 2s linear infinite !important;
        z-index: -1 !important;
        filter: blur(0.5px);
        box-shadow: 0 0 20px rgba(255,0,128,0.5), 0 0 40px rgba(0,255,255,0.3) !important;
    }
    @keyframes rainbowRun {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    div[data-testid="stChatInput"] > div {
        background: #1A1A2E !important;
        border-radius: 16px !important;
        border: none !important;
        position: relative !important;
        z-index: 1 !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: white !important;
    }
    /* Tombol kirim ikut rainbow */
    div[data-testid="stChatInput"] button {
        background: linear-gradient(90deg, #FF006A, #7F00FF, #00F5FF) !important;
        background-size: 200% 100% !important;
        animation: rainbowRun 2s linear infinite !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        box-shadow: 0 0 15px rgba(127,0,255,0.6) !important;
    }
    /* Placeholder text juga glowing dikit */
    div[data-testid="stChatInput"] textarea::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("### 🔥 MASTER AI v9.3 LIVE")
    c1, c2 = st.columns(2)
    with c1: st.button("PUTIH TERANG", use_container_width=True)
    with c2: st.button("ANTI GELAP", use_container_width=True)
    st.divider()
    st.markdown("**Nama lu siapa bang?**")
    nama = st.text_input("", placeholder="Bintang", label_visibility="collapsed")
    st.markdown("**💬 Obrolan**")
    if st.button("➕ Obrolan Baru", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if not st.session_state.messages:
    st.markdown('<div class="glowing-title">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.7);'>Tanya apa aja, gue jawab dengan santai ya!</p>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def get_answer(prompt, nama_user):
    sapaan = f"bang {nama_user}" if nama_user else "bang"
    return f"Oke {sapaan}, gue jawab dengan santai ya! Soal '{prompt}' itu menarik nih!"

if prompt := st.chat_input("Tanya apa saja! 🌈"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        jawaban = get_answer(prompt, nama)
        st.markdown(jawaban)
    st.session_state.messages.append({"role": "assistant", "content": jawaban})
