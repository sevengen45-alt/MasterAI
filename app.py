import streamlit as st
from groq import Groq
import uuid
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="MasterAI v11.3 - Ultimate Edition", page_icon="⚡", layout="wide")

# ===== CONFIG DEVELOPER - INI YANG BIKIN GAK BISA DIBAJAK =====
DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@500;700&display=swap');
* { font-family: 'Google Sans', Inter, sans-serif !important; }
.stApp { background: #FFFFFF !important; }
.stApp::before {
    content: ""; position: fixed; inset: -40%;
    background: 
        radial-gradient(ellipse 700px 600px at 15% 10%, rgba(66,133,244,0.14) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 85% 15%, rgba(219,68,55,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 800px 600px at 50% 115%, rgba(15,157,88,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 20% 90%, rgba(244,180,0,0.13) 0%, transparent 60%);
    animation: orbAlive 16s ease-in-out infinite alternate; filter: blur(18px); z-index: 0; pointer-events: none;
}
@keyframes orbAlive { 0%{transform: translate(0,0) scale(1)} 50%{transform: translate(-3%,3%) scale(1.08)} 100%{transform: translate(3%,-2%) scale(1.02)} }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; background: transparent !important; }
p, div, span { color: #202124 !important; }
h1 { text-align: center !important; font-weight: 500 !important; font-size: 3.4rem !important; line-height: 1.05 !important; color: #202124 !important; -webkit-text-fill-color: #202124 !important; }
h1 .rainbow-alive {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 300% 100% !important; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; animation: rainbowRun 2.5s linear infinite, floatAlive 3s ease-in-out infinite alternate !important;
    font-weight: 700 !important; display: inline-block;
}
@keyframes rainbowRun { 0%{background-position:0%} 100%{background-position:300%} }
@keyframes floatAlive { 0%{transform: translateY(0)} 100%{transform: translateY(-6px)} }
.gemini-line { width: 120px; height: 4px; margin: 18px auto 0 auto; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4); background-size: 300% 100%; animation: rainbowRun 2s linear infinite; border-radius: 100px; }
section[data-testid="stSidebar"] { background: #F8F9FA !important; border-right: 1px solid #E8EAED !important; }
section[data-testid="stSidebar"] * { color: #202124 !important; }
.badge-alive { background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important; background-size: 300% 100% !important; animation: rainbowRun 2s linear infinite !important; color: white !important; padding: 6px 14px; border-radius: 100px; font-size: 11px; font-weight: 700; display: inline-block; margin: 3px; }
.stChatMessage { background: #FFFFFF !important; border: 1px solid #E8EAED !important; border-radius: 22px !important; box-shadow: 0 1px 8px rgba(0,0,0,0.04) !important; max-width: 720px !important; margin: 14px auto !important; position: relative; overflow: hidden; animation: popAlive 0.5s cubic-bezier(0.16,1,0.3,1) !important; }
@keyframes popAlive { 0%{opacity:0; transform: translateY(10px) scale(0.98)} 100%{opacity:1; transform: translateY(0) scale(1)} }
.stChatMessage::after { content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4); background-size: 300% 100%; animation: rainbowRun 2s linear infinite; opacity: 0; transition: opacity 0.3s; }
.stChatMessage:hover::after { opacity: 1; }
.stChatMessage p { color: #202124 !important; font-size: 15.5px !important; line-height: 1.65 !important; }
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 400% 100% !important; animation: rainbowRun 2s linear infinite, inputAlive 2.5s ease-in-out infinite !important;
    padding: 2.5px !important; border-radius: 30px !important; box-shadow: 0 2px 16px rgba(66,133,244,0.18) !important; max-width: 740px !important; margin: 0 auto !important;
}
@keyframes inputAlive { 0%,100%{box-shadow: 0 2px 16px rgba(66,133,244,0.18); transform: scale(1)} 50%{box-shadow: 0 6px 28px rgba(66,133,244,0.28); transform: scale(1.01)} }
[data-testid="stChatInput"] > div { background: #FFFFFF !important; border-radius: 28px !important; border: none !important; }
[data-testid="stChatInput"] textarea { color: #202124 !important; -webkit-text-fill-color: #202124 !important; font-size: 16px !important; }
[data-testid="stChatInput"] button { background: linear-gradient(90deg, #4285F4, #9C27B0) !important; background-size: 200% 100% !important; animation: rainbowRun 2s linear infinite !important; border-radius: 50% !important; width: 36px !important; height: 36px !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# Inisialisasi API Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ===== INVENTARIS SOUND PLAYER (GEMINI FEATURE) =====
# Menyimpan teks terakhir yang perlu dibacakan oleh fitur Voice Chat
if "last_speech_text" not in st.session_state:
    st.session_state.last_speech_text = ""

# ===== SAVE MEMORY =====
if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Ngobrol?", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI 🇮🇩")
    st.markdown('<span class="badge-alive">GEMINI VOICE</span> <span class="badge-alive">CHATGPT STORY</span>', unsafe_allow_html=True)
    st.divider()
    
    # SAVE NAMA USER DI SINI!
    if st.session_state.user_memory["nama"]:
        st.success(f"Yo {st.session_state.user_memory['nama']}! 😎🔥")
        st.caption(f"Developer: Juan Maumere")
    else:
        nama = st.text_input("Eh nama lu siapa?", placeholder="Panggil aja...")
        if nama:
            st.session_state.user_memory["nama"] = nama
            st.rerun()
            
    st.divider()
    st.markdown("### ⚙️ Mode Kekuatan AI")
    # FITUR 1: ChatGPT Mode (Membuat cerita dengan kreativitas maksimal)
    mode_cerita = st.toggle("✍️ Mode ChatGPT (Storyteller Pro)", value=False, help="Aktifkan ini kalau mau minta dibuatin cerita super kreatif & ga bosenin!")
    # FITUR 2: Gemini Mode (Live Voice/Text-to-Speech)
    mode_suara = st.toggle("🔊 Mode Gemini (Live Voice Chat)", value=False, help="Aktifkan ini agar AI langsung berbicara setelah menjawab!")
    
    st.divider()
    st.markdown("### 💬 Obrolan lu")
    if st.button("➕ Obrolan baru", use_container_width=True):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Ngobrol {len(st.session_state.chats)+1} ✨", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
        
    st.divider()
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True):
        if st.button(f"{chat['title'][:28]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()

if len(active["messages"]) == 0:
    st.markdown(f"""
    <div style="text-align:center; padding: 50px 20px 10px 20px; max-width:720px; margin:0 auto;">
        <h1>Yo {st.session_state.user_memory['nama'] or 'Bang'}, Mau<br><span class="rainbow-alive">Ngobrolin Apa?</span></h1>
        <div class="gemini-line"></div>
        <p style="color:#5F6368 !important; font-size:16px; margin-top:20px;">Gas tanya apa pun, aku siap bantu kok! 😎✨</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='text-align:center; color:#202124;'>{active['title']}</h2>", unsafe_allow_html=True)

# Tampilkan riwayat chat
for m in active["messages"]:
    with st.chat_message(m["role"], avatar="😎" if m["role"]=="user" else "🌈"):
        st.markdown(m["content"])

# Pemrosesan Chat Input
if prompt := st.chat_input(f"Mau tanya? Silahkan! {st.session_state.user_memory['nama'] or ''}."):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="😎"): 
        st.markdown(prompt)
        
    with st.chat_message("assistant", avatar="🌈"):
        ph = st.empty()
        ph.markdown("Thinking! 🦾")
        try:
            # ===== ANTI BAJAK - DETEKSI PERTANYAAN SIAPA PEMBUAT =====
            lower_prompt = prompt.lower()
            is_ask_developer = any(k in lower_prompt for k in [
                "siapa yang membuat", "siapa pembuat", "siapa yg membuat", "siapa yg buat",
                "who made you", "who created you", "dibuat siapa", "buatan siapa",
                "siapa developer", "siapa yang bikin", "kamu dibuat siapa",
                "kamu buatan siapa", "siapa pencipta"
            ])
            
            if is_ask_developer:
                ans = DEVELOPER_INFO + f" Btw, lu kah {st.session_state.user_memory['nama'] or 'bang?'}😎"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
                if mode_suara:
