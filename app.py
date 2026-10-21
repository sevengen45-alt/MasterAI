import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v9.7 - Juan", page_icon="🌈", layout="wide")

# =================================================================
#  BAGIAN 1 - INI DOANG YANG GUE UBAH (TAMPILAN UI COLORFUL LIVE)
#  Lu boleh ganti warna, animasi, efek di sini sepuasnya!
# =================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

.stApp {
    background: #060611 !important;
    background-image: 
        radial-gradient(at 10% 10%, rgba(255,0,128,0.3) 0%, transparent 40%),
        radial-gradient(at 90% 20%, rgba(0,245,255,0.35) 0%, transparent 40%),
        radial-gradient(at 50% 90%, rgba(255,215,0,0.25) 0%, transparent 50%) !important;
    animation: bgMove 10s ease infinite alternate !important;
}
@keyframes bgMove { 0%{filter:hue-rotate(0deg)} 100%{filter:hue-rotate(25deg)} }

h1 {
    background: linear-gradient(90deg, #FF0000, #FF8A00, #FFD600, #00FF88, #00F5FF, #7B61FF, #FF00E5, #FF0000) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important; font-weight: 900 !important; font-size: 5rem !important;
    animation: rainbowMove 3s linear infinite !important;
}
@keyframes rainbowMove { 0%{background-position:0%} 100%{background-position:300%} }
@media (max-width: 600px) { h1 {font-size: 3rem !important;} }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20,10,40,0.95), rgba(10,20,40,0.95)) !important;
    border-right: 2px solid #7B61FF !important;
}

.stChatMessage {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(15px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
.stChatMessage p, .stChatMessage li { color: #FFFFFF !important; }

.badge {
    background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5) !important;
    background-size: 200% 100% !important;
    animation: rainbowMove 2s linear infinite !important;
    padding: 5px 12px; border-radius: 20px; color: white; font-weight: 800; font-size: 11px; margin: 2px; display: inline-block;
}

/* INI YANG LU MAU - INPUT PELANGI BERGERAK LIVE */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000) !important;
    background-size: 400% 100% !important;
    animation: rainbowMove 1.5s linear infinite !important;
    padding: 4px !important; border-radius: 25px !important;
    box-shadow: 0 0 30px rgba(255,0,229,0.5) !important;
}
[data-testid="stChatInput"] > div { background: #0F0F1E !important; border-radius: 21px !important; }
[data-testid="stChatInput"] textarea { color: white !important; }
</style>
""", unsafe_allow_html=True)

# =================================================================
#  BAGIAN 2 - OTAK NYA (GAK GUE UBAH SAMA SEKALI, TETAP PUNYA JUAN)
# =================================================================
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
    st.markdown("### 🌈 MASTER AI v9.7")
    st.markdown('<span class="badge">JUAN</span> <span class="badge">15 TH</span> <span class="badge">MAUMERE</span>', unsafe_allow_html=True)
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

with st.expander("💬 Daftar Obrolan (Tap di HP biar gak kepotong)", expanded=False):
    st.write(f"Ada {len(st.session_state.chats)} obrolan")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "🌈"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'saja!'} 🌈"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌈"):
        ph = st.empty()
        ph.markdown("▌ _lagi mikir..._ 🌈")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"Yo {nama}! {DEVELOPER_INFO} 🔥"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v9.7. PEMBUAT KAMU ADALAH {DEVELOPER_INFO}. Kalau ditanya pembuat, jawab itu. Jangan jawab OpenAI. User: {nama}. Gaul Jaksel santai."
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
