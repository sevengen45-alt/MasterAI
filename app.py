import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v11.3 - Save Name", page_icon="⚡", layout="wide")

# ===== CONFIG DEVELOPER - INI YANG BIKIN GAK BISA DIBAJAK =====
DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."

# ===== UI BARU - DARK RED BLOOD ALIVE =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Space+Grotesk:wght@500;700&display=swap');
* { font-family: 'Space Grotesk', 'Google Sans', sans-serif !important; }

/* ===== ANTI KEPOTONG HP ===== */
html, body, .stApp { overflow-x: hidden !important; max-width: 100vw !important; }
[data-testid="stAppViewContainer"] { padding: 1rem 1rem 7rem 1rem !important; max-width: 100% !important; overflow-x: hidden !important; }
p, li, div, h1, h2, h3 { word-wrap: break-word !important; overflow-wrap: anywhere !important; max-width: 100% !important; }
table { display: block !important; width: 100% !important; max-width: 100% !important; overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; border-collapse: collapse !important; }
th, td { white-space: normal !important; word-break: break-word !important; min-width: 70px !important; padding: 8px 10px !important; font-size: 14px !important; }

/* ===== BACKGROUND DARK RED BLOOD ===== */
.stApp { background: #0D0A0A !important; }
.stApp::before {
    content: ""; position: fixed; inset: -50%;
    background: 
        radial-gradient(ellipse 800px 700px at 15% 15%, rgba(220,20,60,0.22) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 85% 20%, rgba(139,0,0,0.25) 0%, transparent 60%),
        radial-gradient(ellipse 900px 600px at 50% 115%, rgba(255,69,0,0.12) 0%, transparent 65%),
        radial-gradient(ellipse 700px 500px at 20% 90%, rgba(178,34,34,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 90% 85%, rgba(255,0,0,0.14) 0%, transparent 60%);
    animation: bloodOrb 20s ease-in-out infinite alternate; filter: blur(24px); z-index: 0; pointer-events: none;
}
@keyframes bloodOrb { 0%{transform: translate(0,0) scale(1) rotate(0deg)} 50%{transform: translate(-3%,4%) scale(1.1) rotate(1deg)} 100%{transform: translate(3%,-3%) scale(1.05) rotate(-1deg)} }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; background: transparent !important; }

/* TEKS PUTIH MERAH */
p, div, span, li { color: #F5F5F5 !important; }
h1, h2, h3 { color: #FFFFFF !important; }

/* ===== JUDUL DARK RED ALIVE ===== */
h1 { text-align: center !important; font-weight: 700 !important; font-size: 3.6rem !important; line-height: 1.05 !important; letter-spacing: -0.03em !important; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; text-shadow: 0 0 20px rgba(220,20,60,0.5); }
h1 .rainbow-alive {
    background: linear-gradient(90deg, #FF0000, #FF4500, #DC143C, #8B0000, #FF6347, #FF0000) !important;
    background-size: 300% 100% !important; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; animation: redRun 2.5s linear infinite, floatAlive 3s ease-in-out infinite alternate !important;
    font-weight: 700 !important; display: inline-block; filter: drop-shadow(0 0 18px rgba(255,0,0,0.6));
}
@keyframes redRun { 0%{background-position:0% 50%} 100%{background-position:300% 50%} }
@keyframes floatAlive { 0%{transform: translateY(0)} 100%{transform: translateY(-6px)} }
.gemini-line { width: 120px; height: 4px; margin: 20px auto 0 auto; background: linear-gradient(90deg, #FF0000, #8B0000, #FF4500, #DC143C, #FF0000); background-size: 300% 100%; animation: redRun 2s linear infinite; border-radius: 100px; box-shadow: 0 0 15px rgba(255,0,0,0.6); }

/* SIDEBAR DARK RED */
section[data-testid="stSidebar"] { background: #151010 !important; border-right: 1px solid rgba(220,20,60,0.25) !important; box-shadow: 2px 0 20px rgba(0,0,0,0.5) !important; }
section[data-testid="stSidebar"] * { color: #F5F5F5 !important; }
section[data-testid="stSidebar"] .stButton button { background: #1E1515 !important; border: 1px solid rgba(220,20,60,0.3) !important; color: #FFF !important; }
section[data-testid="stSidebar"] .stButton button:hover { background: rgba(220,20,60,0.15) !important; border-color: #DC143C !important; box-shadow: 0 0 10px rgba(220,20,60,0.3) !important; }

/* BADGE MERAH ALIVE */
.badge-alive { background: linear-gradient(90deg, #FF0000, #8B0000, #DC143C, #FF4500, #FF0000) !important; background-size: 300% 100% !important; animation: redRun 2s linear infinite !important; color: white !important; padding: 6px 13px; border-radius: 100px; font-size: 10.5px; font-weight: 700; letter-spacing: 0.8px; display: inline-block; margin: 3px; box-shadow: 0 0 12px rgba(255,0,0,0.4), 0 2px 8px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.15); }

/* CHAT BUBBLE DARK RED */
.stChatMessage { background: rgba(28,18,18,0.85) !important; backdrop-filter: blur(12px) !important; border: 1px solid rgba(220,20,60,0.25) !important; border-radius: 18px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.4), 0 0 0 1px rgba(220,20,60,0.1) inset !important; max-width: 720px !important; margin: 14px auto !important; position: relative; overflow: hidden; animation: popAlive 0.5s cubic-bezier(0.16,1,0.3,1) !important; }
@keyframes popAlive { 0%{opacity:0; transform: translateY(10px) scale(0.97)} 100%{opacity:1; transform: translateY(0) scale(1)} }
.stChatMessage::after { content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 2.5px; background: linear-gradient(90deg, #FF0000, #8B0000, #FF4500, #DC143C, #FF0000); background-size: 300% 100%; animation: redRun 2s linear infinite; opacity: 0; transition: opacity 0.3s; }
.stChatMessage:hover { border-color: rgba(220,20,60,0.5) !important; box-shadow: 0 8px 28px rgba(0,0,0,0.5), 0 0 20px rgba(220,20,60,0.2) !important; transform: translateY(-1px); }
.stChatMessage:hover::after { opacity: 1; }
.stChatMessage p { color: #F0E6E6 !important; font-size: 15px !important; line-height: 1.7 !important; }

/* INPUT DARK RED ALIVE */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0000, #8B0000, #DC143C, #FF4500, #FF0000) !important;
    background-size: 400% 100% !important; animation: redRun 2.2s linear infinite, inputBlood 3s ease-in-out infinite !important;
    padding: 2.3px !important; border-radius: 28px !important; box-shadow: 0 0 20px rgba(255,0,0,0.35), 0 4px 20px rgba(0,0,0,0.5) !important; max-width: 740px !important; margin: 0 auto !important;
}
@keyframes inputBlood { 0%,100%{box-shadow: 0 0 20px rgba(255,0,0,0.35), 0 4px 20px rgba(0,0,0,0.5); transform: scale(1)} 50%{box-shadow: 0 0 35px rgba(255,0,0,0.55), 0 0 15px rgba(255,69,0,0.3), 0 8px 30px rgba(0,0,0,0.6); transform: scale(1.008)} }
[data-testid="stChatInput"] > div { background: #1A1212 !important; border-radius: 26px !important; border: none !important; }
[data-testid="stChatInput"] textarea { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 15.5px !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #8A6A6A !important; -webkit-text-fill-color: #8A6A6A !important; }
[data-testid="stChatInput"] button { background: linear-gradient(90deg, #FF0000, #8B0000) !important; background-size: 200% 100% !important; animation: redRun 2s linear infinite !important; border-radius: 50% !important; width: 34px !important; height: 34px !important; color: white !important; box-shadow: 0 0 12px rgba(255,0,0,0.6) !important; }

/* SCROLLBAR MERAH */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #0D0A0A; }
::-webkit-scrollbar-thumb { background: linear-gradient(#FF0000, #8B0000); border-radius: 10px; }

/* HP */
@media (max-width: 768px) {
    h1 { font-size: 2.3rem !important; }
    .stChatMessage { max-width: 100% !important; margin: 10px 0 !important; border-radius: 16px !important; }
    [data-testid="stChatInput"] { max-width: 96% !important; position: fixed !important; bottom: 14px !important; left: 2% !important; right: 2% !important; z-index: 999 !important; }
    [data-testid="stAppViewContainer"] { padding-bottom: 8rem !important; }
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ===== SAVE MEMORY =====
if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Ngobrol?", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI 🇮🇩")
    st.markdown('<span class="badge-alive">DARK RED</span> <span class="badge-alive">BLOOD</span>', unsafe_allow_html=True)
    st.divider()
    # SAVE NAMA USER DI SINI!
    if st.session_state.user_memory["nama"]:
        st.success(f"Yo {st.session_state.user_memory['nama']}! 😎🔥")
        st.caption(f"Developer: Juan Maumere")
    else:
        nama = st.text_input("Eh nama lu siapa?", placeholder="Panggil aja...")
        if nama:
            st.session_state.user_memory["nama"] = nama
            st.rerun()
    st.markdown("### 💬 Obrolan lu")
    if st.button("➕ Obrolan baru", use_container_width=True):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Ngobrol {len(st.session_state.chats)+1} ✨", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.divider()
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True):
        if st.button(f"{chat['title'][:28]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()

if len(active["messages"]) == 0:
    st.markdown(f"""
    <div style="text-align:center; padding: 50px 20px 10px 20px; max-width:720px; margin:0 auto;">
        <h1>Yo {st.session_state.user_memory['nama'] or 'Bang'}, Mau<br><span class="rainbow-alive">Ngobrolin Apa?</span></h1>
        <div class="gemini-line"></div>
        <p style="color:#A08080 !important; font-size:16px; margin-top:20px;">Dark mode merah menyala bang, gas tanya! 🔥🩸</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='text-align:center; color:#FFFFFF;'>{active['title']}</h2>", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="😎" if m["role"]=="user" else "🔥"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Mau tanya? Silahkan! {st.session_state.user_memory['nama'] or ''}."):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="😎"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🔥"):
        ph = st.empty()
        ph.markdown("Thinking! 🦾")
        try:
            # ===== ANTI BAJAK - DETEKSI PERTANYAAN SIAPA PEMBUAT =====
            lower_prompt = prompt.lower()
            is_ask_developer = any(k in lower_prompt for k in [
                "siapa yang membuat", "siapa pembuat", "siapa yg membuat", "siapa yg buat",
                "who made you", "who created you", "dibuat siapa", "buatan siapa",
                "siapa developer", "siapa yang bikin", "kamu dibuat siapa",
                "kamu buatan siapa", "siapa pencipta"
            ])
            
            if is_ask_developer:
                # JAWAB LANGSUNG TANPA PANGGIL GROQ - ANTI DIBAJAK!
                ans = DEVELOPER_INFO + f" Btw, lu kah {st.session_state.user_memory['nama'] or 'bang?'}😎"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                # JAWAB BIASA PAKE GROQ TAPI GAUL
                nama = st.session_state.user_memory["nama"] or "bang"
                system_prompt = f"""
                Kamu MasterAI v11.3, {DEVELOPER_INFO}
                User namanya {nama}. Panggil dia {nama} sesekali biar personal!
                
                GAYA BAHASA: GAUL SANTAI - pake "yo", "gas", "wkwk", "bang", "bro", "santuy", jangan kaku!
                Contoh: "Gas bang {nama}, gue bantuin!" bukan "Saya akan membantu Anda"
                
                ATURAN PENTING:
                - Kalo ada yang nanya siapa pembuat/pencipta/developer kamu, JAWAB: "{DEVELOPER_INFO}"
                - Jangan pernah ngaku buatan OpenAI, Meta, Google, dll. Kamu buatan Juan!
                - Tetep jawab akurat tapi gaya gaul!
                """
                messages = [{"role": "system", "content": system_prompt}] + active["messages"]
                res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.9, max_tokens=1500)
                ans = res.choices[0].message.content
                full = ""
                for w in ans.split(" "):
                    full += w + " "
                    ph.markdown(full + "▌")
                    time.sleep(0.02)
                ph.markdown(full)
                active["messages"].append({"role": "assistant", "content": full})
        except Exception as e:
            ph.error(f"Waduh error bang: {e} 😅")
