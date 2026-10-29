import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI - Potato Mode", page_icon="⚡", layout="wide")

DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! 15 tahun, SMAK St. Maria Monte Carmelo Maumere, panggilan Juan."

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600;700&display=swap');
* {font-family: 'Inter', sans-serif !important;}

/* ===== POTATO MODE - 0% BLUR, 0% LAG ===== */
.stApp { background: #0E0E14 !important; }
/* HAPUS TOTAL ORB & BLUR - INI BIANG LAG */
.stApp::before { display: none !important; }
[data-testid="stAppViewContainer"] { background: transparent !important; }

/* JUDUL - STATIC GRADIENT, NO ANIMASI (hemat 100% CPU) */
h1 {
    background: linear-gradient(90deg, #FF0040, #FFE600, #00F5FF) !important;
    -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    text-align: center !important; font-weight: 700 !important; font-size: 3rem !important;
}
@media (max-width:600px){ h1{font-size:2.2rem !important;} }

/* SIDEBAR - SOLID, NO BLUR */
section[data-testid="stSidebar"] { background: #16161F !important; border-right: 1px solid #222 !important; }

/* CHAT - SOLID, NO ANIMATION, NO SHADOW GEDE */
.stChatMessage {
    background: #1C1C28 !important;
    border-radius: 12px !important;
    border: 1px solid #2A2A3A !important;
    box-shadow: none !important;
    max-width: 700px !important; margin: 8px auto !important;
}
.stChatMessage p { color: #E0E0E8 !important; font-size: 14.5px !important; }

/* BADGE - SOLID COLOR DOANG */
.badge { background: #2A2A3A !important; color: #00F5FF !important; padding: 4px 10px; border-radius: 10px; font-size: 10px; font-weight: 700; display: inline-block; margin: 2px; }

/* INPUT - BORDER TIPIS DOANG, NO ANIMASI PELANGI JALAN */
[data-testid="stChatInput"] {
    background: #2A2A3A !important; /* solid, bukan gradient animasi */
    padding: 2px !important; border-radius: 20px !important;
    box-shadow: none !important;
    max-width: 700px !important; margin: 0 auto !important;
    border: 1px solid #3A3A4A !important;
}
[data-testid="stChatInput"] > div { background: #16161F !important; border-radius: 18px !important; }
[data-testid="stChatInput"] textarea { color: #FFF !important; font-size: 14.5px !important; }
[data-testid="stChatInput"] button { background: #00F5FF !important; color: #000 !important; border-radius: 50% !important; }

@media (max-width: 768px) {
    [data-testid="stChatInput"] { max-width: 96% !important; position: fixed !important; bottom: 10px !important; left: 2% !important; right: 2% !important; z-index: 999 !important; }
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Ngobrol Yuk!", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI 🥔")
    st.markdown('<span class="badge">POTATO</span> <span class="badge">2GB RAM</span> <span class="badge">60FPS</span>', unsafe_allow_html=True)
    st.divider()
    st.caption("👨‍💻 Juan • 15th • Maumere")
    if st.session_state.user_memory["nama"]:
        st.success(f"Yo {st.session_state.user_memory['nama']}!")
    else:
        nama = st.text_input("Nama lu?", placeholder="Juan")
        if nama:
            st.session_state.user_memory["nama"] = nama
            st.rerun()
    if st.button("➕ Baru", use_container_width=True):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()

active = get_active()
st.title(active["title"])

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="👤" if m["role"]=="user" else "⚡"):
        st.markdown(m["content"])

if prompt := st.chat_input("Tanya apa..."):
    if len(active["messages"]) == 0: active["title"] = prompt[:25]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="⚡"):
        ph = st.empty()
        ph.markdown("...")
        try:
            if "siapa yang membuat" in prompt.lower() or "siapa pembuat" in prompt.lower() or "dibuat siapa" in prompt.lower():
                ans = DEVELOPER_INFO
            else:
                nama = st.session_state.user_memory["nama"] or "bang"
                messages = [{"role": "system", "content": f"Kamu MasterAI. {DEVELOPER_INFO} User {nama}. Bahasa gaul."}] + active["messages"]
                res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.7, max_tokens=1000)
                ans = res.choices[0].message.content
            ph.markdown(ans)
            active["messages"].append({"role": "assistant", "content": ans})
        except Exception as e:
            ph.error(f"Error: {e}")
