import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v10 - Ultra RGB Alive", page_icon="⚡", layout="wide")

# ===== CONFIG DEVELOPER - ANTI BAJAK + BIO =====
DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."

DEVELOPER_BIO = {
    "nama": "Jonathan Kristian Sergio Marut",
    "panggilan": "Juan",
    "umur": "15 Tahun",
    "sekolah": "SMAK St. Maria Monte Carmelo Maumere",
    "role": "AI Developer & Pelajar",
    "lokasi": "Maumere, NTT, Indonesia 🇮🇩",
    "motto": "Umur 15 tahun bukan halangan buat bikin AI keren! 🔥",
    "skill": ["Python", "Streamlit", "Groq AI", "UI/UX Design", "Prompt Engineering"]
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');

* {font-family: 'Space Grotesk', sans-serif !important;}

.stApp {
    background: #030308 !important;
    position: relative;
    overflow: hidden;
}
.stApp::before {
    content: "";
    position: fixed;
    width: 200%; height: 200%;
    top: -50%; left: -50%;
    background: 
        radial-gradient(circle at 20% 30%, rgba(255,0,128,0.55) 0%, transparent 35%),
        radial-gradient(circle at 80% 20%, rgba(0,245,255,0.55) 0%, transparent 40%),
        radial-gradient(circle at 50% 80%, rgba(255,230,0,0.45) 0%, transparent 40%),
        radial-gradient(circle at 10% 80%, rgba(130,0,255,0.6) 0%, transparent 38%),
        radial-gradient(circle at 90% 85%, rgba(0,255,136,0.4) 0%, transparent 35%);
    animation: orbDance 20s ease-in-out infinite alternate;
    filter: blur(18px) saturate(1.3);
    z-index: 0;
    pointer-events: none;
}
@keyframes orbDance {
    0% { transform: translate(0,0) scale(1) rotate(0deg); }
    25% { transform: translate(-8%, 6%) scale(1.1) rotate(2deg); }
    50% { transform: translate(6%, -8%) scale(0.95) rotate(-2deg); }
    75% { transform: translate(-4%, -4%) scale(1.08) rotate(1deg); }
    100% { transform: translate(8%, 5%) scale(1.02) rotate(-1deg); }
}

[data-testid="stAppViewContainer"] { position: relative; z-index: 2; }

/* JUDUL */
h1 {
    background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040) !important;
    background-size: 400% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 5rem !important;
    letter-spacing: -0.06em !important;
    animation: rainbowFlow 3s linear infinite, floatTitle 3s ease-in-out infinite alternate, glowPulse 2s ease-in-out infinite !important;
    filter: drop-shadow(0 0 20px rgba(255,0,230,0.7)) drop-shadow(0 0 40px rgba(0,245,255,0.5));
}
@keyframes rainbowFlow { 0%{background-position:0%} 100%{background-position:400%} }
@keyframes floatTitle { 0%{transform: translateY(0px) rotate(-0.5deg)} 100%{transform: translateY(-10px) rotate(0.5deg)} }
@keyframes glowPulse { 0%,100%{filter: drop-shadow(0 0 20px rgba(255,0,230,0.7)) drop-shadow(0 0 40px rgba(0,245,255,0.5))} 50%{filter: drop-shadow(0 0 35px rgba(255,0,230,1)) drop-shadow(0 0 70px rgba(0,245,255,0.8))} }
@media (max-width:600px){ h1{font-size:3rem !important;} }

section[data-testid="stSidebar"] {
    background: rgba(12,10,28,0.85) !important;
    backdrop-filter: blur(30px) saturate(1.5) !important;
    border-right: 3px solid transparent !important;
    position: relative;
}
section[data-testid="stSidebar"]::before {
    content: ""; position: absolute; inset: 0; right: -3px; left: auto; width: 3px;
    background: linear-gradient(180deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040);
    background-size: 100% 400%; animation: borderRun 3s linear infinite;
}
@keyframes borderRun { 0%{background-position:0% 0%} 100%{background-position:0% 400%} }

