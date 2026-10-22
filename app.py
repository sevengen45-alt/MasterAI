import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v11 - Gemini White", page_icon="✨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* { font-family: 'Google Sans', 'Inter', -apple-system, sans-serif !important; }

/* BACKGROUND PUTIH BERSIH + GRADIENT HALUS KAYAK GEMINI */
.stApp {
    background: #FFFFFF !important;
    background-image: 
        radial-gradient(ellipse 800px 600px at 10% -10%, rgba(66,133,244,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 90% 0%, rgba(234,67,53,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 700px 600px at 50% 120%, rgba(52,168,83,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 20% 100%, rgba(251,188,4,0.08) 0%, transparent 60%) !important;
}
[data-testid="stAppViewContainer"] { background: transparent !important; }
p, div, span, li { color: #1F1F !important; }

/* JUDUL - PUTIH + PELANGI GEMINI */
h1 {
    font-family: 'Google Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 3.2rem !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
    text-align: center !important;
    color: #1F1F1F !important;
    -webkit-text-fill-color: #1F1F1F !important;
}
h1 span.gemini {
    background: linear-gradient(90deg, #4285F4 0%, #9C27B0 25%, #DB4437 50%, #F4B400 75%, #0F9D58 100%) !important;
    background-size: 200% 100% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: geminiFlow 4s linear infinite !important;
    font-weight: 700 !important;
}
@keyframes geminiFlow { 0%{background-position:0% 50%} 100%{background-position:200% 50%} }

/* SIDEBAR - PUTIH + BORDER HALUS */
section[data-testid="stSidebar"] {
    background: #F8F9FA !important;
    border-right: 1px solid #E8EAED !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] * { color: #1F1F1F !important; }
section[data-testid="stSidebar"] .stButton button {
    background: #FFFFFF !important; border: 1px solid #E8EAED !important;
    border-radius: 12px !important; color: #1F1F1F !important;
    font-weight: 500 !important; transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: #F1F3F4 !important; border-color: #DADCE0 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}

/* BADGE - GEMINI STYLE */
.badge {
    background: #FFFFFF !important; border: 1px solid #E8EAED !important;
    padding: 6px 14px; border-radius: 100px; color: #5F6368 !important;
    font-size: 11px; font-weight: 600; display: inline-block; margin: 3px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.badge.rainbow {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58) !important;
    background-size: 200% 100% !important; animation: geminiFlow 3s linear infinite !important;
    color: white !important; border: none !important;
    box-shadow: 0 2px 8px rgba(66,133,244,0.25);
}

/* CHAT BUBBLE - PUTIH BERSIH KAYAK GEMINI */
.stChatMessage {
    background: #FFFFFF !important;
    border: 1px solid #E8EAED !important;
    border-radius: 20px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04) !important;
    max-width: 720px !important; margin: 12px auto !important;
    animation: msgIn 0.4s cubic-bezier(0.16,1,0.3,1) !important;
    position: relative; overflow: hidden;
}
@keyframes msgIn { 0%{opacity:0; transform: translateY(8px)} 100%{opacity:1; transform: translateY(0)} }
.stChatMessage:hover {
    border-color: #DADCE0 !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
}
.stChatMessage[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background: #F8F9FA !important; border-color: #F1F3F4 !important;
}
/* AURA PELANGI TIPIS SAAT HOVER */
.stChatMessage::after {
    content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 2px;
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58);
    background-size: 200% 100%; animation: geminiFlow 3s linear infinite;
    opacity: 0; transition: opacity 0.3s;
}
.stChatMessage:hover::after { opacity: 1; }

.stChatMessage p { color: #1F1F1F !important; font-size: 15.5px !important; line-height: 1.65 !important; font-weight: 400 !important; }
.stChatMessage strong { color: #1A73E8 !important; }

/* INPUT - GEMINI STYLE PUTIH + BORDER PELANGI SAAT FOKUS */
[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 1.5px solid #E8EAED !important;
    border-radius: 28px !important;
    padding: 4px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    max-width: 720px !important; margin: 0 auto !important;
    transition: all 0.25s cubic-bezier(0.16,1,0.3,1) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: transparent !important;
    background: linear-gradient(white, white) padding-box, linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58) border-box !important;
    background-size: 200% 100% !important;
    animation: geminiFlow 3s linear infinite !important;
    box-shadow: 0 4px 20px rgba(66,133,244,0.15), 0 0 0 4px rgba(66,133,244,0.08) !important;
    transform: translateY(-1px);
}
[data-testid="stChatInput"] > div { background: transparent !important; border: none !important; }
[data-testid="stChatInput"] textarea {
    color: #1F1F1F !important; font-size: 16px !important; font-weight: 400 !important;
    -webkit-text-fill-color: #1F1F1F !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #80868B !important; -webkit-text-fill-color: #80868B !important;
}
[data-testid="stChatInput"] button {
    background: #1F1F1F !important; color: white !important;
    border-radius: 50% !important; width: 36px !important; height: 36px !important;
    font-weight: 700 !important; transition: all 0.2s !important;
}
[data-testid="stChatInput"] button:hover {
    background: #000 !important; transform: scale(1.05) !important;
}

/* SCROLLBAR HALUS */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: #DADCE0; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #BDC1C6; }
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
    st.markdown("### ✨ MasterAI")
    st.markdown('<span class="badge rainbow">GEMINI</span> <span class="badge">WHITE</span> <span class="badge">CLEAN</span>', unsafe_allow_html=True)
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Hai {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama kamu?", placeholder="Nama kamu")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()
    st.markdown("### 💬 Obrolan")
    if st.button("➕ Obrolan baru", use_container_width=True):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.divider()
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True):
        if st.button(f"{chat['title'][:30]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()

# JUDUL GEMINI STYLE
if len(active["messages"]) == 0:
    st.markdown(f"""
    <div style="text-align:center; padding: 40px 20px 20px 20px; max-width:720px; margin:0 auto;">
        <h1 style="margin-bottom:8px;">Siap Memulai<br><span class="gemini">Obrolan?</span></h1>
        <p style="color:#5F6368 !important; font-size:16px; margin-top:16px;">Tanya apa saja, saya siap membantu ✨</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='font-size:2rem !important; margin-bottom:20px;'>{active['title']}</h1>", unsafe_allow_html=True)

with st.expander("💬 Daftar Obrolan", expanded=False):
    st.write(f"Ada {len(st.session_state.chats)} obrolan")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑" if m["role"]=="user" else "✨"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya {st.session_state.user_memory['nama'] or 'apa saja'} ✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="✨"):
        ph = st.empty()
        ph.markdown("✨ _Sedang berpikir..._")
        try:
            nama = st.session_state.user_memory["nama"] or "teman"
            system_prompt = f"Kamu MasterAI v11 Gemini White. Nama user {nama}. Jawab ramah, jelas, membantu, bahasa Indonesia santai."
            messages = [{"role": "system", "content": system_prompt}] + active["messages"]
            res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.8, max_tokens=1500)
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
