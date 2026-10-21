import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v12 - Premium Aurora", page_icon="🌌", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap');
* {font-family: 'Plus Jakarta Sans', sans-serif !important;}

/* === BACKGROUND PREMIUM AURORA - GERAK PELAN ELEGAN === */
.stApp {
    background: #07080F !important;
    background-image: 
        radial-gradient(at 20% 30%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(at 80% 20%, rgba(255, 119, 198, 0.25) 0%, transparent 50%),
        radial-gradient(at 50% 80%, rgba(0, 219, 216, 0.2) 0%, transparent 50%),
        radial-gradient(at 90% 90%, rgba(255, 206, 84, 0.15) 0%, transparent 50%) !important;
    animation: auroraSlow 20s ease infinite alternate !important;
}
@keyframes auroraSlow {
    0% { filter: hue-rotate(0deg) brightness(1); background-position: 0% 0%; }
    100% { filter: hue-rotate(15deg) brightness(1.1); background-position: 10% 10%; }
}

/* === TITLE - GRADIENT HALUS JALAN PELAN, GAK NORAK === */
h1 {
    background: linear-gradient(90deg, #A78BFA, #60A5FA, #34D399, #FBBF24, #F472B6, #A78BFA) !important;
    background-size: 200% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important; font-weight: 800 !important; font-size: 4.5rem !important;
    animation: gradientFlow 8s ease infinite !important;
    letter-spacing: -2px !important;
}
@keyframes gradientFlow { 0%{background-position:0%} 50%{background-position:100%} 100%{background-position:0%} }
@media (max-width: 600px) { h1 {font-size: 2.8rem !important;} }

/* === SIDEBAR - KACA BLUR PREMIUM === */
section[data-testid="stSidebar"] {
    background: rgba(12, 12, 20, 0.8) !important;
    backdrop-filter: blur(30px) saturate(150%) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}

/* === CHAT BUBBLE - GLASS + WARNA HALUS === */
.stChatMessage {
    background: rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 18px !important;
    transition: all 0.4s ease !important;
}
.stChatMessage:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(167,139,250,0.3) !important;
    transform: translateY(-1px);
}
.stChatMessage p { color: rgba(255,255,255,0.92) !important; font-size: 15.5px !important; line-height: 1.6 !important; }

/* === BADGE - PASTEL ELEGAN, GERAK PELAN === */
.badge {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    padding: 5px 12px; border-radius: 100px; color: rgba(255,255,255,0.9);
    font-size: 10px; font-weight: 700; letter-spacing: 0.5px; margin: 3px; display: inline-block;
}
.badge-premium {
    background: linear-gradient(90deg, rgba(167,139,250,0.2), rgba(96,165,250,0.2)) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    animation: softGlow 3s ease infinite alternate !important;
}
@keyframes softGlow { 0%{box-shadow:0 0 10px rgba(167,139,250,0.2)} 100%{box-shadow:0 0 20px rgba(96,165,250,0.3)} }

/* === INPUT - BORDER PELANGI HALUS, GAK NORAK === */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #A78BFA, #60A5FA, #34D399, #FBBF24, #F472B6) !important;
    background-size: 300% 100% !important;
    animation: gradientFlow 6s ease infinite !important;
    padding: 1.5px !important; border-radius: 20px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.05) inset !important;
}
[data-testid="stChatInput"] > div {
    background: rgba(15, 15, 25, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 18.5px !important;
}
[data-testid="stChatInput"] textarea { color: white !important; }
[data-testid="stChatInput"] button {
    background: rgba(255,255,255,0.1) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stChatInput"] button:hover {
    background: linear-gradient(90deg, #A78BFA, #60A5FA) !important;
    transform: scale(1.05);
}
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
    st.markdown("### 🌌 MASTER AI v12")
    st.markdown('<span class="badge badge-premium">PREMIUM</span> <span class="badge">JUAN • 15</span> <span class="badge">MAUMERE</span>', unsafe_allow_html=True)
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Yo {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama lu siapa?", placeholder="Juan")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()
    st.markdown("### 💬 Obrolan")
    if st.button("➕ Obrolan Baru", use_container_width=True):
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
st.title(active["title"])

with st.expander("💬 Obrolan (HP)", expanded=False):
    st.write(f"{len(st.session_state.chats)} obrolan")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="👤" if m["role"]=="user" else "✨"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'saja'}..."):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="✨"):
        ph = st.empty()
        ph.markdown("▌ _sedang berpikir..._")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"{DEVELOPER_INFO}"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v12 Premium. PEMBUAT KAMU {DEVELOPER_INFO}. Jangan jawab OpenAI. User: {nama}. Bahasa santai Jaksel tapi elegan."
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