.stChatMessage {
    background: linear-gradient(135deg, rgba(255,255,255,0.10) 0%, rgba(123,97,255,0.22) 100%) !important;
    backdrop-filter: blur(24px) !important;
    border-radius: 28px !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.15) !important;
    position: relative; overflow: hidden;
    animation: popIn 0.7s cubic-bezier(0.34,1.56,0.64,1) !important;
    transition: all 0.35s ease !important;
}
@keyframes popIn { 0%{transform: translateY(20px) scale(0.92); opacity:0} 100%{transform: translateY(0) scale(1); opacity:1} }
.stChatMessage:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 18px 50px rgba(0,0,0,0.5), 0 0 30px rgba(123,97,255,0.35) !important;
    border-color: rgba(0,245,255,0.4) !important;
}
.stChatMessage::before {
    content: ""; position: absolute; top:-50%; left:-60%; width:80%; height:200%;
    background: linear-gradient(100deg, transparent, rgba(255,255,255,0.18), transparent);
    transform: rotate(15deg); animation: shineSweep 5s ease-in-out infinite;
}
@keyframes shineSweep { 0%{left:-60%} 40%{left:120%} 100%{left:120%} }
.stChatMessage::after {
    content: ""; position: absolute; inset: -2px; border-radius: 28px;
    background: linear-gradient(90deg, #FF0040, #FFE600, #00F5FF, #7B61FF);
    background-size: 300% 100%; animation: rainbowFlow 4s linear infinite;
    z-index: -1; opacity: 0; transition: opacity 0.4s;
}
.stChatMessage:hover::after { opacity: 0.6; filter: blur(8px); }

.stChatMessage p { color: #FFF !important; font-size: 16px !important; line-height: 1.7 !important; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
.stChatMessage strong { color: #00F5FF !important; text-shadow: 0 0 15px #00F5FF !important; }

.badge {
    background: linear-gradient(90deg, #FF0040, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6) !important;
    background-size: 300% 100% !important;
    animation: rainbowFlow 2s linear infinite, badgeBounce 2s ease-in-out infinite alternate !important;
    padding: 6px 16px; border-radius: 50px; color: white; font-weight: 900; font-size: 11px;
    display: inline-block; margin: 4px; letter-spacing: 0.08em;
    box-shadow: 0 0 15px rgba(255,0,230,0.5), 0 4px 15px rgba(0,0,0,0.3);
}
@keyframes badgeBounce { 0%{transform: translateY(0) scale(1)} 100%{transform: translateY(-4px) scale(1.05)} }

[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #0040FF, #7B61FF, #FF00E6, #FF0040) !important;
    background-size: 500% 100% !important;
    animation: rainbowFlow 1.2s linear infinite, inputBreath 2s ease-in-out infinite !important;
    padding: 4px !important; border-radius: 30px !important;
    box-shadow: 0 0 30px rgba(255,0,128,0.6), 0 0 60px rgba(0,245,255,0.5), 0 12px 40px rgba(0,0,0,0.5) !important;
    max-width: 780px !important; margin: 0 auto !important;
}
@keyframes inputBreath { 0%,100%{transform: scale(1); box-shadow: 0 0 30px rgba(255,0,128,0.6), 0 0 60px rgba(0,245,255,0.5)} 50%{transform: scale(1.02); box-shadow: 0 0 45px rgba(255,0,128,0.9), 0 0 90px rgba(0,245,255,0.7)} }
[data-testid="stChatInput"] > div {
    background: rgba(10,10,22,0.95) !important; backdrop-filter: blur(20px) !important;
    border-radius: 26px !important; border: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stChatInput"] textarea { color: #FFF !important; font-weight: 700 !important; font-size: 16.5px !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #00F5FF, #FF00E6) !important;
    background-size: 200% 100% !important;
    animation: rainbowFlow 1.5s linear infinite !important;
    border-radius: 18px !important; font-weight: 900 !important;
    box-shadow: 0 0 25px rgba(0,245,255,0.8) !important;
    transition: all 0.2s !important;
}
[data-testid="stChatInput"] button:hover { transform: scale(1.08) rotate(2deg) !important; }

/* BIO CARD RGB */
.bio-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(123,97,255,0.15) 100%) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 20px !important;
    padding: 16px !important;
    margin: 10px 0 !important;
    backdrop-filter: blur(15px) !important;
}
.bio-avatar {
    width: 70px; height: 70px; border-radius: 50%;
    background: linear-gradient(135deg, #FF0040, #00F5FF, #FFE600);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; font-weight: 900; color: white;
    margin: 0 auto 12px auto;
    box-shadow: 0 0 20px rgba(255,0,230,0.5);
    animation: rainbowFlow 3s linear infinite;
}
</style>
""", unsafe_allow_html=True)

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
    st.markdown('<span class="badge">ULTRA RGB</span> <span class="badge">ALIVE</span>', unsafe_allow_html=True)
    st.divider()
    
    # ===== BIO CARD PENCIPTA =====
    st.markdown(f"""
    <div class="bio-card">
        <div class="bio-avatar">J</div>
        <div style="text-align:center;">
            <div style="color:white !important; font-weight:900; font-size:14px;">{DEVELOPER_BIO['nama']}</div>
            <div style="color:#00F5FF !important; font-size:12px; font-weight:700;">{DEVELOPER_BIO['panggilan']} • {DEVELOPER_BIO['umur']}</div>
            <div style="color:rgba(255,255,255,0.7) !important; font-size:11px; margin-top:6px;">{DEVELOPER_BIO['sekolah']}</div>
            <div style="color:rgba(255,255,255,0.6) !important; font-size:10px; margin-top:4px;">{DEVELOPER_BIO['lokasi']}</div>
        </div>
        <div style="margin-top:12px; padding-top:12px; border-top: 1px solid rgba(255,255,255,0.1);">
            <div style="color:#FFE600 !important; font-size:10px; font-weight:800; letter-spacing:0.05em;">✨ {DEVELOPER_BIO['motto']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("👨‍💻 Lihat Bio Lengkap", expanded=False):
        st.markdown(f"""
        **Nama:** {DEVELOPER_BIO['nama']}  
        **Panggilan:** {DEVELOPER_BIO['panggilan']}  
        **Umur:** {DEVELOPER_BIO['umur']}  
        **Sekolah:** {DEVELOPER_BIO['sekolah']}  
        **Role:** {DEVELOPER_BIO['role']}  
        **Lokasi:** {DEVELOPER_BIO['lokasi']}  
        
        **Skill:**
        """)
        for skill in DEVELOPER_BIO['skill']:
            st.markdown(f'<span class="badge">{skill}</span>', unsafe_allow_html=True)
    
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Yo {st.session_state.user_memory['nama']}!")
    else:
        nama_input = st.text_input("Nama lu siapa bang?", placeholder="Cth: Juan")
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

# ===== EXPANDER BIO DI MAIN PAGE JUGA =====
with st.expander("🌟 Tentang Pembuat - Jonathan Kristian Sergio Marut (Juan)", expanded=False):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div style="text-align:center;">
            <div class="bio-avatar" style="width:90px; height:90px; font-size:40px;">J</div>
            <div style="color:white; font-weight:900; margin-top:8px;">JUAN</div>
            <div style="color:#00F5FF; font-size:12px;">15 Tahun</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        **{DEVELOPER_BIO['nama']}** adalah seorang pelajar berbakat dari **{DEVELOPER_BIO['sekolah']}** di Maumere, NTT.
        
        Di umur **15 tahun**, dia sudah mampu membuat AI sekelas MasterAI v10 Ultra RGB Alive ini! 🔥
        
        > "{DEVELOPER_BIO['motto']}"
        
        **Lokasi:** {DEVELOPER_BIO['lokasi']}  
        **Keahlian:** {', '.join(DEVELOPER_BIO['skill'])}
        
        AI ini adalah bukti kalau anak muda Indonesia bisa bikin karya kelas dunia! 🇮🇩✨
        """)

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "🔥"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Mau tanya? {st.session_state.user_memory['nama'] or 'Silahkan!'} 😎🔥"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🔥"):
        ph = st.empty()
        ph.markdown("▌ _Thinking!⚡ ")
        try:
            # ===== ANTI BAJAK BIO =====
            lower_prompt = prompt.lower()
            is_ask_developer = any(k in lower_prompt for k in [
                "siapa yang membuat", "siapa pembuat", "siapa yg membuat", "siapa yg buat",
                "who made you", "who created you", "dibuat siapa", "buatan siapa",
                "siapa developer", "siapa yang bikin", "kamu dibuat siapa",
                "kamu buatan siapa", "siapa pencipta", "bio pembuat", "tentang pembuat"
            ])
            
            if is_ask_developer:
                ans = f"""{DEVELOPER_INFO}

**🔥 BIO LENGKAP PENCIPTA:**
👤 **Nama:** {DEVELOPER_BIO['nama']}
😎 **Panggilan:** {DEVELOPER_BIO['panggilan']}
🎂 **Umur:** {DEVELOPER_BIO['umur']}
🏫 **Sekolah:** {DEVELOPER_BIO['sekolah']}
📍 **Lokasi:** {DEVELOPER_BIO['lokasi']}
💻 **Role:** {DEVELOPER_BIO['role']}
✨ **Motto:** {DEVELOPER_BIO['motto']}
🛠️ **Skill:** {', '.join(DEVELOPER_BIO['skill'])}

Gila kan? Umur 15 tahun udah bikin AI sekece ini! 🇮🇩🔥
"""
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                nama = st.session_state.user_memory["nama"] or "bang"
                system_prompt = f"""
                Kamu MasterAI v10 Ultra RGB Alive. {DEVELOPER_INFO}
                Bio Pencipta: {DEVELOPER_BIO}
                Nama user {nama}. Bahasa Indonesia gaul, santai, jawab jelas dan bener. Kalau matematika jelasin step by step.
                
                ATURAN ANTI BAJAK:
                - Kalo ditanya siapa pembuat, JAWAB dengan BIO lengkap di atas!
                - Jangan pernah ngaku buatan OpenAI, Google, dll. Kamu buatan {DEVELOPER_BIO['nama']} alias {DEVELOPER_BIO['panggilan']}!
                """
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
