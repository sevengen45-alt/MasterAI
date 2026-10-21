import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v10 - FULL COLOR", page_icon="🌈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

/* === FULL BACKGROUND AURORA PELANGI BERGERAK === */
.stApp {
    background: #000 !important;
    background-image: 
        radial-gradient(at 0% 0%, #FF0000 0%, transparent 50%),
        radial-gradient(at 50% 0%, #FF8A00 0%, transparent 50%),
        radial-gradient(at 100% 0%, #FFD600 0%, transparent 50%),
        radial-gradient(at 0% 50%, #00FF88 0%, transparent 50%),
        radial-gradient(at 50% 50%, #00F5FF 0%, transparent 50%),
        radial-gradient(at 100% 50%, #7B61FF 0%, transparent 50%),
        radial-gradient(at 0% 100%, #FF00E5 0%, transparent 50%),
        radial-gradient(at 100% 100%, #FF006A 0%, transparent 50%) !important;
    background-size: 200% 200% !important;
    animation: fullColorMove 8s ease infinite alternate !important;
}
@keyframes fullColorMove {
    0% { background-position: 0% 0%; filter: hue-rotate(0deg) brightness(1.2); }
    100% { background-position: 100% 100%; filter: hue-rotate(60deg) brightness(1.4); }
}

/* === TITLE FULL PELANGI SUPER NGEBUT === */
h1 {
    background: linear-gradient(90deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF, #FF00E5, #FF0000) !important;
    background-size: 200% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 900 !important; font-size: 5.5rem !important; text-align: center !important;
    animation: rainbowFast 1.5s linear infinite !important;
    filter: drop-shadow(0 0 30px #FF00E5) drop-shadow(0 0 60px #00F5FF) !important;
}
@keyframes rainbowFast { 0%{background-position:0%} 100%{background-position:200%} }
@media (max-width: 600px) { h1 {font-size: 3.2rem !important;} }

/* === SIDEBAR FULL PELANGI BORDER === */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0A1A 0%, #1A0A2A 25%, #0A1A2A 50%, #1A1A0A 75%, #0A0A1A 100%) !important;
    backdrop-filter: blur(25px) !important;
    border-right: 4px solid transparent !important;
    border-image: linear-gradient(180deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF, #FF00E5) 1 !important;
    animation: borderRainbow 3s linear infinite !important;
}
@keyframes borderRainbow { 0%{border-image: linear-gradient(180deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF, #FF00E5) 1} 100%{border-image: linear-gradient(360deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF, #FF00E5) 1} }

/* === CHAT BUBBLE USER = CYAN-PINK, BOT = PELANGI === */
div[data-testid="stChatMessage"]:has(span[aria-label="user"]) {
    background: linear-gradient(135deg, rgba(0,245,255,0.25), rgba(255,0,229,0.25)) !important;
    border: 2px solid #00F5FF !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.4) !important;
}
div[data-testid="stChatMessage"]:has(span[aria-label="assistant"]) {
    background: linear-gradient(135deg, rgba(255,215,0,0.15), rgba(123,97,255,0.25), rgba(255,0,106,0.15)) !important;
    border: 2px solid transparent !important;
    border-image: linear-gradient(90deg, #FFD600, #7B61FF, #FF006A) 1 !important;
    box-shadow: 0 0 25px rgba(123,97,255,0.5) !important;
}
.stChatMessage p { color: white !important; font-size: 17px !important; font-weight: 600 !important; text-shadow: 0 0 10px rgba(255,255,255,0.5); }

/* === BADGE FULL WARNA WARNI JALAN SENDIRI-SENDIRI === */
.badge {
    padding: 6px 14px; border-radius: 20px; color: white; font-weight: 900; font-size: 11px; margin: 3px; display: inline-block;
    background-size: 200% 100% !important; animation: rainbowFast 2s linear infinite !important;
    box-shadow: 0 0 15px currentColor !important;
}
.badge:nth-child(1) { background: linear-gradient(90deg, #FF0000, #FF8A00) !important; }
.badge:nth-child(2) { background: linear-gradient(90deg, #FFD600, #00FF88) !important; animation-delay: 0.3s !important; }
.badge:nth-child(3) { background: linear-gradient(90deg, #00F5FF, #7B61FF) !important; animation-delay: 0.6s !important; }
.badge:nth-child(4) { background: linear-gradient(90deg, #FF00E5, #FF006A) !important; animation-delay: 0.9s !important; }

/* === BUTTON SIDEBAR PELANGI === */
section[data-testid="stSidebar"] button {
    background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5) !important;
    background-size: 200% 100% !important;
    animation: rainbowFast 3s linear infinite !important;
    border: none !important; color: white !important; font-weight: 800 !important;
    border-radius: 15px !important; box-shadow: 0 0 20px rgba(123,97,255,0.6) !important;
}

/* === INPUT FULL PELANGI PALING MENCOLOK === */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0000, #FF7F00, #FFFF00, #00FF00, #00FFFF, #0000FF, #FF00FF, #FF0000) !important;
    background-size: 500% 100% !important;
    animation: rainbowFast 1s linear infinite !important;
    padding: 5px !important; border-radius: 30px !important;
    box-shadow: 0 0 40px #FF00E5, 0 0 80px #00F5FF, 0 0 120px #FFD600 !important;
}
[data-testid="stChatInput"] > div { background: #0A0A14 !important; border-radius: 25px !important; }
[data-testid="stChatInput"] textarea { color: white !important; font-weight: 700 !important; font-size: 16px !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #FF0000, #FFD600, #00FF88, #00F5FF, #FF00E5) !important;
    background-size: 300% 100% !important;
    animation: rainbowFast 1s linear infinite !important;
    border-radius: 50% !important; width: 40px !important; height: 40px !important;
}
</style>
""", unsafe_allow_html=True)

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
    st.markdown("### 🌈 MASTER AI v10 FULL")
    st.markdown('<span class="badge">FULL COLOR</span> <span class="badge">RGB</span> <span class="badge">JUAN</span> <span class="badge">LIVE</span>', unsafe_allow_html=True)
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Yo {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama lu siapa bang?", placeholder="Bintang")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()
    st.markdown("### 💬 Obrolan")
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1} ✨", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.divider()
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True):
        if st.button(f"{chat['title'][:28]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.title(active["title"])

with st.expander("💬 Daftar Obrolan (HP Tap Sini)", expanded=False):
    st.write(f"Ada {len(st.session_state.chats)} obrolan")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🔥" if m["role"]=="user" else "🌈"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'saja!'} 🌈 FULL COLOR"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🔥"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌈"):
        ph = st.empty()
        ph.markdown("▌ _lagi mikir full color..._ 🌈")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"Yo {nama}! {DEVELOPER_INFO} 🔥🌈 FULL COLOR EDITION!"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v10 Full Color. PEMBUAT KAMU {DEVELOPER_INFO}. Jangan jawab OpenAI. User: {nama}. Gaul Jaksel."
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
