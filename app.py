import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v11.1 - Gemini Alive", page_icon="🌈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@500;700&display=swap');

* { font-family: 'Google Sans', Inter, sans-serif !important; }

/* PUTIH + 4 ORB PELANGI YANG BERGERAK HALUS */
.stApp {
    background: #FFFFFF !important;
}
.stApp::before {
    content: ""; position: fixed; inset: -40%;
    background: 
        radial-gradient(ellipse 700px 600px at 15% 10%, rgba(66,133,244,0.14) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 85% 15%, rgba(219,68,55,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 800px 600px at 50% 115%, rgba(15,157,88,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 20% 90%, rgba(244,180,0,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 90% 85%, rgba(156,39,176,0.10) 0%, transparent 60%);
    animation: orbAlive 16s ease-in-out infinite alternate;
    filter: blur(18px); z-index: 0; pointer-events: none;
}
@keyframes orbAlive {
    0% { transform: translate(0,0) scale(1) rotate(0deg); }
    50% { transform: translate(-3%, 3%) scale(1.08) rotate(1deg); }
    100% { transform: translate(3%, -2%) scale(1.02) rotate(-1deg); }
}
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; background: transparent !important; }

p, div, span { color: #202124 !important; }

/* JUDUL - PELANGI ALIVE SUPER HIDUP */
h1 { text-align: center !important; font-weight: 500 !important; font-size: 3.4rem !important; line-height: 1.05 !important; color: #202124 !important; -webkit-text-fill-color: #202124 !important; }
h1 .rainbow-alive {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: rainbowRun 2.5s linear infinite, floatAlive 3s ease-in-out infinite alternate !important;
    font-weight: 700 !important; display: inline-block;
    filter: drop-shadow(0 2px 12px rgba(66,133,244,0.25));
}
@keyframes rainbowRun { 0%{background-position:0% 50%} 100%{background-position:300% 50%} }
@keyframes floatAlive { 0%{transform: translateY(0)} 100%{transform: translateY(-6px)} }

.gemini-line {
    width: 120px; height: 4px; margin: 18px auto 0 auto;
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4);
    background-size: 300% 100%; animation: rainbowRun 2s linear infinite;
    border-radius: 100px; box-shadow: 0 2px 10px rgba(66,133,244,0.3);
}

/* SIDEBAR PUTIH */
section[data-testid="stSidebar"] { background: #F8F9FA !important; border-right: 1px solid #E8EAED !important; }
section[data-testid="stSidebar"] * { color: #202124 !important; }

/* BADGE PELANGI ALIVE */
.badge-alive {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 300% 100% !important; animation: rainbowRun 2s linear infinite, badgeFloat 2.5s ease-in-out infinite alternate !important;
    color: white !important; padding: 6px 14px; border-radius: 100px; font-size: 11px; font-weight: 700;
    display: inline-block; margin: 3px; box-shadow: 0 2px 10px rgba(66,133,244,0.3);
}
@keyframes badgeFloat { 0%{transform: translateY(0)} 100%{transform: translateY(-3px)} }

/* CHAT BUBBLE PUTIH + GARIS PELANGI ALIVE DI BAWAH */
.stChatMessage {
    background: #FFFFFF !important; border: 1px solid #E8EAED !important;
    border-radius: 22px !important; box-shadow: 0 1px 8px rgba(0,0,0,0.04) !important;
    max-width: 720px !important; margin: 14px auto !important;
    position: relative; overflow: hidden; animation: popAlive 0.5s cubic-bezier(0.16,1,0.3,1) !important;
}
@keyframes popAlive { 0%{opacity:0; transform: translateY(10px) scale(0.98)} 100%{opacity:1; transform: translateY(0) scale(1)} }
.stChatMessage::after {
    content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 3px;
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4);
    background-size: 300% 100%; animation: rainbowRun 2s linear infinite;
    opacity: 0; transition: opacity 0.3s;
}
.stChatMessage:hover { border-color: #DADCE0 !important; box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important; transform: translateY(-1px); }
.stChatMessage:hover::after { opacity: 1; }
.stChatMessage p { color: #202124 !important; font-size: 15.5px !important; line-height: 1.65 !important; }

/* INPUT - PUTIH TAPI BORDER PELANGI ALIVE PALING HIDUP */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 400% 100% !important;
    animation: rainbowRun 2s linear infinite, inputAlive 2.5s ease-in-out infinite !important;
    padding: 2.5px !important; border-radius: 30px !important;
    box-shadow: 0 2px 16px rgba(66,133,244,0.18) !important;
    max-width: 740px !important; margin: 0 auto !important;
}
@keyframes inputAlive {
    0%,100% { box-shadow: 0 2px 16px rgba(66,133,244,0.18); transform: scale(1); }
    50% { box-shadow: 0 6px 28px rgba(66,133,244,0.28), 0 0 20px rgba(219,68,55,0.15); transform: scale(1.01); }
}
[data-testid="stChatInput"] > div {
    background: #FFFFFF !important; border-radius: 28px !important; border: none !important;
}
[data-testid="stChatInput"] textarea { color: #202124 !important; -webkit-text-fill-color: #202124 !important; font-size: 16px !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #80868B !important; -webkit-text-fill-color: #80868B !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437) !important;
    background-size: 200% 100% !important; animation: rainbowRun 2s linear infinite !important;
    border-radius: 50% !important; width: 36px !important; height: 36px !important;
    color: white !important; box-shadow: 0 2px 10px rgba(66,133,244,0.4) !important;
}
[data-testid="stChatInput"] button:hover { transform: scale(1.08) !important; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Memulai Obrolan?", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("###  MasterAI")
    st.markdown('<span class="badge-alive">ALIVE</span> <span class="badge-alive">GEMINI</span> <span class="badge-alive">WHITE</span>', unsafe_allow_html=True)
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Hai {st.session_state.user_memory['nama']}!")
    else:
        nama = st.text_input("Nama kamu?", placeholder="Nama kamu")
        if nama:
            st.session_state.user_memory["nama"] = nama
            st.rerun()
    st.markdown("### 💬 Obrolan")
    if st.button("➕ Obrolan baru", use_container_width=True):
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

if len(active["messages"]) == 0:
    st.markdown("""
    <div style="text-align:center; padding: 50px 20px 10px 20px; max-width:720px; margin:0 auto;">
        <h1>Siap Memulai<br><span class="rainbow-alive">Obrolan?</span></h1>
        <div class="gemini-line"></div>
        <p style="color:#5F6368 !important; font-size:16px; margin-top:20px;">Tanya apa saja, saya siap membantu ✨</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='text-align:center; color:#202124;'>{active['title']}</h2>", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑" if m["role"]=="user" else "🌈"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya {st.session_state.user_memory['nama'] or 'apa saja'} ✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌈"):
        ph = st.empty()
        ph.markdown("🌈 _Thinking alive..._")
        try:
            nama = st.session_state.user_memory["nama"] or "teman"
            msgs = [{"role": "system", "content": f"Kamu MasterAI v11.1 Gemini Alive White. User {nama}. Ramah, jelas."}] + active["messages"]
            res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=msgs, temperature=0.8, max_tokens=1500)
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
