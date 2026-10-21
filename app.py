import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v11 - Color Live", page_icon="🌈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

/* ===== BACKGROUND - WARNA JALAN PELAN, TAPI GAK GOYANG ===== */
.stApp {
    background: #000 !important;
    background-image: 
        radial-gradient(circle at 20% 30%, #FF0000 0%, transparent 40%),
        radial-gradient(circle at 80% 20%, #00F5FF 0%, transparent 40%),
        radial-gradient(circle at 50% 80%, #FFD600 0%, transparent 40%),
        radial-gradient(circle at 10% 90%, #7B61FF 0%, transparent 40%),
        radial-gradient(circle at 90% 90%, #FF00E5 0%, transparent 40%) !important;
    background-size: 150% 150% !important;
    animation: bgColorMove 12s ease infinite alternate !important;
}
@keyframes bgColorMove {
    0% { background-position: 0% 0%, 100% 0%, 50% 100%, 0% 100%, 100% 100%; filter: brightness(1); }
    100% { background-position: 20% 30%, 80% 20%, 50% 80%, 10% 90%, 90% 90%; filter: brightness(1.2); }
}

/* ===== JUDUL - CUMA WARNA PELANGI JALAN, GAK GOYANG ===== */
h1 {
    background: linear-gradient(90deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF, #FF00E5, #FF0000) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important; 
    font-weight: 900 !important; 
    font-size: 5.5rem !important;
    animation: titleColorMove 3s linear infinite !important;
}
@keyframes titleColorMove { 0%{background-position:0%} 100%{background-position:300%} }
@media (max-width: 600px) { h1 {font-size: 3rem !important;} }

/* ===== SIDEBAR - DIEM, GAK NAIK TURUN ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0A1A, #1A0A2A) !important;
    border-right: 3px solid transparent !important;
    border-image: linear-gradient(180deg, #FF0000, #FFD600, #00F5FF, #FF00E5) 1 !important;
}

/* ===== CHAT BUBBLE - DIEM, GAK BERNAFAS ===== */
.stChatMessage {
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    background: rgba(255,255,255,0.07) !important;
}
.stChatMessage p { color: white !important; font-size: 17px !important; font-weight: 600 !important; }

/* ===== BADGE - CUMA WARNA JALAN, GAK LOMPAT ===== */
.badge {
    padding: 6px 14px; border-radius: 20px; color: white; font-weight: 900; font-size: 11px; margin: 3px; display: inline-block;
    background: linear-gradient(90deg, #FF0000, #FFD600, #00F5FF, #FF00E5) !important;
    background-size: 300% 100% !important;
    animation: badgeColorMove 3s linear infinite !important;
}
@keyframes badgeColorMove { 0%{background-position:0%} 100%{background-position:300%} }

/* ===== INPUT TASKBAR - CUMA BORDER PELANGI JALAN, GAK MEMBESAR & GAK GOYANG ===== */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0000, #FFFF00, #00FF00, #00FFFF, #0000FF, #FF00FF, #FF0000) !important;
    background-size: 600% 100% !important;
    animation: inputColorMove 2s linear infinite !important;
    padding: 4px !important; 
    border-radius: 30px !important;
    box-shadow: 0 0 25px rgba(255,0,229,0.4), 0 0 50px rgba(0,245,255,0.2) !important;
}
@keyframes inputColorMove { 0%{background-position:0%} 100%{background-position:600%} }
[data-testid="stChatInput"] > div { 
    background: #0A0A14 !important; 
    border-radius: 26px !important; 
}
[data-testid="stChatInput"] textarea { color: white !important; font-weight: 700 !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #00F5FF, #7B61FF) !important;
    border-radius: 50% !important;
}

/* HAPUS TOTAL EMOJI JATUH */
.stApp::after { display: none !important; content: none !important; }
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
    st.markdown("### 🌈 MASTER AI v11 Color Live")
    st.markdown('<span class="badge">COLOR LIVE</span> <span class="badge">JUAN</span>', unsafe_allow_html=True)
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

with st.expander("💬 Daftar Obrolan (HP)", expanded=False):
    st.write(f"Ada {len(st.session_state.chats)} obrolan")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "🌈"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya apa saja! 👨🏼‍💻✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌈"):
        ph = st.empty()
        ph.markdown("▌ _lagi mikir..._ 🌈")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"Yo {nama}! {DEVELOPER_INFO}"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v11 Color Live. PEMBUAT KAMU {DEVELOPER_INFO}. User: {nama}. Gaul Jaksel."
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
