import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v9.7 - Alive Premium", page_icon="🇮🇩", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}
p, li, div { font-family: 'Inter', sans-serif !important; }

/* BACKGROUND HIDUP - MESH GRADIENT GERAK HALUS */
.stApp {
    background: #050510 !important;
    overflow: hidden;
}
.stApp::before {
    content: ""; position: fixed; inset: -50%;
    background: 
        radial-gradient(at 15% 15%, rgba(255,0,128,0.45) 0%, transparent 40%),
        radial-gradient(at 85% 10%, rgba(0,245,255,0.45) 0%, transparent 45%),
        radial-gradient(at 50% 85%, rgba(255,215,0,0.35) 0%, transparent 50%),
        radial-gradient(at 25% 75%, rgba(127,0,255,0.5) 0%, transparent 45%);
    animation: meshFloat 18s ease-in-out infinite alternate;
    filter: blur(20px); z-index: 0; pointer-events: none;
}
@keyframes meshFloat {
    0% { transform: translate(0%, 0%) scale(1) rotate(0deg); }
    50% { transform: translate(-5%, 5%) scale(1.1) rotate(2deg); }
    100% { transform: translate(5%, -3%) scale(1.05) rotate(-1deg); }
}
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; }

/* TITLE - PELANGI HIDUP + GLOW PULSE */
h1 {
    background: linear-gradient(90deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF, #FF00E5, #FF0000) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 4.8rem !important;
    animation: rainbowTitle 4s linear infinite, titleFloat 3.5s ease-in-out infinite alternate !important;
    filter: drop-shadow(0 0 20px rgba(255,0,229,0.5)) drop-shadow(0 0 40px rgba(0,245,255,0.3)) !important;
    letter-spacing: -0.04em !important;
    position: relative; z-index: 2;
}
@keyframes rainbowTitle { 0%{background-position:0%} 100%{background-position:300%} }
@keyframes titleFloat { 0%{transform: translateY(0px)} 100%{transform: translateY(-6px)} }
@media (max-width: 600px) { h1 {font-size: 2.8rem !important;} }

/* SIDEBAR - GLASS HIDUP + BORDER PELANGI GERAK */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,10,35,0.9), rgba(10,15,35,0.92)) !important;
    backdrop-filter: blur(24px) saturate(1.4) !important;
    border-right: 2px solid transparent !important;
    border-image: linear-gradient(180deg, #00F5FF, #7B61FF, #FF00E5, #FFD600) 1 !important;
    box-shadow: 10px 0 40px rgba(0,0,0,0.5) !important;
    position: relative; z-index: 2;
}
section[data-testid="stSidebar"]::after {
    content: ""; position: absolute; top: 0; right: 0; width: 2px; height: 100%;
    background: linear-gradient(180deg, #00F5FF, #7B61FF, #FF00E5, #FFD600, #00F5FF);
    background-size: 100% 300%; animation: borderFlow 4s linear infinite;
}
@keyframes borderFlow { 0%{background-position:0% 0%} 100%{background-position:0% 300%} }

/* CHAT BUBBLE - GLASS HIDUP + SHIMMER + HOVER GLOW */
.stChatMessage {
    background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(123,97,255,0.18)) !important;
    backdrop-filter: blur(22px) saturate(1.3) !important;
    border-radius: 24px !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    transition: all 0.4s ease !important;
    animation: bubbleIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
@keyframes bubbleIn { 0%{opacity:0; transform: translateY(12px) scale(0.98)} 100%{opacity:1; transform: translateY(0) scale(1)} }
.stChatMessage:hover {
    transform: translateY(-2px) !important;
    border-color: rgba(0,245,255,0.3) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35), 0 0 20px rgba(123,97,255,0.25) !important;
}
.stChatMessage::before {
    content: ""; position: absolute; top: 0; left: -120%; width: 70%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
    animation: shimmer 4.5s ease-in-out infinite; transform: skewX(-15deg);
}
@keyframes shimmer { 0%{left:-120%} 50%{left:120%} 100%{left:120%} }
.stChatMessage p, .stChatMessage li { color: #FFFFFF !important; font-size: 15.5px !important; line-height: 1.65 !important; text-shadow: 0 1px 8px rgba(0,0,0,0.4); }
.stChatMessage strong { color: #00F5FF !important; text-shadow: 0 0 12px rgba(0,245,255,0.6) !important; }
.stChatMessage h2 { color: #FFD600 !important; -webkit-text-fill-color: #FFD600 !important; }

/* BADGE - PELANGI + FLOAT + GLOW */
.badge {
    background: linear-gradient(90deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF) !important;
    background-size: 200% 100% !important;
    animation: rainbowTitle 2.5s linear infinite, badgeFloat 2.8s ease-in-out infinite alternate !important;
    padding: 6px 14px; border-radius: 20px; color: white;
    font-size: 11px; font-weight: 800; display: inline-block; margin: 3px;
    box-shadow: 0 4px 15px rgba(123,97,255,0.5), 0 0 10px rgba(255,255,255,0.2);
    letter-spacing: 0.05em;
}
@keyframes badgeFloat { 0%{transform: translateY(0)} 100%{transform: translateY(-3px)} }

/* INPUT - SUPER RAINBOW LIVE + PULSE GLOW - JADI PUSAT PERHATIAN */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000) !important;
    background-size: 400% 100% !important;
    animation: rainbowTitle 1.8s linear infinite, inputPulse 2.5s ease-in-out infinite !important;
    padding: 3.5px !important;
    border-radius: 28px !important;
    box-shadow: 0 0 25px rgba(255,0,229,0.55), 0 0 50px rgba(0,245,255,0.35), 0 8px 32px rgba(0,0,0,0.4) !important;
    max-width: 760px !important; margin: 0 auto !important;
}
@keyframes inputPulse { 0%,100%{box-shadow: 0 0 25px rgba(255,0,229,0.55), 0 0 50px rgba(0,245,255,0.35)} 50%{box-shadow: 0 0 35px rgba(255,0,229,0.75), 0 0 70px rgba(0,245,255,0.5)} }
[data-testid="stChatInput"] > div {
    background: rgba(15,15,30,0.95) !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 25px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stChatInput"] textarea { 
    color: white !important; font-weight: 600 !important; font-size: 16px !important;
    -webkit-text-fill-color: white !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(255,255,255,0.6) !important; -webkit-text-fill-color: rgba(255,255,255,0.6) !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5) !important;
    background-size: 200% 100% !important;
    animation: rainbowTitle 2s linear infinite !important;
    border-radius: 16px !important; color: white !important; font-weight: 800 !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.7), inset 0 1px 0 rgba(255,255,255,0.3) !important;
    transition: transform 0.2s ease !important;
}
[data-testid="stChatInput"] button:hover { transform: scale(1.05) !important; }

/* SCROLLBAR HIDUP */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00F5FF, #FF00E5);
    border-radius: 10px;
}

/* FIX HP */
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
    st.markdown("### MasterAI")
    st.markdown('<span class="badge">COLORFUL</span> <span class="badge">ALIVE</span> <span class="badge">RGB</span> <span class="badge">GERAK</span>', unsafe_allow_html=True)
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
