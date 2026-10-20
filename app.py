import streamlit as st

st.set_page_config(page_title="MASTER AI v9.3 - Rainbow", page_icon="🌈", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;800&display=swap');
    .stApp {
        background: #0B0B14 !important;
        background-image: 
            radial-gradient(at 30% 20%, rgba(0, 245, 255, 0.15) 0px, transparent 50%),
            radial-gradient(at 80% 0%, rgba(127, 0, 255, 0.25) 0px, transparent 50%),
            radial-gradient(at 100% 80%, rgba(255, 0, 106, 0.15) 0px, transparent 50%) !important;
        font-family: 'Space Grotesk', sans-serif;
    }
    .glowing-title {
        font-size: 4rem; font-weight: 800; text-align: center; margin-top: 80px;
        background: linear-gradient(90deg, #FFFFFF 0%, #00F5FF 20%, #7F00FF 50%, #FF006A 75%, #FF8A00 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: gradientShift 4s ease infinite, neonGlow 2s ease-in-out infinite alternate;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; }
    }
    @keyframes neonGlow {
        0% { filter: drop-shadow(0 0 15px #00F5FF) drop-shadow(0 0 30px #7F00FF); }
        100% { filter: drop-shadow(0 0 25px #FF006A) drop-shadow(0 0 45px #FF8A00); }
    }
    section[data-testid="stSidebar"] {
        background: rgba(17, 17, 25, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(127, 0, 255, 0.2);
    }

    /* === YANG BARU: TABEL TANYA JADI RAINBOW PELANGI === */
    [data-testid="stChatInput"] {
        background: transparent !important;
        padding: 3px !important;
        border-radius: 18px !important;
        background: linear-gradient(90deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7F00FF, #FF006A) !important;
        background-size: 400% 400% !important;
        animation: rainbowMove 3s linear infinite !important;
        box-shadow: 0 0 25px rgba(127, 0, 255, 0.4) !important;
    }
    @keyframes rainbowMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    [data-testid="stChatInput"] > div {
        background: #1A1A2E !important;
        border-radius: 15px !important;
        border: none !important;
    }
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: white !important;
    }
    [data-testid="stChatInput"] button {
        background: linear-gradient(90deg, #00F5FF, #7F00FF) !important;
        border-radius: 10px !important;
        color: white !important;
        border: none !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 12px !important; color: white !important;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("### 🔥 MASTER AI v9.3")
    col1, col2 = st.columns(2)
    with col1:
        st.button("PUTIH TERANG", use_container_width=True)
    with col2:
        st.button("ANTI GELAP", use_container_width=True)
    st.divider()
    st.markdown("**Nama lu siapa bang?**")
    nama = st.text_input("", placeholder="Bintang", label_visibility="collapsed")
    st.markdown("**💬 Obrolan**")
    if st.button("➕ Obrolan Baru", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown('<div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:10px; text-align:center;">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown('<div class="glowing-title">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:rgba(255,255,255,0.7); margin-top:15px;'>Tanya apa aja, gue jawab dengan santai ya!</p>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def get_simple_answer(prompt, nama_user):
    sapaan = f"bang {nama_user}" if nama_user else "bang"
    return f"Oke {sapaan}, gue jawab dengan santai ya! Soal '{prompt}' itu menarik nih, mau gue jelasin dari sisi mana dulu?"

if prompt := st.chat_input("Tanya apa saja!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        jawaban = get_simple_answer(prompt, nama)
        st.markdown(jawaban)
    st.session_state.messages.append({"role": "assistant", "content": jawaban})
