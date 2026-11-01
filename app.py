import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v10 - Clean Orange & RGB", page_icon="⚡", layout="wide")

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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&family=Inter:wght@400;500;600;700&display=swap');

* {font-family: 'Inter', sans-serif !important;}
h1, h2, h3, h4, h5, h6 {font-family: 'Space Grotesk', sans-serif !important;}

/* THEME CLAUDE: Clean White & Soft Orange Background */
.stApp {
    background: #FAF9F5 !important;
    color: #1A1A1A !important;
}

/* JUDUL - Tetap RGB Menyala Sesuai Request */
h1 {
    background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040) !important;
    background-size: 400% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 4.2rem !important;
    letter-spacing: -0.05em !important;
    animation: rainbowFlow 3s linear infinite, floatTitle 3s ease-in-out infinite alternate !important;
    filter: drop-shadow(0 0 15px rgba(255,138,0,0.25));
}
@keyframes rainbowFlow { 0%{background-position:0%} 100%{background-position:400%} }
@keyframes floatTitle { 0%{transform: translateY(0px)} 100%{transform: translateY(-6px)} }
@media (max-width:600px){ h1{font-size:2.8rem !important;} }

/* SIDEBAR - Clean dengan Garis RGB di Kanan */
section[data-testid="stSidebar"] {
    background: #F4F1EA !important;
    border-right: 3px solid transparent !important;
    position: relative;
}
section[data-testid="stSidebar"]::before {
    content: ""; position: absolute; inset: 0; right: -3px; left: auto; width: 3px;
    background: linear-gradient(180deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040);
    background-size: 100% 400%; animation: borderRun 3s linear infinite;
}
@keyframes borderRun { 0%{background-position:0% 0%} 100%{background-position:0% 400%} }

/* CHAT MESSAGE - Gaya Clean Card Claude */
.stChatMessage {
    background: #FFFFFF !important;
    border-radius: 20px !important;
    border: 1px solid #EBE7DE !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03) !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
}
.stChatMessage:hover {
    border-color: #FF8A00 !important;
    box-shadow: 0 8px 30px rgba(255,138,0,0.08) !important;
}
.stChatMessage p { color: #2C2C2C !important; font-size: 16px !important; line-height: 1.6 !important; }
.stChatMessage strong { color: #D96500 !important; }

/* BADGE RGB */
.badge {
    background: linear-gradient(90deg, #FF0040, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6) !important;
    background-size: 300% 100% !important;
    animation: rainbowFlow 2s linear infinite !important;
    padding: 5px 14px; border-radius: 50px; color: white; font-weight: 900; font-size: 11px;
    display: inline-block; margin: 4px; letter-spacing: 0.08em;
    box-shadow: 0 2px 10px rgba(255,138,0,0.2);
}

/* CHAT INPUT - Clean Orange Accent */
[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 2px solid #E3DDD1 !important;
    border-radius: 24px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
    max-width: 780px !important; margin: 0 auto !important;
    padding: 4px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #FF8A00 !important;
    box-shadow: 0 0 0 3px rgba(255,138,0,0.15) !important;
}
[data-testid="stChatInput"] textarea { color: #1A1A1A !important; font-weight: 500 !important; font-size: 16px !important; }
[data-testid="stChatInput"] button {
    background: #FF8A00 !important;
    color: white !important;
    border-radius: 16px !important;
    font-weight: 800 !important;
    transition: all 0.2s !important;
}
[data-testid="stChatInput"] button:hover {
    background: #E07800 !important;
    transform: scale(1.05) !important;
}

/* BIO CARD */
.bio-card {
    background: #FFFFFF !important;
    border: 1px solid #EBE7DE !important;
    border-radius: 16px !important;
    padding: 16px !important;
    margin: 10px 0 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.02);
}
.bio-avatar {
    width: 70px; height: 70px; border-radius: 50%;
    background: linear-gradient(135deg, #FF8A00, #FF0040, #7B61FF);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; font-weight: 900; color: white;
    margin: 0 auto 12px auto;
    box-shadow: 0 4px 15px rgba(255,138,0,0.3);
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
    st.markdown('<span class="badge">CLEAN ORANGE</span> <span class="badge">RGB ALIVE</span>', unsafe_allow_html=True)
    st.divider()
    
    # ===== BIO CARD PENCIPTA =====
    st.markdown(f"""
    <div class="bio-card">
        <div class="bio-avatar">J</div>
        <div style="text-align:center;">
            <div style="color:#1A1A1A !important; font-weight:900; font-size:14px;">{DEVELOPER_BIO['nama']}</div>
            <div style="color:#FF8A00 !important; font-size:12px; font-weight:700;">{DEVELOPER_BIO['panggilan']} • {DEVELOPER_BIO['umur']}</div>
            <div style="color:#555555 !important; font-size:11px; margin-top:6px;">{DEVELOPER_BIO['sekolah']}</div>
            <div style="color:#666666 !important; font-size:10px; margin-top:4px;">{DEVELOPER_BIO['lokasi']}</div>
        </div>
        <div style="margin-top:12px; padding-top:12px; border-top: 1px solid #EBE7DE;">
            <div style="color:#D96500 !important; font-size:10px; font-weight:800; letter-spacing:0.05em;">✨ {DEVELOPER_BIO['motto']}</div>
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
            <div style="color:#1A1A1A; font-weight:900; margin-top:8px;">JUAN</div>
            <div style="color:#FF8A00; font-size:12px;">15 Tahun</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        **{DEVELOPER_BIO['nama']}** adalah seorang pelajar berbakat dari **{DEVELOPER_BIO['sekolah']}** di Maumere, NTT.
        
        Di umur **15 tahun**, dia sudah mampu membuat AI sekelas MasterAI v10 Clean Orange Edition ini! 🔥
        
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
                Kamu MasterAI v10 Clean Orange Edition. {DEVELOPER_INFO}
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
