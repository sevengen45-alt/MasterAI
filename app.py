import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v10 - Light RGB", page_icon="⚡", layout="wide")

DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

/* ===== LIGHTWEIGHT VERSION ===== */
.stApp {
    background: #0A0A12 !important; /* gak pure hitam, biar mata gak sakit */
}
/* HAPUS ORB RAKSASA - GANTI 2 ORB KECIL AJA */
.stApp::before {
    content: ""; position: fixed; inset: 0;
    background: 
        radial-gradient(ellipse 400px 300px at 20% 20%, rgba(255,0,128,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 400px 300px at 80% 80%, rgba(0,245,255,0.12) 0%, transparent 60%);
    animation: orbLight 25s ease-in-out infinite alternate;
    filter: blur(0px); /* HAPUS BLUR - INI YANG BIKIN LAG */
    z-index: 0; pointer-events: none;
    will-change: transform; /* GPU acceleration */
}
@keyframes orbLight { 0%{transform: translate(0,0)} 100%{transform: translate(-2%,2%)} }

[data-testid="stAppViewContainer"] { position: relative; z-index: 1; }

/* JUDUL - SIMPLIFIED, HAPUS FLOAT + GLOW PULSE */
h1 {
    background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    text-align: center !important; font-weight: 800 !important; font-size: 4rem !important;
    animation: rainbowFlow 4s linear infinite !important; /* cuma 1 animasi, bukan 3 */
    will-change: background-position;
}
@keyframes rainbowFlow { 0%{background-position:0%} 100%{background-position:300%} }
@media (max-width:600px){ h1{font-size:2.6rem !important;} }

/* SIDEBAR - HAPUS BACKDROP-FILTER, HAPUS BORDER ANIMASI */
section[data-testid="stSidebar"] {
    background: #12121E !important; /* solid color, no blur */
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}

/* CHAT BUBBLE - HAPUS BLUR, HAPUS SHINE, HAPUS ::AFTER RGB */
.stChatMessage {
    background: #181828 !important; /* solid, no gradient */
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    box-shadow: none !important; /* HAPUS SHADOW GEDE */
    animation: popSimple 0.35s ease !important;
}
@keyframes popSimple { 0%{opacity:0; transform: translateY(8px)} 100%{opacity:1; transform: translateY(0)} }
.stChatMessage:hover { border-color: rgba(0,245,255,0.2) !important; transform: none !important; } /* HAPUS scale */
.stChatMessage p { color: #E8E8F0 !important; font-size: 15.5px !important; line-height: 1.6 !important; }
.stChatMessage strong { color: #00F5FF !important; }

/* BADGE - SIMPLIFIED */
.badge {
    background: #1E1E32 !important; /* solid, gak gradient animasi berat */
    border: 1px solid rgba(0,245,255,0.2);
    padding: 5px 12px; border-radius: 20px; color: #00F5FF; font-weight: 700; font-size: 10px;
    display: inline-block; margin: 3px;
}

/* INPUT - HAPUS BREATH, HAPUS DOUBLE SHADOW */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0040, #FFE600, #00F5FF, #7B61FF) !important;
    background-size: 300% 100% !important;
    animation: rainbowFlow 3s linear infinite !important; /* cuma 1 animasi */
    padding: 2px !important; border-radius: 24px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important; /* shadow kecil aja */
    max-width: 720px !important; margin: 0 auto !important;
}
[data-testid="stChatInput"] > div { background: #12121E !important; border-radius: 22px !important; border: none !important; }
[data-testid="stChatInput"] textarea { color: #FFF !important; font-size: 15px !important; }
[data-testid="stChatInput"] button { background: #00F5FF !important; border-radius: 50% !important; color: #000 !important; font-weight: 800 !important; }

.bio-card {
    background: #181828 !important; border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important; padding: 14px !important;
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Ngobrol!", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI")
    st.markdown('<span class="badge">LIGHT RGB</span> <span class="badge">FAST</span>', unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<div class='bio-card'><div style='color:white; font-weight:800; text-align:center;'>Juan • 15 Tahun<br><span style='color:#00F5FF; font-size:11px;'>SMAK Monte Carmelo</span></div></div>", unsafe_allow_html=True)
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"Yo {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama lu siapa bang?", placeholder="Juan")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()
    st.markdown("### 💬 Obrolan")
    if st.button("➕ Baru", use_container_width=True):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.divider()
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True):
        if st.button(f"{chat['title'][:24]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.title(active["title"])

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "⚡"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya {st.session_state.user_memory['nama'] or ''}..."):
    if len(active["messages"]) == 0: active["title"] = prompt[:30]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="⚡"):
        ph = st.empty()
        ph.markdown("Thinking...")
        try:
            lower = prompt.lower()
            if any(k in lower for k in ["siapa yang membuat","siapa pembuat","dibuat siapa","siapa developer","kamu dibuat siapa"]):
                ans = DEVELOPER_INFO
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                nama = st.session_state.user_memory["nama"] or "bang"
                system_prompt = f"Kamu MasterAI v10. {DEVELOPER_INFO} User {nama}. Bahasa gaul santai."
                messages = [{"role": "system", "content": system_prompt}] + active["messages"]
                res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.8, max_tokens=1200)
                ans = res.choices[0].message.content
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
        except Exception as e:
            ph.error(f"Error: {e}")
