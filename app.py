import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v16 - Obsidian Gold", page_icon="🪙", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
* {font-family: 'Inter', sans-serif !important;}

/* BACKGROUND - HITAM PEKAT GOLD HIDUP PELAN */
.stApp {
    background: #080608 !important;
    background-image: 
        radial-gradient(at 20% 20%, rgba(255,215,0,0.08) 0%, transparent 60%),
        radial-gradient(at 80% 80%, rgba(255,165,0,0.06) 0%, transparent 60%) !important;
    animation: goldBreath 8s ease infinite alternate !important;
}
@keyframes goldBreath { 0%{filter:brightness(1)} 100%{filter:brightness(1.1)} }

/* JUDUL - PUTIH BERSIH GOLD GLOW, DIEM, GAK PELANGI */
.live-title {
    color: #FFFFFF !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 4rem !important;
    letter-spacing: -0.05em !important;
    text-shadow: 0 0 30px rgba(255,215,0,0.3) !important;
    display: block !important;
    padding: 30px 0 10px 0 !important;
    line-height: 0.9 !important;
}
.live-subtitle {
    text-align: center !important;
    color: rgba(255,255,255,0.4) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase !important;
    margin-bottom: 25px !important;
}
@media (max-width: 600px) { .live-title { font-size: 2.4rem !important; } }

/* SIDEBAR - FULL HITAM MINIMALIS */
section[data-testid="stSidebar"] {
    background: #0A0A0A !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: rgba(255,255,255,0.6) !important;
    border-radius: 10px !important;
    text-align: left !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,215,0,0.08) !important;
    border-color: rgba(255,215,0,0.2) !important;
    color: #FFD700 !important;
}

/* CHAT BUBBLE - MINIMALIS KAYA CHATGPT */
.stChatMessage {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 0 !important;
    padding: 20px 0 !important;
}
.stChatMessage[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: rgba(255,255,255,0.02) !important;
}
.stChatMessage p { 
    color: #E8E8E8 !important; 
    font-size: 15px !important; 
    line-height: 1.7 !important;
    font-weight: 400 !important;
}

/* BADGE - GOLD MINIMALIS */
.badge-gold {
    background: #FFD700 !important;
    color: #000 !important;
    padding: 4px 10px; border-radius: 6px; font-weight: 900; font-size: 10px;
    letter-spacing: 0.1em; margin: 2px; display: inline-block;
}
.badge-dark {
    background: rgba(255,255,255,0.08) !important;
    color: rgba(255,255,255,0.5) !important;
    padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 10px;
    border: 1px solid rgba(255,255,255,0.08); margin: 2px; display: inline-block;
}

/* TASKBAR - FLOATING ISLAND GOLD LIVE */
div[data-testid="stChatInput"] {
    background: #1A1A1A !important;
    border: 1px solid rgba(255,215,0,0.25) !important;
    border-radius: 20px !important;
    padding: 6px !important;
    box-shadow: 
        0 0 0 1px rgba(255,215,0,0.1),
        0 10px 40px rgba(0,0,0,0.8),
        0 0 40px rgba(255,215,0,0.08) !important;
    bottom: 30px !important;
    max-width: 750px !important;
    margin: 0 auto !important;
    animation: goldGlow 3s ease infinite alternate !important;
}
@keyframes goldGlow {
    0% { border-color: rgba(255,215,0,0.25); box-shadow: 0 0 0 1px rgba(255,215,0,0.1), 0 10px 40px rgba(0,0,0,0.8), 0 0 40px rgba(255,215,0,0.08); }
    100% { border-color: rgba(255,215,0,0.4); box-shadow: 0 0 0 1px rgba(255,215,0,0.2), 0 10px 40px rgba(0,0,0,0.8), 0 0 60px rgba(255,215,0,0.15); }
}
div[data-testid="stChatInput"] > div { background: transparent !important; }
div[data-testid="stChatInput"] textarea { 
    color: white !important; 
    font-weight: 400 !important;
    font-size: 15px !important;
}
div[data-testid="stChatInput"] button {
    background: #FFD700 !important;
    color: black !important;
    border-radius: 12px !important;
}
div[data-testid="stChatInput"] button:hover { background: #FFC400 !important; }
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
    st.markdown('<span class="badge-gold">OBSIDIAN GOLD</span> <span class="badge-dark">V16</span>', unsafe_allow_html=True)
    st.markdown("#### MasterAI")
    st.caption("Obsidian Edition by Juan")
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Yo {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama lu siapa bang?", placeholder="Nama lu?")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()
    if st.button("＋ New Chat", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.divider()
    st.caption(f"{len(st.session_state.chats)} conversations")
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True)[:15]:
        if st.button(f"{chat['title'][:26]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.markdown(f"<div class='live-title'>{active['title']}</div><div class='live-subtitle'>OBSIDIAN • GOLD • BY JUAN</div>", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="●" if m["role"]=="user" else "◍"):
        st.markdown(m["content"])

if prompt := st.chat_input("Tanya apa saja..."):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="●"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="◍"):
        ph = st.empty()
        ph.markdown("▌")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"{DEVELOPER_INFO}"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v16 Obsidian Gold. PEMBUAT KAMU ADALAH {DEVELOPER_INFO}. User: {nama}. Jawab elegan, minimalis, pro."
                messages = [{"role": "system", "content": system_prompt}] + active["messages"]
                res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.8, max_tokens=1500)
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
