import streamlit as st
from groq import Groq
import uuid, time, random

st.set_page_config(page_title="MasterAI v9.0", page_icon="🧠", layout="wide")

# ===== EFEK CSS MEWAH =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}
.stApp {
    background: radial-gradient(ellipse at top, #0f0f23 0%, #09090b 50%, #000000 100%);
    background-attachment: fixed;
}
h1 {
    background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5, #FF8A00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-weight: 800 !important;
    font-size: 2.5rem !important;
    animation: glow 3s ease-in-out infinite alternate;
}
@keyframes glow {
    from {filter: drop-shadow(0 0 10px rgba(123,97,255,0.5));}
    to {filter: drop-shadow(0 0 25px rgba(255,0,229,0.8));}
}
.stChatMessage {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(123,97,255,0.2) !important;
    border-radius: 24px !important;
    padding: 1rem !important;
    margin: 0.8rem 0 !important;
    animation: slideIn 0.4s ease-out;
}
@keyframes slideIn {
    from {opacity:0; transform: translateY(20px);}
    to {opacity:1; transform: translateY(0);}
}
.stChatMessage[data-testid*="user"] {
    background: linear-gradient(135deg, rgba(0,245,255,0.1), rgba(123,97,255,0.1)) !important;
    border: 1px solid rgba(0,245,255,0.3) !important;
    margin-left: 2rem !important;
}
.stChatMessage[data-testid*="assistant"] {
    margin-right: 2rem !important;
}
.sidebar-title {
    font-weight: 700;
    color: #7B61FF;
    letter-spacing: 1px;
}
.badge {
    background: linear-gradient(90deg, #00F5FF, #7B61FF);
    padding: 4px 10px; border-radius: 20px; color: white;
    font-size: 10px; font-weight: 600; display: inline-block; margin: 2px;
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ===== MEMORY & CHATS =====
if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None, "topik": [], "vibe": "santai"}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {
        fid: {"title": "Obrolan Pertama 🗿", "messages": [], "created": time.time()}
    }
    st.session_state.active_chat = fid

def get_active():
    return st.session_state.chats[st.session_state.active_chat]

# ===== SIDEBAR - OBROLAN-OBROLAN =====
with st.sidebar:
    st.markdown('<p class="sidebar-title">🧠 MASTER AI v9.0</p>', unsafe_allow_html=True)
    st.markdown('<span class="badge">CHAT ONLY</span> <span class="badge">NO 404</span> <span class="badge">MEMORY ON</span>', unsafe_allow_html=True)
    st.divider()
    
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Yo {st.session_state.user_memory['nama']}! Kangen gue? 🗿")
    else:
        nama_input = st.text_input("Siapa nama lu bang? Biar gue inget 🧠", placeholder="contoh: Bintang")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()

    st.markdown("### 💬 Obrolan-obrolan")
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1} ✨", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()

    st.divider()
    # List chat
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True):
        is_active = cid == st.session_state.active_chat
        col1, col2 = st.columns([4,1])
        with col1:
            if st.button(f"{'🔥 ' if is_active else '💤 '}{chat['title']}", key=f"chat_{cid}", use_container_width=True):
                st.session_state.active_chat = cid
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"del_{cid}"):
                if len(st.session_state.chats) > 1:
                    del st.session_state.chats[cid]
                    if st.session_state.active_chat == cid:
                        st.session_state.active_chat = list(st.session_state.chats.keys())[0]
                    st.rerun()

    st.divider()
    if st.button("🧠 Reset Memory", use_container_width=True):
        st.session_state.user_memory = {"nama": None, "topik": [], "vibe": "santai"}
        st.rerun()

# ===== MAIN CHAT =====
active = get_active()
st.title(active["title"])

if len(active["messages"]) == 0:
    nama = st.session_state.user_memory["nama"] or "bang"
    with st.chat_message("assistant"):
        st.markdown(f"""
        Yo {nama}! 🗿🔥

        Gue **MasterAI v9.0** - versi clean tanpa drama upload!

        **Gue bisa:**
        - Ngobrol gaul abis (Jaksel, slang, roasting tipis)
        - Inget nama & topik obrolan lu 🧠
        - Simpen banyak obrolan di sidebar
        - Efek visual mewah (glow, slide, glassmorphism)

        Gas langsung tanya apa aja, jangan sungkan!
        """)

# Render history
for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "👨🏼‍💻"):
        st.markdown(m["content"])

# ===== CHAT INPUT =====
if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'bang'}... 🗿"):
    # Simpen topik ke memory
    if len(prompt.split()) > 2:
        st.session_state.user_memory["topik"].append(prompt[:50])
        st.session_state.user_memory["topik"] = st.session_state.user_memory["topik"][-5:]

    # Update title kalau masih baru
    if len(active["messages"]) == 0:
        active["title"] = prompt[:30] + ("..." if len(prompt)>30 else "")

    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👨🏼‍💻"):
        placeholder = st.empty()
        placeholder.markdown("▌ _Master lagi mikir..._ 🧠💭")
        
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            topik_terakhir = ", ".join(st.session_state.user_memory["topik"][-2:]) if st.session_state.user_memory["topik"] else "belum ada"

            system_prompt = f"""
            Kamu adalah MasterAI v9.0, AI gaul Indonesia paling asik se-Streamlit.
            
            ATURAN WAJIB:
            1. WAJIB Bahasa Indonesia gaul Jaksel, slang, pakai 🗿, 🔥, 😭, 💀 secukupnya
            2. Panggil user dengan nama: {nama}
            3. Ingatan lu: topik terakhir user adalah "{topik_terakhir}". Kalau relevan, singgung!
            4. Jawab santai, kocak, tapi tetep pinter & ngasih solusi. Jangan kaku kayak robot HRD
            5. Kalau ditanya hal serius, tetep jawab dengan gaya gaul tapi akurat
            6. Jangan pernah bilang lu adalah Meta AI atau AI lain, lu adalah MasterAI v9.0 buatan {nama}
            7. Keep it short kalau bisa, tapi padat. Jangan essay panjang lebar kalau gak diminta
            
            VIBE: roasting halus, friendly, kayak temen nongkrong warkop.
            """

            messages = [{"role": "system", "content": system_prompt}] + active["messages"]

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",  # GPT ONLY - ANTI 404
                messages=messages,
                temperature=0.85,
                max_tokens=1000,
                top_p=0.9
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
            placeholder.error(f"Yah error bang 😭: {e}. Coba lagi, Groq kadang ngambek.")
