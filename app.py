import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v17 - Apple White", page_icon="", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800;900&display=swap');
* {font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;}

/* ===== BACKGROUND PUTIH APPLE - BERSIH BANGET ===== */
.stApp {
    background: #FBFBFD !important;
    background-image: none !important;
}
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: 
        radial-gradient(at 15% 15%, rgba(0,122,255,0.04) 0%, transparent 50%),
        radial-gradient(at 85% 15%, rgba(175,82,222,0.03) 0%, transparent 50%),
        radial-gradient(at 50% 85%, rgba(0,122,255,0.02) 0%, transparent 60%);
    pointer-events: none;
    z-index: -1;
}

/* ===== JUDUL - HITAM PEKAT APPLE STYLE ===== */
.apple-title {
    color: #1D1D1F !important;
    text-align: center !important;
    font-weight: 800 !important;
    font-size: 3.2rem !important;
    letter-spacing: -0.04em !important;
    line-height: 1.05 !important;
    display: block !important;
    padding: 40px 0 8px 0 !important;
}
.apple-subtitle {
    text-align: center !important;
    color: #86868B !important;
    font-size: 17px !important;
    font-weight: 400 !important;
    margin-bottom: 30px !important;
}
@media (max-width: 600px) { .apple-title { font-size: 2rem !important; } }

/* ===== SIDEBAR - PUTIH ABU APPLE SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: #F5F5F7 !important;
    border-right: 1px solid rgba(0,0,0,0.06) !important;
}
section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] h4 {
    color: #1D1D1F !important;
}
section[data-testid="stSidebar"] .stButton button {
    background: #FFFFFF !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    color: #1D1D1F !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    text-align: left !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    border-color: rgba(0,0,0,0.1) !important;
}
section[data-testid="stSidebar"] button[kind="primary"] {
    background: #007AFF !important;
    color: white !important;
    border: none !important;
}

/* ===== CHAT - APPLE MESSAGE STYLE ===== */
.stChatMessage {
    background: transparent !important;
    border: none !important;
    padding: 12px 0 !important;
    max-width: 720px !important;
    margin: 0 auto !important;
}
div[data-testid="stChatMessageContent"] {
    border-radius: 18px !important;
    padding: 12px 16px !important;
}
.stChatMessage[data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stChatMessageContent"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
.stChatMessage[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stChatMessageContent"] {
    background: transparent !important;
}
.stChatMessage p {
    color: #1D1D1F !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    font-weight: 400 !important;
}
[data-testid="chatAvatarIcon-user"], [data-testid="chatAvatarIcon-assistant"] {
    background: #E8E8ED !important;
    color: #1D1D1F !important;
}

/* ===== BADGE - APPLE PILL ===== */
.apple-pill {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.02em;
    margin: 3px;
}
.pill-blue { background: #007AFF !important; color: white !important; }
.pill-gray { background: #E8E8ED !important; color: #1D1D1F !important; }
.pill-dark { background: #1D1D1F !important; color: white !important; }

/* ===== TASKBAR - APPLE FLOATING ISLAND PUTIH ===== */
div[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.85) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 24px !important;
    padding: 8px !important;
    box-shadow: 
        0 1px 3px rgba(0,0,0,0.04),
        0 8px 24px rgba(0,0,0,0.08) !important;
    bottom: 24px !important;
    max-width: 700px !important;
    margin: 0 auto !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: rgba(0,122,255,0.3) !important;
    box-shadow: 
        0 0 0 4px rgba(0,122,255,0.1),
        0 8px 24px rgba(0,0,0,0.08) !important;
}
div[data-testid="stChatInput"] > div {
    background: transparent !important;
}
div[data-testid="stChatInput"] textarea {
    color: #1D1D1F !important;
    font-weight: 400 !important;
    font-size: 16px !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: #86868B !important;
}
div[data-testid="stChatInput"] button {
    background: #1D1D1F !important;
    color: white !important;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
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
    st.markdown('<span class="apple-pill pill-dark"> APPLE</span> <span class="apple-pill pill-gray">V17</span> <span class="apple-pill pill-blue">JUAN</span>', unsafe_allow_html=True)
    st.markdown("#### ")
    if st.session_state.user_memory["nama"]:
        st.markdown(f"**{st.session_state.user_memory['nama']}**")
    else:
        nama_input = st.text_input("Nama", placeholder="Nama kamu?", label_visibility="collapsed")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()
    st.divider()
    if st.button("＋ New Chat", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"New Chat", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.markdown(" ")
    st.caption("Recent")
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True)[:10]:
        if st.button(f"{chat['title'][:24]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.markdown(f"<div class='apple-title'>{active['title']}</div><div class='apple-subtitle'>Apple Intelligence • by Juan • Maumere</div>", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask anything..."):
    if len(active["messages"]) == 0: active["title"] = prompt[:40]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        ph = st.empty()
        ph.markdown("▌")
        try:
            nama = st.session_state.user_memory["nama"] or ""
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = DEVELOPER_INFO
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI Apple Edition. Pembuat: {DEVELOPER_INFO}. User: {nama}. Gaya Apple: clean, helpful, minimalis."
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
