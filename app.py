import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v9.6 - Colorful", page_icon="🇮🇩", layout="wide")

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
    animation: bgMove 10s ease infinite alternate !important;
}
@keyframes bgMove {
    0% { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(25deg); }
}

/* TITLE SUPER COLORFUL HIDUP */
h1 {
    background: linear-gradient(90deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF, #FF00E5, #FF0000) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 5rem !important;
    animation: rainbowTitle 3s linear infinite !important;
    filter: drop-shadow(0 0 25px rgba(255,0,229,0.6)) !important;
}
@keyframes rainbowTitle { 0%{background-position:0%} 100%{background-position:300%} }
@media (max-width: 600px) { h1 {font-size: 3rem !important;} }

/* SIDEBAR COLORFUL */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20,10,40,0.95), rgba(10,20,40,0.95)) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 2px solid !important;
    border-image: linear-gradient(180deg, #00F5FF, #7B61FF, #FF00E5) 1 !important;
}

/* CHAT BUBBLE JADI WARNA WARNI HIDUP */
.stChatMessage {
    background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(123,97,255,0.15)) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 24px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    position: relative;
    overflow: hidden;
}
.stChatMessage::before {
    content: "";
    position: absolute;
    top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    animation: shimmer 3s ease infinite;
}
@keyframes shimmer { 0%{left:-100%} 100%{left:200%} }

.stChatMessage p, .stChatMessage li { color: #FFFFFF !important; font-size: 16px !important; text-shadow: 0 0 10px rgba(255,255,255,0.3); }
.stChatMessage strong { color: #00F5FF !important; }
.stChatMessage h2 { color: #FFD600 !important; -webkit-text-fill-color: #FFD600 !important; }

/* BADGE PELANGI BERGERAK */
.badge {
    background: linear-gradient(90deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF) !important;
    background-size: 200% 100% !important;
    animation: rainbowTitle 2s linear infinite !important;
    padding: 5px 12px; border-radius: 20px; color: white;
    font-size: 11px; font-weight: 800; display: inline-block; margin: 3px;
    box-shadow: 0 0 15px rgba(123,97,255,0.6);
}

/* INPUT TANYA - SUPER RAINBOW LIVE PALING MENCOLOK */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000) !important;
    background-size: 400% 100% !important;
    animation: rainbowTitle 1.5s linear infinite !important;
    padding: 4px !important;
    border-radius: 25px !important;
    box-shadow: 0 0 30px rgba(255,0,229,0.6), 0 0 60px rgba(0,245,255,0.4) !important;
}
[data-testid="stChatInput"] > div {
    background: #0F0F1E !important;
    border-radius: 21px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
[data-testid="stChatInput"] textarea { color: white !important; font-weight: 600 !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #00F5FF, #FF00E5) !important;
    background-size: 200% 100% !important;
    animation: rainbowTitle 2s linear infinite !important;
    border-radius: 14px !important;
    color: white !important;
    font-weight: bold !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.6) !important;
}

/* FIX HP BIAR GAK KEPOTONG */
@media (max-width: 768px) {
    [data-testid="stSidebar"] { min-width: 280px !important; }
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Memulai Obrolan!", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI 🦾")
    st.markdown('<span class="badge">COLORFUL</span> <span class="badge">LIVE</span> <span class="badge">RGB</span> <span class="badge">GERAK</span>', unsafe_allow_html=True)
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

# Tombol khusus HP biar gak kepotong kayak kemarin
with st.expander("💬 Daftar Obrolan (Tap di HP)", expanded=False):
    st.write(f"Ada {len(st.session_state.chats)} obrolan")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "🌈"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'saja!'} 👨🏼‍💻✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌈"):
        ph = st.empty()
        ph.markdown("▌ _Thinking!⚡")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            system_prompt = f"Kamu MasterAI v9.6 Colorful. Nama user {nama}. Bahasa Indonesia gaul, super santai, colorful, jawab jelas dan bener. Kalau matematika jelasin step by step."
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
