import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v9.7 - LIVE", page_icon="🌈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

.stApp {
    background: #050510 !important;
    background-image: 
        radial-gradient(at 10% 10%, rgba(255,0,128,0.3) 0%, transparent 40%),
        radial-gradient(at 90% 20%, rgba(0,245,255,0.35) 0%, transparent 40%),
        radial-gradient(at 50% 90%, rgba(255,215,0,0.25) 0%, transparent 50%),
        radial-gradient(at 20% 80%, rgba(127,0,255,0.3) 0%, transparent 40%) !important;
}

/* ===== FIX 1: JUDUL LIVE PELANGI - PASTI JALAN ===== */
.live-rainbow-title {
    background: linear-gradient(90deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF, #FF00E5, #FF0000) !important;
    background-size: 400% 100% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 4.5rem !important;
    animation: rainbowLive 2s linear infinite !important;
    filter: drop-shadow(0 0 25px rgba(255,0,229,0.6)) !important;
    display: block !important;
    padding: 20px 0 !important;
}
@keyframes rainbowLive { 
    0% { background-position: 0% 50%; } 
    100% { background-position: 400% 50%; } 
}
@media (max-width: 600px) { .live-rainbow-title { font-size: 2.6rem !important; } }

/* Hapus style h1 bawaan biar gak bentrok */
h1 { visibility: hidden; height: 0; margin: 0; padding: 0; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20,10,40,0.95), rgba(10,20,40,0.95)) !important;
    backdrop-filter: blur(20px) !important;
}

.stChatMessage {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
.stChatMessage p { color: #FFFFFF !important; }

.badge {
    background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5) !important;
    background-size: 200% 100% !important;
    animation: rainbowLive 2s linear infinite !important;
    padding: 5px 12px; border-radius: 20px; color: white; font-weight: 800; font-size: 11px; margin: 2px; display: inline-block;
}

/* ===== FIX 2: TASKBAR LIVE PELANGI - PASTI NYALA MENYALA ===== */
div[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0000, #FF7F00, #FFFF00, #00FF00, #00FFFF, #0000FF, #FF00FF, #FF0000) !important;
    background-size: 500% 100% !important;
    animation: rainbowLive 1.2s linear infinite !important;
    padding: 4px !important;
    border-radius: 30px !important;
    box-shadow: 0 0 30px #FF00E5, 0 0 60px #00F5FF !important;
}
div[data-testid="stChatInput"] > div {
    background: #0F0F1E !important;
    border-radius: 26px !important;
}
div[data-testid="stChatInput"] textarea {
    color: white !important;
    font-weight: 600 !important;
}
div[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #FF0000, #00F5FF, #FF00E5) !important;
    background-size: 300% 100% !important;
    animation: rainbowLive 1s linear infinite !important;
    border-radius: 50% !important;
}
</style>
""", unsafe_allow_html=True)

# OTAK TETAP PUNYA JUAN
DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Memulai Obrolan!", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### 🌈 MasterAI v9.7 LIVE")
    st.markdown('<span class="badge">JUAN</span> <span class="badge">LIVE</span>', unsafe_allow_html=True)
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Yo {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama lu siapa bang?", placeholder="Bintang")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()

active = get_active()

# INI KUNCINYA - JUDUL PAKE MARKDOWN BIAR LIVE!
st.markdown(f"<h1 class='live-rainbow-title'>{active['title']}</h1>", unsafe_allow_html=True)

with st.expander("💬 Daftar Obrolan (HP Tap Sini)", expanded=False):
    st.write(f"Ada {len(st.session_state.chats)} obrolan")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "🌈"):
        st.markdown(m["content"])

if prompt := st.chat_input("Tanya apa saja! 👨🏼‍💻✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌈"):
        ph = st.empty()
        ph.markdown("▌ _lagi mikir..._ 🌈")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"Yo {nama}! {DEVELOPER_INFO} 🔥"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v9.7. PEMBUAT KAMU ADALAH {DEVELOPER_INFO}. User: {nama}. Gaul Jaksel."
                messages = [{"role": "system", "content": system_prompt}] + active["messages"]
                res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.85, max_tokens=1500)
                ans = res.choices[0].message.content
                full = ""
                for w in ans.split(" "):
                    full += w + " "
                    ph.markdown(full + "▌")
                    time.sleep(0.02)
                ph.markdown(full)
                active["messages"].append({"role": "assistant", "content": full})
        except Exception as e:
            ph.error(f"Error: {e}")
