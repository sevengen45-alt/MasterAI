import streamlit as st
import time
import random

# --- CONFIG ---
st.set_page_config(
    page_title="MASTER AI - Obrolan Hidup",
    page_icon="🔥",
    layout="wide"
)

# --- CSS GLOWING HIDUP ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #1a1a40 0%, #000000 50%, #0f0c29 100%);
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Glowing Title */
    .glowing-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #00F5FF, #7F00FF, #FF006A, #FF8A00);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 5s ease infinite, glowPulse 2s ease-in-out infinite;
        margin-top: 80px;
        text-shadow: 0 0 30px rgba(127, 0, 255, 0.5);
    }
    
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes glowPulse {
        0%, 100% { filter: drop-shadow(0 0 20px #7F00FF); }
        50% { filter: drop-shadow(0 0 40px #00F5FF); }
    }
    
    /* Glass Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(20, 20, 35, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(127, 0, 255, 0.3);
    }
    
    /* Chat Bubble */
    .stChatMessage {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    /* Button Obrolan Baru - Glowing Red Orange */
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #FF3B30, #FF9500) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        box-shadow: 0 0 20px rgba(255, 59, 48, 0.5) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    div[data-testid="stButton"] > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 30px rgba(255, 149, 0, 0.8) !important;
    }
    
    /* Input chat glowing */
    .stChatInput {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(0, 245, 255, 0.3) !important;
        box-shadow: 0 0 15px rgba(0, 245, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chats" not in st.session_state:
    st.session_state.chats = ["Siap Memulai Obrolan!"]

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔥 MASTER AI v9.3")
    st.markdown('<span style="color:#00F5FF; font-size:0.8rem;">● ONLINE • VERSI HIDUP</span>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown("**Nama lu siapa bang?**")
    nama = st.text_input("", placeholder="Contoh: Bintang", label_visibility="collapsed")
    if nama:
        st.success(f"Siap bang {nama}!")
    
    st.markdown("**💬 Obrolan**")
    if st.button("🔥 Obrolan Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("**Riwayat**")
    for chat in st.session_state.chats:
        st.markdown(f'<div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:8px; font-size:0.9rem;">💭 {chat}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.caption("Dibuat dengan santai oleh Juang 🔥")

# --- MAIN CONTENT ---
if not st.session_state.messages:
    st.markdown('<div class="glowing-title">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:rgba(255,255,255,0.6); margin-top:20px; font-size:1.2rem;">Yo {nama if nama else "bang"}, tanya apa aja, gue jawab dengan santai ya! 👌</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div style="background:rgba(0,245,255,0.1); padding:20px; border-radius:15px; text-align:center; border:1px solid rgba(0,245,255,0.2)">🤖<br><b>Tanya Coding</b><br><span style="font-size:0.8rem; opacity:0.7">Error streamlit? sini gue bantu</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background:rgba(127,0,255,0.1); padding:20px; border-radius:15px; text-align:center; border:1px solid rgba(127,0,255,0.2)">🔥<br><b>Curhat Santai</b><br><span style="font-size:0.8rem; opacity:0.7">Gabut? ngobrol aja</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="background:rgba(255,0,106,0.1); padding:20px; border-radius:15px; text-align:center; border:1px solid rgba(255,0,106,0.2)">💡<br><b>Bikin Ide</b><br><span style="font-size:0.8rem; opacity:0.7">Butuh ide konten? gas</span></div>', unsafe_allow_html=True)

# Tampilkan chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- LOGIKA JAWABAN (BAHASA GAUL SANTAI) ---
def get_santai_response(prompt, nama_user):
    prompt_low = prompt.lower()
    
    # Aturan bahasa: santai, gaul, TAPI jangan bilang "aku akan jawab pake bahasa jaksel"
    sapaan = f"Oke bang {nama_user}, " if nama_user else "Oke bang, "
    
    if "halo" in prompt_low or "hai" in prompt_low:
        return f"{sapaan}halo juga! Gue udah siap nih, mau dibahas apa? Tanya aja, gue jawab dengan santai ya!"
    elif "error" in prompt_low or "streamlit" in prompt_low:
        return f"{sapaan}wah error lagi ya? Coba spill errornya apa, screenshot juga boleh. Gue bantu beresin sampe jalan, gue jawab dengan santai ya biar gak pusing!"
    elif "ui.py" in prompt_low or "app.py" in prompt_low:
        return f"{sapaan}nah itu dia! Jadi ui.py sama app.py itu beda file tapi fungsinya sama. Kalo di hosting lu settingnya ui.py, ya editnya di ui.py. Simple kan? Gue jelasin dengan santai ya!"
    else:
        responses = [
            f"{sapaan}menarik nih pertanyaannya. Jadi gini, {prompt} itu sebenernya bisa kita breakdown pelan-pelan. Menurut gue, kuncinya ada di cara kita approachnya. Mau gue jelasin lebih detail? Gue jawab dengan santai ya!",
            f"{sapaan}paham gue maksud lu. Kalo soal {prompt}, jujur ini agak tricky tapi seru buat dibahas. Gue punya beberapa ide, mau coba versi yang mana dulu?",
            f"Yo {nama_user if nama_user else 'bang'}! Gas, kalo {prompt} itu gue udah ada bayangan. Kita bikin versi yang lebih hidup dan bercahaya kayak yang lu mau. Ada ide tambahan lagi gak?",
        ]
        return random.choice(responses)

# --- INPUT CHAT ---
if prompt := st.chat_input("Tanya apa saja!"):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI Response
    with st.chat_message("assistant"):
        with st.spinner("Lagi mikir..."):
            time.sleep(0.8)
            response = get_santai_response(prompt, nama)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
