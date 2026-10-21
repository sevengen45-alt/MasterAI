import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v10.1 - Perfected RGB", page_icon="🇮🇩", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}
p, li, span, div { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: #070711 !important;
    position: relative;
}
.stApp::before {
    content: ""; position: fixed; inset: -30%;
    background: 
        radial-gradient(ellipse 600px 500px at 15% 20%, rgba(255,0,100,0.32) 0%, transparent 60%),
        radial-gradient(ellipse 700px 600px at 85% 15%, rgba(0,230,255,0.30) 0%, transparent 60%),
        radial-gradient(ellipse 800px 500px at 50% 90%, rgba(255,210,0,0.20) 0%, transparent 65%),
        radial-gradient(ellipse 500px 500px at 20% 85%, rgba(120,0,255,0.35) 0%, transparent 60%);
    animation: perfectFloat 22s ease-in-out infinite alternate;
    filter: blur(22px); z-index: 0; pointer-events: none;
}
@keyframes perfectFloat {
    0% { transform: translate3d(0,0,0) scale(1); }
    100% { transform: translate3d(-2%, 2%, 0) scale(1.06); }
}
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; }

/* JUDUL - SEMPURNA, HALUS, TAPI TETAP HIDUP */
h1 {
    background: linear-gradient(90deg, #FF2A5A, #FF8A1A, #FFD600, #00E67A, #00E5FF, #7B61FF, #FF2AD4, #FF2A5A) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 4.6rem !important;
    letter-spacing: -0.05em !important;
    line-height: 0.95 !important;
    animation: perfectRainbow 6s linear infinite, perfectTitleFloat 4s ease-in-out infinite alternate !important;
    filter: drop-shadow(0 4px 20px rgba(255,0,150,0.35)) !important;
    padding-bottom: 12px !important;
}
@keyframes perfectRainbow { 0%{background-position:0% 50%} 100%{background-position:300% 50%} }
@keyframes perfectTitleFloat { 0%{transform: translateY(0)} 100%{transform: translateY(-4px)} }
@media (max-width:600px){ h1{font-size:3rem !important;} }

/* SIDEBAR - SEMPURNA, GLASS PREMIUM */
section[data-testid="stSidebar"] {
    background: rgba(14,12,30,0.82) !important;
    backdrop-filter: blur(32px) saturate(1.3) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    box-shadow: 12px 0 50px rgba(0,0,0,0.4) !important;
}
section[data-testid="stSidebar"]::after {
    content: ""; position: absolute; top: 0; right: 0; width: 1.5px; height: 100%;
    background: linear-gradient(180deg, #FF2A5A 0%, #FFD600 25%, #00E5FF 50%, #7B61FF 75%, #FF2AD4 100%);
    background-size: 100% 300%; animation: perfectBorder 6s linear infinite; opacity: 0.8;
}
@keyframes perfectBorder { 0%{background-position:0% 0%} 100%{background-position:0% 300%} }

/* CHAT BUBBLE - SEMPURNA, TIDAK BERLEBIHAN */
.stChatMessage {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04)) !important;
    backdrop-filter: blur(20px) saturate(1.2) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.06) !important;
    position: relative; overflow: hidden;
    animation: perfectPop 0.5s cubic-bezier(0.16,1,0.3,1) !important;
    transition: all 0.3s cubic-bezier(0.16,1,0.3,1) !important;
    max-width: 760px !important; margin: 12px auto !important;
}
@keyframes perfectPop { 0%{opacity:0; transform: translateY(10px)} 100%{opacity:1; transform: translateY(0)} }
.stChatMessage:hover {
    transform: translateY(-1px) !important;
    border-color: rgba(255,255,255,0.14) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.32), inset 0 1px 0 rgba(255,255,255,0.08) !important;
}
.stChatMessage::before {
    content: ""; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
    animation: perfectShine 6s ease-in-out infinite;
}
@keyframes perfectShine { 0%{left:-100%} 60%{left:200%} 100%{left:200%} }

.stChatMessage p { color: rgba(255,255,255,0.92) !important; font-size: 15.5px !important; line-height: 1.7 !important; font-weight: 450 !important; }
.stChatMessage strong { color: #5EE6FF !important; font-weight: 700 !important; }

/* BADGE - SEMPURNA, KECIL ELEGAN */
.badge {
    background: linear-gradient(90deg, #FF2A5A, #FF8A1A, #FFD600, #00E67A, #00E5FF, #7B61FF) !important;
    background-size: 250% 100% !important;
    animation: perfectRainbow 4s linear infinite !important;
    padding: 5px 13px; border-radius: 100px; color: #FFF; font-size: 10.5px; font-weight: 800;
    letter-spacing: 0.08em; display: inline-block; margin: 3px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.25);
}

/* INPUT - SEMPURNA, FOKUS PREMIUM */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF2A5A, #FF8A1A, #FFD600, #00E67A, #00E5FF, #7B61FF, #FF2AD4) !important;
    background-size: 300% 100% !important;
    animation: perfectRainbow 3.5s linear infinite !important;
    padding: 2px !important;
    border-radius: 24px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.04) !important;
    max-width: 740px !important; margin: 0 auto !important;
    transition: all 0.3s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    box-shadow: 0 8px 36px rgba(0,0,0,0.45), 0 0 28px rgba(123,97,255,0.35) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stChatInput"] > div {
    background: #12121E !important;
    border-radius: 22px !important;
    border: none !important;
}
[data-testid="stChatInput"] textarea {
    color: #FFF !important; font-weight: 500 !important; font-size: 15.5px !important;
    -webkit-text-fill-color: #FFF !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(255,255,255,0.45) !important; -webkit-text-fill-color: rgba(255,255,255,0.45) !important;
}
[data-testid="stChatInput"] button {
    background: #FFFFFF !important;
    color: #0A0A14 !important; border-radius: 14px !important;
    font-weight: 800 !important; width: 32px !important; height: 32px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stChatInput"] button:hover {
    transform: scale(1.06) !important; background: #F0F0F5 !important;
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
    st.markdown('<span class="badge">PERFECTED</span> <span class="badge">PREMIUM</span> <span class="badge">SMOOTH</span>', unsafe_allow_html=True)
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
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "✨"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'saja!'} ✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="✨"):
        ph = st.empty()
        ph.markdown("▌ _Thinking..._")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            system_prompt = f"Kamu MasterAI v10.1 Perfected. Nama user {nama}. Bahasa Indonesia gaul, santai, jawab jelas dan bener."
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
