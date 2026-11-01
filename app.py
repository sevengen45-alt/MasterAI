import streamlit as st
from groq import Groq
import uuid
import time

# Konfigurasi layout responsif (Potret di HP, Auto-Lanskap di Desktop)
st.set_page_config(
    page_title="MasterAI v10 - Ultra RGB Alive", 
    page_icon="⚡", 
    layout="centered"
)

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
  
/* Perbaikan agar elemen teks umum tidak merusak ikon bawaan Streamlit */
body, p, span, div {font-family: 'Space Grotesk', sans-serif !important;}  
  
.stApp {  
    background: #030308 !important;  
    position: relative;  
    overflow-x: hidden;  
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
    50% { transform: translate6%, -8%) scale(0.95) rotate(-2deg); }  
    75% { transform: translate(-4%, -4%) scale(1.08) rotate(1deg); }  
    100% { transform: translate(8%, 5%) scale(1.02) rotate(-1deg); }  
}  
  
[data-testid="stAppViewContainer"] { position: relative; z-index: 2; }  

/* KONTROL FRAME UTAMA POTRET & LANSKAP */
.block-container {
    max-width: 800px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 5rem !important;
}
  
/* JUDUL */  
h1 {  
    background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040) !important;  
    background-size: 400% 100% !important;  
    -webkit-background-clip: text !important;  
    -webkit-text-fill-color: transparent !important;  
    text-align: center !important;  
    font-weight: 900 !important;  
    font-size: 3rem !important;  
    letter-spacing: -0.06em !important;  
    animation: rainbowFlow 3s linear infinite, floatTitle 3s ease-in-out infinite alternate, glowPulse 2s ease-in-out infinite !important;  
    filter: drop-shadow(0 0 20px rgba(255,0,230,0.7)) drop-shadow(0 0 40px rgba(0,245,255,0.5));  
}  
@keyframes rainbowFlow { 0%{background-position:0%} 100%{background-position:400%} }  
@keyframes floatTitle { 0%{transform: translateY(0px) rotate(-0.5deg)} 100%{transform: translateY(-10px) rotate(0.5deg)} }  
@keyframes glowPulse { 0%,100%{filter: drop-shadow(0 0 20px rgba(255,0,230,0.7)) drop-shadow(0 0 40px rgba(0,245,255,0.5))} 50%{filter: drop-shadow(0 0 35px rgba(255,0,230,1)) drop-shadow(0 0 70px rgba(0,245,255,0.8))} }  
@media (max-width:600px){ h1{font-size:2.2rem !important;} }  
  
section[data-testid="stSidebar"] {  
    background: rgba(12,10,28,0.95) !important;  
    backdrop-filter: blur(30px) saturate(1.5) !important;  
    border-right: 2px solid rgba(255,255,255,0.1) !important;  
}  
  
