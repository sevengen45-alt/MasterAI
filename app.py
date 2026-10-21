import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v13 - Vibrant", page_icon="🎨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@700;800;900&display=swap');
* {font-family: 'Geist', sans-serif !important;}

/* BACKGROUND - MESH GRADIENT 5 WARNA BERGERAK PELAN TAPI VIBRANT */
.stApp {
    background-color: #080810 !important;
    background-image: 
        radial-gradient(at 0% 0%, hsla(253,100%,70%,0.5) 0px, transparent 50%),
        radial-gradient(at 50% 0%, hsla(189,100%,56%,0.4) 0px, transparent 50%),
        radial-gradient(at 100% 0%, hsla(22,100%,60%,0.4) 0px, transparent 50%),
        radial-gradient(at 0% 100%, hsla(343,100%,60%,0.5) 0px, transparent 50%),
        radial-gradient(at 50% 100%, hsla(24,100%,65%,0.3) 0px, transparent 50%),
        radial-gradient(at 100% 100%, hsla(189,100%,70%,0.4) 0px, transparent 50%) !important;
    animation: meshMove 15s ease infinite alternate !important;
}
@keyframes meshMove {
    0% { background-position: 0% 0%, 50% 0%, 100% 0%, 0% 100%, 50% 100%, 100% 100%; }
    100% { background-position: 10% 20%, 60% 10%, 90% 20%, 10% 80%, 40% 90%, 90% 80%; }
}

/* TITLE - VIBRANT 3 WARNA DOANG TAPI PEKAT + GERAK */
h1 {
    background: linear-gradient(100deg, #8B5CF6 0%, #06B6D4 50%, #F43F5E 100%) !important;
    background-size: 200% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 900 !important; font-size: 4.8rem !important; text-align: center !important;
    letter-spacing: -0.04em !important;
    animation: titleShift 4s ease infinite !important;
}
@keyframes titleShift { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
@media (max-width: 600px) { h1 {font-size: 3rem !important;} }

/* SIDEBAR - DARK + GLOW TIPIS WARNA-WARNI */
section[data-testid="stSidebar"] {
    background: rgba(10,10,18,0.9) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(139,92,246,0.2) !important;
}

/* CHAT - SETIAP PESAN WARNA BEDA TIPIS */
.stChatMessage {
    background: rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 16px !important;
    border-left: 3px solid transparent !important;
    border-image: linear-gradient(180deg, #8B5CF6, #06B6D4) 1 !important;
}
.stChatMessage:nth-child(even) {
    border-image: linear-gradient(180deg, #F43F5E, #FB923C) 1 !important;
}
.stChatMessage p { color: #F8FAFC !important; font-size: 15.5px !important; }

/* BADGE - WARNA SOLID VIBRANT, GAK PELANGI JALAN */
.badge {
    padding: 6px 14px; border-radius: 100px; font-weight: 800; font-size: 11px; color: white;
    display: inline-block; margin: 3px;
}
.b-purple { background: #8B5CF6 !important; box-shadow: 0 0 20px rgba(139,92,246,0.5) !important; }
.b-cyan { background: #06B6D4 !important; box-shadow: 0 0 20px rgba(6,182,214,0.5) !important; }
.b-pink { background: #F43F5E !important; box-shadow: 0 0 20px rgba(244,63,94,0.5) !important; }
.b-orange { background: #FB923C !important; box-shadow: 0 0 20px rgba(251,146,60,0.5) !important; }

/* INPUT - INI KUNCINYA: BORDER PELANGI 3 WARNA GERAK HALUS */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #8B5CF6, #06B6D4, #F43F5E, #FB923C, #8B5CF6) !important;
    background-size: 300% 100% !important;
    animation: borderFlow 3s linear infinite !important;
    padding: 2px !important; border-radius: 24px !important;
    box-shadow: 0 0 30px rgba(139,92,246,0.3) !important;
}
@keyframes borderFlow { 0%{background-position:0%} 100%{background-position:300%} }
[data-testid="stChatInput"] > div {
    background: #0F0F19 !important; border-radius: 22px !important;
}
[data-testid="stChatInput"] textarea { color: white !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #8B5CF6, #06B6D4) !important;
    border-radius: 12px !important; transition: 0.3s !important;
}
[data-testid="stChatInput"] button:hover { transform: scale(1.05); box-shadow: 0 0 20px #8B5CF6; }
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
    st.markdown("### 🎨 MASTER AI v13")
    st.markdown('<span class="badge b-purple">JUAN</span> <span class="badge b-cyan">VIBRANT</span> <span class="badge b-pink">15 TH</span> <span class="badge b-orange">MAUMERE</span>', unsafe_allow_html=True)
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Yo {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama lu siapa?", placeholder="Juan")
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
    st.write(f"{len(st.session_state.chats)} obrolan")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="👤" if m["role"]=="user" else "🎨"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'saja'}..."):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🎨"):
        ph = st.empty()
        ph.markdown("▌ _memproses..._")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"{DEVELOPER_INFO}"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v13 Vibrant. PEMBUAT KAMU {DEVELOPER_INFO}. Jangan jawab OpenAI. User: {nama}. Santai Jaksel."
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
