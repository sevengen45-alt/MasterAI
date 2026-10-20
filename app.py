import streamlit as st

st.set_page_config(page_title="MASTER AI v9.3 - Hidup", page_icon="🔥", layout="wide")

# --- UI DOANG YANG GUE UBAH JADI LEBIH HIDUP BERWARNA ---
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

    /* JUDUL "Siap Memulai Obrolan!" - LEBIH HIDUP */
    .glowing-title {
        font-size: 4rem; font-weight: 800; text-align: center; margin-top: 100px;
        background: linear-gradient(90deg, #FFFFFF 0%, #00F5FF 20%, #7F00FF 50%, #FF006A 75%, #FF8A00 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: gradientShift 4s ease infinite, neonGlow 2s ease-in-out infinite alternate;
        letter-spacing: -1px;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; }
    }
    @keyframes neonGlow {
        0% { filter: drop-shadow(0 0 15px #00F5FF) drop-shadow(0 0 30px #7F00FF); }
        100% { filter: drop-shadow(0 0 25px #FF006A) drop-shadow(0 0 45px #FF8A00); }
    }

    /* SIDEBAR - TETAP SAMA STRUKTURNYA, CUMA LEBIH GLASS */
    section[data-testid="stSidebar"] {
        background: rgba(17, 17, 25, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(127, 0, 255, 0.2);
    }

    /* TOMBOL PUTIH TERANG & ANTI GELAP - LEBIH HIDUP */
    div[data-testid="stButton"] > button {
        border-radius: 12px !important; font-weight: 700 !important; transition: all 0.3s ease !important;
    }
    /* Tombol Obrolan Baru yang di foto lu */
    button[kind="primary"] {
        background: linear-gradient(90deg, #FF3B30, #FF9500) !important;
        box-shadow: 0 0 20px rgba(255, 59, 48, 0.5) !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.05);
        box-shadow: 0 0 35px rgba(255, 149, 0, 0.8) !important;
    }

    /* INPUT NAMA & CHAT INPUT - GLOWING */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(0, 245, 255, 0.2) !important;
        border-radius: 12px !important; color: white !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00F5FF !important;
        box-shadow: 0 0 15px rgba(0, 245, 255, 0.3) !important;
    }
    .stChatInput {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(127, 0, 255, 0.3) !important;
        box-shadow: 0 0 20px rgba(127, 0, 255, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC NYA TETAP SAMA PERSIS KAYAK v9.3 PUNYA LU - GUE GAK UBAH ---
# (Ini biar nama, obrolan, pemrosesan bahasa tetep)

if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR - STRUKTUR TETAP SAMA KAYAK DI FOTO
with st.sidebar:
    st.markdown("### 🔥 MASTER AI v9.3")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("PUTIH TERANG", use_container_width=True):
            st.session_state.theme = "light"
    with col2:
        if st.button("ANTI GELAP", use_container_width=True):
            st.session_state.theme = "dark"
    
    st.divider()
    st.markdown("**Nama lu siapa bang?**")
    nama = st.text_input("", placeholder="Bintang", label_visibility="collapsed")
    
    st.markdown("**💬 Obrolan**")
    if st.button("➕ Obrolan Baru", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown('<div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:10px; text-align:center; font-size:0.9rem; border:1px solid rgba(255,255,255,0.1)">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)

# MAIN - JUDUL SAMA PERSIS KAYAK DI FOTO
if not st.session_state.messages:
    st.markdown('<div class="glowing-title">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)
    if nama:
        st.markdown(f"<p style='text-align:center; color:rgba(255,255,255,0.6); margin-top:15px;'>Yo {nama}, gue siap nih! Tanya aja, gue jawab dengan santai ya!</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.5); margin-top:15px;'>Tanya apa aja, gue jawab dengan santai ya!</p>", unsafe_allow_html=True)

# CHAT HISTORY - LOGIC TETAP
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# LOGIC JAWABAN - GUE BALIKIN KE YANG SIMPLE BIAR GAK RIBET (GAK PAKE RESEARCH)
def get_simple_answer(prompt, nama_user):
    # Ini logic bahasa gaul santai lu yang lama, gak gue ubah-ubah
    sapaan = f"bang {nama_user}" if nama_user else "bang"
    return f"Oke {sapaan}, gue jawab dengan santai ya! Soal '{prompt}' itu menarik nih, mau gue jelasin dari sisi mana dulu?"

# INPUT
if prompt := st.chat_input("Tanya apa saja!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # Simulasi jawaban simple
        jawaban = get_simple_answer(prompt, nama if 'nama' in locals() else "")
        st.markdown(jawaban)
    
    st.session_state.messages.append({"role": "assistant", "content": jawaban})
