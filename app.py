import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v18 - White Rainbow", page_icon="🌈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
* {font-family: 'Inter', -apple-system, sans-serif !important;}

/* ===== BACKGROUND - PUTIH APPLE + GLOW PELANGI SUPER HALUS ===== */
.stApp {
    background: #FBFBFD !important;
}
.stApp::before {
    content: "";
    position: fixed; inset: 0;
    background: 
        radial-gradient(at 10% 10%, rgba(255,0,85,0.05) 0%, transparent 45%),
        radial-gradient(at 90% 10%, rgba(255,171,0,0.04) 0%, transparent 45%),
        radial-gradient(at 50% 50%, rgba(0,230,118,0.03) 0%, transparent 60%),
        radial-gradient(at 10% 90%, rgba(41,121,255,0.05) 0%, transparent 45%),
        radial-gradient(at 90% 90%, rgba(170,0,255,0.04) 0%, transparent 45%);
    pointer-events: none;
    z-index: -1;
    animation: whiteRainbowBg 20s ease infinite alternate;
}
@keyframes whiteRainbowBg {
    0% { opacity: 0.8; filter: hue-rotate(0deg); }
    100% { opacity: 1; filter: hue-rotate(20deg); }
}

/* ===== JUDUL - HITAM TAPI ADA PELANGI TIPIS JALAN DIBAWAHNYA ===== */
.white-rainbow-title {
    color: #1D1D1F !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 3.5rem !important;
    letter-spacing: -0.04em !important;
    line-height: 1 !important;
    display: block !important;
    padding: 40px 0 0 0 !important;
    position: relative !important;
}
.white-rainbow-title::after {
    content: "";
    display: block;
    width: 200px;
    height: 4px;
    margin: 15px auto 0 auto;
    background: linear-gradient(90deg, #FF0055, #FFAB00, #00E676, #2979FF, #AA00FF, #FF0055);
    background-size: 400% 100%;
    animation: rainbowLine 3s linear infinite;
    border-radius: 100px;
}
@keyframes rainbowLine { 0%{background-position:0%} 100%{background-position:400%} }
.white-rainbow-sub {
    text-align: center !important;
    color: #86868B !important;
    font-size: 15px !important;
    margin: 12px 0 30px 0 !important;
    font-weight: 500 !important;
}
@media (max-width: 600px) { .white-rainbow-title { font-size: 2.2rem !important; } }

/* ===== SIDEBAR - PUTIH + BORDER PELANGI TIPIS ===== */
section[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid rgba(0,0,0,0.06) !important;
    position: relative;
}
section[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    top: 0; right: 0;
    width: 2px; height: 100%;
    background: linear-gradient(180deg, #FF0055, #FFAB00, #00E676, #2979FF, #AA00FF);
    background-size: 100% 400%;
    animation: sidebarRainbow 5s linear infinite;
}
@keyframes sidebarRainbow { 0%{background-position:0% 0%} 100%{background-position:0% 400%} }
section[data-testid="stSidebar"] .stButton button {
    background: #F5F5F7 !important;
    border: none !important;
    color: #1D1D1F !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* ===== CHAT - PUTIH + BORDER KIRI PELANGI LIVE ===== */
.stChatMessage {
    background: #FFFFFF !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    border-left: 3px solid transparent !important;
    border-image: linear-gradient(180deg, #FF0055, #FFAB00, #00E676, #2979FF, #AA00FF) 1 !important;
    border-radius: 16px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    padding: 4px !important;
    margin: 10px auto !important;
    max-width: 720px !important;
}
.stChatMessage p { color: #1D1D1F !important; font-size: 15px !important; line-height: 1.6 !important; }

/* ===== BADGE - PUTIH + PELANGI GRADIENT ===== */
.pill {
    display: inline-block; padding: 6px 14px; border-radius: 100px;
    font-size: 11px; font-weight: 700; margin: 3px;
    background-size: 300% 100% !important;
    animation: rainbowLine 3s linear infinite !important;
    color: white !important;
}
.pill-r1 { background: linear-gradient(90deg, #FF0055, #FFAB00) !important; }
.pill-r2 { background: linear-gradient(90deg, #00E676, #2979FF) !important; }
.pill-r3 { background: linear-gradient(90deg, #2979FF, #AA00FF) !important; }
.pill-white { background: #F5F5F7 !important; color: #1D1D1F !important; border: 1px solid rgba(0,0,0,0.06) !important; animation: none !important; }

/* ===== TASKBAR - PUTIH APPLE + BORDER PELANGI LIVE JALAN ===== */
div[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0055, #FFAB00, #00E676, #2979FF, #AA00FF, #FF0055) !important;
    background-size: 500% 100% !important;
    animation: rainbowLine 2.5s linear infinite !important;
    padding: 2px !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.04) !important;
    bottom: 24px !important;
    max-width: 700px !important;
    margin: 0 auto !important;
}
div[data-testid="stChatInput"] > div {
    background: rgba(255,255,255,0.92) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 22px !important;
}
div[data-testid="stChatInput"] textarea {
    color: #1D1D1F !important;
    font-weight: 400 !important;
    font-size: 16px !important;
}
div[data-testid="stChatInput"] textarea::placeholder { color: #86868B !important; }
div[data-testid="stChatInput"] button {
    background: #1D1D1F !important;
    color: white !important;
    border-radius: 50% !important;
}
</style>
""", unsafe_allow_html=True)

DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Memulai Obrolan?", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown('<span class="pill pill-r1">RAINBOW</span> <span class="pill pill-r2">WHITE</span> <span class="pill pill-white">JUAN</span>', unsafe_allow_html=True)
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Yo {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama", placeholder="Nama kamu?", label_visibility="collapsed")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()
    if st.button("＋ New Chat", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": "New Chat", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.caption(f"{len(st.session_state.chats)} chats")
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True)[:10]:
        if st.button(f"{chat['title'][:24]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.markdown(f"<div class='white-rainbow-title'>{active['title']}</div><div class='white-rainbow-sub'>White Apple • Rainbow Live • by Juan Maumere</div>", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Tanya apa saja! 👨🏼‍💻✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        ph = st.empty()
        ph.markdown("▌")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = DEVELOPER_INFO
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI White Rainbow. Pembuat: {DEVELOPER_INFO}. User: {nama}. Clean helpful."
                messages = [{"role": "system", "content": system_prompt}] + active["messages"]
                res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.7, max_tokens=1500)
                ans = res.choices[0].message.content
                full = ""
                for w in ans.split(" "):
                    full += w + " "
                    ph.markdown(full + "▌")
                    time.sleep(0.015)
                ph.markdown(full)
                active["messages"].append({"role": "assistant", "content": full})
        except Exception as e:
            ph.error(f"Error: {e}")
