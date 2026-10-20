import streamlit as st
from groq import Groq
import time
from datetime import datetime
import uuid

st.set_page_config(page_title="MasterAI", page_icon="👨🏼‍💻", layout="wide")

st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at 20% 30%, #1a1a2e 0%, #0f0f1e 40%, #000000 100%); }
    h1 { font-weight: 800 !important; background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-size: 3rem !important; }
    .stChatMessage { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; backdrop-filter: blur(10px); border-radius: 20px !important; }
    div[data-testid="stChatInput"] { background: rgba(255,255,255,0.08) !important; border-radius: 30px !important; border: 1px solid rgba(255,255,255,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# ===== INIT CLIENT =====
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key belum ada di Secrets!")
    st.stop()

# ===== INIT MULTI CHAT SYSTEM =====
if "chats" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.chats = {
        first_id: {"title": "Obrolan Baru ✨", "messages": [{"role": "assistant", "content": "Yo bang! MasterAI v4.0 siap! Sekarang bisa bikin banyak obrolan tanpa batas! 😎👨🏼‍💻"}], "created": datetime.now().strftime("%d %b")}
    }
    st.session_state.active_chat = first_id

# ===== SIDEBAR - LIST CHAT =====
with st.sidebar:
    st.markdown("## 👨🏼‍💻 MasterAI v4.0")
    
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {"title": f"Obrolan Baru {len(st.session_state.chats)+1}", "messages": [{"role": "assistant", "content": "Obrolan baru dimulai bang! Mau bahas apa? 🗿🔥"}], "created": datetime.now().strftime("%d %b")}
        st.session_state.active_chat = new_id
        st.rerun()

    st.markdown("---")
    st.markdown("### 💬 Daftar Obrolan")
    
    # Tampilkan semua chat dari terbaru
    for chat_id in reversed(list(st.session_state.chats.keys())):
        chat = st.session_state.chats[chat_id]
        is_active = chat_id == st.session_state.active_chat
        label = f"{'👉 ' if is_active else '💭 '}{chat['title'][:25]}"
        if st.button(label, key=chat_id, use_container_width=True, type="secondary" if is_active else "primary"):
            st.session_state.active_chat = chat_id
            st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Hapus", use_container_width=True):
            if len(st.session_state.chats) > 1:
                del st.session_state.chats[st.session_state.active_chat]
                st.session_state.active_chat = list(st.session_state.chats.keys())[-1]
                st.rerun()
    with col2:
        if st.button("🧹 Hapus Semua", use_container_width=True):
            st.session_state.chats.clear()
            st.rerun()

    st.caption(f"Total: {len(st.session_state.chats)} obrolan")

# ===== MAIN CHAT AREA =====
active = st.session_state.chats[st.session_state.active_chat]
st.title(active["title"])
st.caption(f"MasterAI v4.0 • {len(active['messages'])} pesan • {active['created']}")

# Tampilkan chat aktif
for msg in active["messages"]:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"]=="user" else "🤖"):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ketik di sini bang..."):
    # Auto rename judul dari pesan pertama
    if len(active["messages"]) == 1:
        active["title"] = prompt[:30] + ("..." if len(prompt)>30 else "")
    
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        try:
            completion = client.chat.completions.create(
                messages=[{"role": m["role"], "content": m["content"]} for m in active["messages"]],
                model="openai/gpt-oss-20b",
            )
            response = completion.choices[0].message.content
            placeholder = st.empty()
            full = ""
            for c in response:
                full += c
                placeholder.markdown(full + "▌")
                time.sleep(0.004)
            placeholder.markdown(full)
            active["messages"].append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
