import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v15 - Rainbow Elegan", page_icon="🌈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

/* ===== BACKGROUND RAINBOW - 5 WARNA TAPI KALEM, DIEM ===== */
.stApp {
    background: #08080A !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(255,0,85,0.25) 0%, transparent 55%),
        radial-gradient(at 100% 0%, rgba(255,171,0,0.2) 0%, transparent 55%),
        radial-gradient(at 50% 50%, rgba(0,230,118,0.12) 0%, transparent 60%),
        radial-gradient(at 0% 100%, rgba(41,121,255,0.25) 0%, transparent 55%),
        radial-gradient(at 100% 100%, rgba(170,0,255,0.25) 0%, transparent 55%) !important;
    background-size: 120% 120% !important;
    animation: rainbowBgSlow 20s ease infinite alternate !important;
}
@keyframes rainbowBgSlow {
    0% { background-position: 0% 0%, 100% 0%, 50% 50%, 0% 100%, 100% 100%; filter: brightness(1) hue-rotate(0deg); }
    100% { background-position: 10% 10%, 90% 10%, 55% 60%, 10% 90%, 90% 90%; filter: brightness(1.1) hue-rotate(15deg); }
}

/* ===== JUDUL - RAINBOW 5 WARNA JALAN PELAN 5 DETIK, DIEM ===== */
.live-rainbow-title {
    background: linear-gradient(90deg, #FF0055, #FFAB00, #00E676, #2979FF, #AA00FF, #FF0055) !important;
    background-size: 400% 100% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 4.8rem !important;
    letter-spacing: -0.04em !important;
    animation: rainbowTitleSlow 5s linear infinite !important;
    filter: drop-shadow(0 0 20px rgba(170,0,255,0.3)) !important;
    display: block !important;
    padding: 15px 0 !important;
}
@keyframes rainbowTitleSlow { 
    0% { background-position: 0% 50%; } 
    100% { background-position: 400% 50%; } 
}
@media (max-width: 600px) { .live-rainbow-title { font-size: 2.8rem !important; } }

/* ===== SIDEBAR - DARK GLASS ===== */
section[data-testid="stSidebar"] {
    background: rgba(12,12,14,0.9) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 2px solid rgba(170,0,255,0.15) !important;
}

/* ===== CHAT - DIEM ===== */
.stChatMessage {
    background: rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-left: 3px solid #AA00FF !important;
}
.stChatMessage p { color: #F8F8FF !important; font-size: 15.5px !important; }

/* ===== BADGE - RAINBOW JALAN PELAN, DIEM ===== */
.badge {
    padding: 6px 14px; border-radius: 20px; color: white; font-weight: 800; font-size: 11px; margin: 3px; display: inline-block;
    background-size: 300% 100% !important;
    animation: rainbowTitleSlow 4s linear infinite !important;
}
.b-1 { background: linear-gradient(90deg, #FF0055, #FFAB00) !important; }
.b-2 { background: linear-gradient(90deg, #00E676, #2979FF) !important; }
.b-3 { background: linear-gradient(90deg, #2979FF, #AA00FF) !important; }

/* ===== TASKBAR - RAINBOW 5 WARNA LIVE JALAN 3 DETIK, DIEM GAK GOYANG ===== */
div[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0055, #FFAB00, #00E676, #2979FF, #AA00FF, #FF0055) !important;
    background-size: 500% 100% !important;
    animation: rainbowTitleSlow 3s linear infinite !important;
    padding: 3px !important;
    border-radius: 28px !important;
    box-shadow: 0 0 20px rgba(170,0,255,0.35), 0 0 45px rgba(41,121,255,0.15) !important;
}
div[data-testid="stChatInput"] > div {
    background: #121214 !important;
    border-radius: 25px !important;
}
div[data-testid="stChatInput"] textarea { color: white !important; font-weight: 600 !important; }
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #FF0055, #AA00FF) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ===== OTAK TETAP PUNYA JUAN =====
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
    st.markdown("### 🌈 MASTER AI RAINBOW")
    st.markdown('<span class="badge b-1">RAINBOW</span> <span class="badge b-2">LIVE</span> <span class="badge b-3">JUAN</span>', unsafe_allow_html=True)
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
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.divider()
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True):
        if st.button(f"{chat['title'][:28]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.markdown(f"<h1 class='live-rainbow-title'>{active['title']}</h1>", unsafe_allow_html=True)

with st.expander("💬 Daftar Obrolan (HP Tap Sini)", expanded=False):
    st.write(f"Ada {len(st.session_state.chats)} obrolan")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "🌈"):
        st.markdown(m["content"])

if prompt := st.chat_input("Tanya apa saja! 👨🏼‍💻✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌈"):
        ph = st.empty()
        ph.markdown("▌ _lagi mikir..._ 🌈")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"Yo {nama}! {DEVELOPER_INFO} 🌈"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v15 Rainbow Elegan. PEMBUAT KAMU ADALAH {DEVELOPER_INFO}. User: {nama}. Santai Jaksel."
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
