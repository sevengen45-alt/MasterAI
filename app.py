import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v9.2", page_icon="🧠", layout="wide")

# ===== CSS JUMBO TITLE + EFEK =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

.stApp {
    background: radial-gradient(ellipse at top, #0f0f23 0%, #09090b 50%, #000000 100%);
    background-attachment: fixed;
}

/* TULISAN OBROLAN PERTAMA JUMBO */
h1 {
    background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5, #FF8A00) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 5.5rem !important;
    line-height: 1.0 !important;
    letter-spacing: -3px !important;
    margin-top: 4rem !important;
    margin-bottom: 4rem !important;
    filter: drop-shadow(0 0 30px rgba(123,97,255,0.8)) !important;
    animation: pulse 2.5s ease-in-out infinite alternate;
}

@keyframes pulse {
    from {transform: scale(1); filter: drop-shadow(0 0 20px rgba(123,97,255,0.6));}
    to {transform: scale(1.03); filter: drop-shadow(0 0 45px rgba(255,0,229,0.9));}
}

.stChatMessage {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(123,97,255,0.2) !important;
    border-radius: 24px !important;
    padding: 1rem !important;
}

.badge {
    background: linear-gradient(90deg, #00F5FF, #7B61FF);
    padding: 4px 10px; 
    border-radius: 20px; 
    color: white;
    font-size: 10px; 
    font-weight: 600; 
    display: inline-block; 
    margin: 2px;
}

/* Responsive HP - biar gak kepotong */
@media (max-width: 600px) {
    h1 {font-size: 3.8rem !important; margin-top: 2rem !important;}
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ===== MEMORY & CHATS =====
if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None, "topik": []}

if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {
        fid: {"title": "Siap Memulai Obrolan!", "messages": [], "created": time.time()}
    }
    st.session_state.active_chat = fid

def get_active():
    return st.session_state.chats[st.session_state.active_chat]

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 🧠 MASTER AI v9.2")
    st.markdown('<span class="badge">CHAT ONLY</span> <span class="badge">JUMBO TITLE</span>', unsafe_allow_html=True)
    st.divider()
    
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Yo {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama lu siapa bang? 🧠", placeholder="contoh: Bintang")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()

    st.markdown("### 💬 Obrolan-obrolan")
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {
            "title": f"Chat {len(st.session_state.chats)+1} ✨", 
            "messages": [], 
            "created": time.time()
        }
        st.session_state.active_chat = nid
        st.rerun()
    
    st.divider()
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True):
        is_active = cid == st.session_state.active_chat
        if st.button(f"{'🔥 ' if is_active else '💤 '}{chat['title']}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

    st.divider()
    if st.button("🧠 Reset Memory", use_container_width=True):
        st.session_state.user_memory = {"nama": None, "topik": []}
        st.rerun()

# ===== MAIN - HANYA TULISAN BESAR + CHAT =====
active = get_active()

# INI KUNCINYA - HANYA TITLE JUMBO, TANPA BAGAN BESAR
st.title(active["title"])

# RENDER CHAT HISTORY (kalau kosong, ya kosong aja - gak ada welcome card)
for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "👨🏼‍💻"):
        st.markdown(m["content"])

# ===== INPUT =====
if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'bang'}... 🗿"):
    # Simpen memory
    if len(prompt.split()) > 1:
        st.session_state.user_memory["topik"].append(prompt[:50])
        st.session_state.user_memory["topik"] = st.session_state.user_memory["topik"][-5:]

    # Update judul kalau masih obrolan pertama
    if len(active["messages"]) == 0:
        active["title"] = prompt[:35] + ("..." if len(prompt)>35 else "")

    active["messages"].append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👨🏼‍💻"):
        placeholder = st.empty()
        placeholder.markdown("▌ _lagi mikir..._ 🧠💭")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            topik = ", ".join(st.session_state.user_memory["topik"][-2:]) if st.session_state.user_memory["topik"] else "belum ada"
            
            system_prompt = f"""
            Kamu MasterAI v9.2, AI gaul Indonesia.
            Nama user: {nama}, topik terakhir: {topik}
            WAJIB: Bahasa Indonesia gaul Jaksel, slang, santai, kocak, pakai emoji 🗿🔥💀 secukupnya.
            Panggil user {nama}. Jangan kaku. Jawab pinter tapi gaul.
            """

            messages = [{"role": "system", "content": system_prompt}] + active["messages"]

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                temperature=0.85,
                max_tokens=1000
            )
            answer = response.choices[0].message.content

            # Efek ketik
            full = ""
            for word in answer.split(" "):
                full += word + " "
                placeholder.markdown(full + "▌")
                time.sleep(0.02)
            placeholder.markdown(full)
            
            active["messages"].append({"role": "assistant", "content": full})

        except Exception as e:
            placeholder.error(f"Error bang 😭: {e}")
