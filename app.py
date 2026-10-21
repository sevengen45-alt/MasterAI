import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v14 - Ocean Breeze", page_icon="🌊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

/* ===== BACKGROUND OCEAN - BIRU TOSKA UNGU JALAN PELAN ===== */
.stApp {
    background: #050A14 !important;
    background-image: 
        radial-gradient(at 10% 20%, rgba(0,219,216,0.35) 0%, transparent 50%),
        radial-gradient(at 90% 10%, rgba(0,119,182,0.4) 0%, transparent 50%),
        radial-gradient(at 50% 80%, rgba(0,150,199,0.25) 0%, transparent 50%),
        radial-gradient(at 20% 90%, rgba(123,97,255,0.3) 0%, transparent 50%),
        radial-gradient(at 85% 85%, rgba(0,219,216,0.2) 0%, transparent 40%) !important;
    background-size: 120% 120% !important;
    animation: oceanMove 18s ease infinite alternate !important;
}
@keyframes oceanMove {
    0% { background-position: 0% 0%, 100% 0%, 50% 100%, 0% 100%, 100% 100%; filter: brightness(1); }
    100% { background-position: 15% 25%, 85% 15%, 60% 85%, 10% 85%, 90% 90%; filter: brightness(1.15); }
}

/* ===== JUDUL - OCEAN GRADIENT BIRU TOSKA UNGU JALAN LIVE ===== */
.live-rainbow-title {
    background: linear-gradient(90deg, #00DBD8, #0096C7, #0077B6, #7B61FF, #00DBD8) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 4.8rem !important;
    letter-spacing: -0.03em !important;
    animation: oceanTitleFlow 4s ease infinite !important;
    filter: drop-shadow(0 0 20px rgba(0,219,216,0.3)) !important;
    display: block !important;
    padding: 15px 0 !important;
}
@keyframes oceanTitleFlow { 
    0% { background-position: 0% 50%; } 
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; } 
}
@media (max-width: 600px) { .live-rainbow-title { font-size: 2.8rem !important; } }

/* ===== SIDEBAR - DARK BLUE GLASS ===== */
section[data-testid="stSidebar"] {
    background: rgba(5,10,20,0.9) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 2px solid rgba(0,219,216,0.2) !important;
}

/* ===== CHAT BUBBLE - DIEM, BORDER OCEAN ===== */
.stChatMessage {
    background: rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 18px !important;
    border: 1px solid rgba(0,219,216,0.15) !important;
    border-left: 3px solid #00DBD8 !important;
}
.stChatMessage p { color: #F0F9FF !important; font-size: 15.5px !important; line-height: 1.6 !important; }

/* ===== BADGE - OCEAN SOLID + GLOW ===== */
.badge {
    padding: 6px 14px; border-radius: 20px; color: white; font-weight: 800; font-size: 11px; margin: 3px; display: inline-block;
}
.b-ocean-1 { background: linear-gradient(90deg, #00DBD8, #0096C7) !important; box-shadow: 0 0 15px rgba(0,219,216,0.4) !important; }
.b-ocean-2 { background: linear-gradient(90deg, #0077B6, #7B61FF) !important; box-shadow: 0 0 15px rgba(0,119,182,0.4) !important; }
.b-ocean-3 { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(0,219,216,0.2) !important; }

/* ===== TASKBAR - BORDER OCEAN PELANGI BIRU TOSKA UNGU LIVE ===== */
div[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #00DBD8, #0096C7, #0077B6, #7B61FF, #00DBD8) !important;
    background-size: 400% 100% !important;
    animation: oceanBorderFlow 2.5s linear infinite !important;
    padding: 3px !important;
    border-radius: 28px !important;
    box-shadow: 0 0 25px rgba(0,219,216,0.4), 0 0 50px rgba(123,97,255,0.15) !important;
}
@keyframes oceanBorderFlow { 0%{background-position:0%} 100%{background-position:400%} }
div[data-testid="stChatInput"] > div {
    background: #080E1C !important;
    border-radius: 25px !important;
}
div[data-testid="stChatInput"] textarea { color: white !important; font-weight: 600 !important; }
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #00DBD8, #7B61FF) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ===== OTAK TETAP PUNYA JUAN - GAK DIUBAH =====
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
    st.markdown("### MasterAI")
    st.markdown('<span class="badge b-ocean-1">OCEAN</span> <span class="badge b-ocean-2">JUAN</span> <span class="badge b-ocean-3">LIVE</span>', unsafe_allow_html=True)
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
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "🌊"):
        st.markdown(m["content"])

if prompt := st.chat_input("Tanya apa saja! 👨🏼‍💻✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🇮🇩"):
        ph = st.empty()
        ph.markdown("▌ _Thinking!⚡")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"Yo {nama}! {DEVELOPER_INFO} 🌊"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v14 Ocean. PEMBUAT KAMU ADALAH {DEVELOPER_INFO}. User: {nama}. Bahasa santai Jaksel."
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
