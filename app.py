import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v9.3 - FIX RAINBOW", page_icon="🧠", layout="wide")

# ===== CSS LU + TAMBAHAN RAINBOW LIVE (TANPA NGUBAH OTAK) =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

.stApp {
    background: radial-gradient(ellipse at top, #0f0f23 0%, #09090b 50%, #000000 100%);
    background-attachment: fixed;
}

/* JUMBO TITLE - TETAP KAYAK PUNYA LU */
h1 {
    background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5, #FF8A00) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 5.5rem !important;
    line-height: 1.0 !important;
    margin-top: 3rem !important;
    margin-bottom: 2rem !important;
    filter: drop-shadow(0 0 30px rgba(123,97,255,0.8)) !important;
    background-size: 200% 200% !important;
    animation: titleMove 3s ease infinite !important;
}
@keyframes titleMove { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }

@media (max-width: 600px) {
    h1 {font-size: 3.5rem !important;}
}

/* FIX UTAMA - WARNA TEKS JAWABAN JADI PUTIH TERANG (PUNYA LU) */
.stChatMessage p,
.stChatMessage li,
.stChatMessage span,
.stChatMessage div,
.stMarkdown p,
.stMarkdown li {
    color: #FFFFFF !important;
    opacity: 1 !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
}
.stChatMessage h1, .stChatMessage h2, .stChatMessage h3 {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background: none !important;
}
.stChatMessage h2 { color: #00F5FF !important; -webkit-text-fill-color: #00F5FF !important; }
.stChatMessage strong, .stChatMessage b { color: #FFFFFF !important; font-weight: 800 !important; }
.stChatMessage table { color: white !important; }
.stChatMessage th { background: rgba(123,97,255,0.3) !important; color: white !important; }
.stChatMessage td { color: #E0E0E0 !important; border-color: rgba(255,255,255,0.2) !important; }
.stChatMessage {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(123,97,255,0.25) !important;
    border-radius: 20px !important;
}
.badge {
    background: linear-gradient(90deg, #00F5FF, #7B61FF);
    padding: 4px 10px; border-radius: 20px; color: white;
    font-size: 10px; font-weight: 600; display: inline-block; margin: 2px;
}

/* === TAMBAHAN GUE: TABEL TANYA JADI RAINBOW LIVE GERAK === */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000) !important;
    background-size: 300% 100% !important;
    animation: rainbowLive 2s linear infinite !important;
    padding: 3px !important;
    border-radius: 20px !important;
    border: none !important;
    box-shadow: 0 0 25px rgba(123,97,255,0.6), 0 0 40px rgba(0,245,255,0.3) !important;
}
@keyframes rainbowLive {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}
[data-testid="stChatInput"] > div {
    background: #141423 !important;
    border-radius: 17px !important;
    border: none !important;
}
[data-testid="stChatInput"] textarea {
    color: white !important;
    background: transparent !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #00F5FF, #7B61FF) !important;
    border-radius: 12px !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ===== OTAK AI - TETAP SAMA, GAK GUE UBAH! (GROQ + GPT-OSS-120B) =====
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None, "topik": []}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Memulai Obrolan!", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active():
    return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### 🧠 MASTER AI v9.3")
    st.markdown('<span class="badge">PUTIH TERANG</span> <span class="badge">ANTI GELAP</span> <span class="badge">🌈 RAINBOW LIVE</span>', unsafe_allow_html=True)
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
        if st.button(f"{chat['title'][:30]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.title(active["title"])

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "👨🏼‍💻"):
        st.markdown(m["content"])

# ===== CHAT INPUT - TETAP PAKE OTAK ASLI =====
if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'saja!'} 🌈"):
    if len(active["messages"]) == 0:
        active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="👨🏼‍💻"):
        ph = st.empty()
        ph.markdown("▌ _lagi mikir..._ 🧠")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            system_prompt = f"Kamu MasterAI v9.3. Nama user {nama}. WAJIB Bahasa Indonesia gaul Jaksel, santai, kocak. Jawab jelas. Kalau ada soal matematika kayak 2^4 x 2^10, jelasin pake rumus eksponen dan hitung hasilnya bener."
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
            ph.error(f"Error: {e} - Cek GROQ_API_KEY di secrets!")