.stChatMessage {  
    background: linear-gradient(135deg, rgba(255,255,255,0.10) 0%, rgba(123,97,255,0.22) 100%) !important;  
    backdrop-filter: blur(24px) !important;  
    border-radius: 24px !important;  
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
  
.stChatMessage p { color: #FFF !important; font-size: 15px !important; line-height: 1.6 !important; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }  
.stChatMessage strong { color: #00F5FF !important; text-shadow: 0 0 15px #00F5FF !important; }  
  
.badge {  
    background: linear-gradient(90deg, #FF0040, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6) !important;  
    background-size: 300% 100% !important;  
    animation: rainbowFlow 2s linear infinite, badgeBounce 2s ease-in-out infinite alternate !important;  
    padding: 4px 10px; border-radius: 50px; color: white; font-weight: 900; font-size: 9px;  
    display: inline-block; margin: 2px; letter-spacing: 0.08em;  
    box-shadow: 0 0 15px rgba(255,0,230,0.5);  
}  
@keyframes badgeBounce { 0%{transform: translateY(0) scale(1)} 100%{transform: translateY(-4px) scale(1.05)} }  
  
[data-testid="stChatInput"] {  
    background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #0040FF, #7B61FF, #FF00E6, #FF0040) !important;  
    background-size: 500% 100% !important;  
    animation: rainbowFlow 1.2s linear infinite, inputBreath 2s ease-in-out infinite !important;  
    padding: 3px !important; border-radius: 22px !important;  
    box-shadow: 0 0 25px rgba(255,0,128,0.6), 0 0 50px rgba(0,245,255,0.5) !important;  
}  
@keyframes inputBreath { 0%,100%{transform: scale(1);} 50%{transform: scale(1.01);} }  
[data-testid="stChatInput"] > div {  
    background: rgba(10,10,22,0.95) !important; backdrop-filter: blur(20px) !important;  
    border-radius: 20px !important; border: 1px solid rgba(255,255,255,0.08) !important;  
}  
[data-testid="stChatInput"] textarea { color: #FFF !important; font-weight: 700 !important; font-size: 14.5px !important; }  
[data-testid="stChatInput"] button {  
    background: linear-gradient(90deg, #00F5FF, #FF00E6) !important;  
    border-radius: 12px !important; font-weight: 900 !important;  
}  
  
/* BIO CARD RGB */  
.bio-card {  
    background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(123,97,255,0.15) 100%) !important;  
    border: 1px solid rgba(255,255,255,0.12) !important;  
    border-radius: 14px !important;  
    padding: 10px !important;  
    margin: 6px 0 !important;  
    backdrop-filter: blur(15px) !important;  
}  
.bio-avatar {  
    width: 50px; height: 50px; border-radius: 50%;  
    background: linear-gradient(135deg, #FF0040, #00F5FF, #FFE600);  
    display: flex; align-items: center; justify-content: center;  
    font-size: 24px; font-weight: 900; color: white;  
    margin: 0 auto 8px auto;  
    box-shadow: 0 0 15px rgba(255,0,230,0.5);  
    animation: rainbowFlow 3s linear infinite;  
}  
</style>  """, unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Memulai Obrolan!", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

# ===== KONTROL UTAMA & PANEL HANDPHONE DI DALAM FRAME =====
with st.sidebar:
    st.markdown("### MasterAI v10")
    st.markdown('<span class="badge">ULTRA RGB</span> <span class="badge">ALIVE</span>', unsafe_allow_html=True)
    st.divider()

    # Bio Card Pencipta di Sidebar
    st.markdown(f"""  
    <div class="bio-card">  
        <div class="bio-avatar">J</div>  
        <div style="text-align:center;">  
            <div style="color:white !important; font-weight:900; font-size:12px;">{DEVELOPER_BIO['nama']}</div>  
            <div style="color:#00F5FF !important; font-size:10px; font-weight:700;">{DEVELOPER_BIO['panggilan']} • {DEVELOPER_BIO['umur']}</div>  
            <div style="color:rgba(255,255,255,0.7) !important; font-size:9px; margin-top:3px;">{DEVELOPER_BIO['sekolah']}</div>  
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
        """)  
        for skill in DEVELOPER_BIO['skill']:  
            st.markdown(f'<span class="badge">{skill}</span>', unsafe_allow_html=True)  
      
    st.divider()  

# ===== PANEL UTAMA: SAVE NAMA & OBROLAN BARU (MUAT DI HP) =====
with st.container():
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.session_state.user_memory["nama"]:  
            st.success(f"👋 Yo {st.session_state.user_memory['nama']}!")  
        else:  
            nama_input = st.text_input("Nama lu siapa bang?", placeholder="Cth: Juan")  
            if nama_input:  
                st.session_state.user_memory["nama"] = nama_input  
                st.rerun()  
    with col_b:
        st.markdown("<div style='margin-top: 2px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):  
            nid = str(uuid.uuid4())  
            st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1} ✨", "messages": [], "created": time.time()}  
            st.session_state.active_chat = nid  
            st.rerun()  

# Pilihan Riwayat Chat Cepat di Main Page (Sangat ramah user HP)
with st.expander("📂 Pilih / Lihat Riwayat Obrolan Lainnya", expanded=False):
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True):  
        if st.button(f"💬 {chat['title'][:30]}", key=f"quick_chat_{cid}", use_container_width=True):  
            st.session_state.active_chat = cid  
            st.rerun()

st.divider()

active = get_active()
st.title(active["title"])

# ===== EXPANDER BIO DI MAIN PAGE =====
with st.expander("🌟 Tentang Pembuat - Jonathan Kristian Sergio Marut (Juan)", expanded=False):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div style="text-align:center;">
        <div class="bio-avatar" style="width:70px; height:70px; font-size:30px;">J</div>
        <div style="color:white; font-weight:900; margin-top:4px;">JUAN</div>
        <div style="color:#00F5FF; font-size:10px;">15 Tahun</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        {DEVELOPER_BIO['nama']} adalah seorang pelajar berbakat dari {DEVELOPER_BIO['sekolah']} di Maumere, NTT.

        Di umur **15 tahun**, dia sudah mampu membuat AI sekelas MasterAI v10 Ultra RGB Alive ini! 🔥  
          
        > "{DEVELOPER_BIO['motto']}"  
          
        **Lokasi:** {DEVELOPER_BIO['lokasi']}    
        **Keahlian:** {', '.join(DEVELOPER_BIO['skill'])}  
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

🔥 BIO LENGKAP PENCIPTA:
👤 Nama: {DEVELOPER_BIO['nama']}
😎 Panggilan: {DEVELOPER_BIO['panggilan']}
🎂 Umur: {DEVELOPER_BIO['umur']}
🏫 Sekolah: {DEVELOPER_BIO['sekolah']}
📍 Lokasi: {DEVELOPER_BIO['lokasi']}
💻 Role: {DEVELOPER_BIO['role']}
✨ Motto: {DEVELOPER_BIO['motto']}
🛠️ Skill: {', '.join(DEVELOPER_BIO['skill'])}

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
