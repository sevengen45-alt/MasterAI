import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v11.3 - Save Name", page_icon="⚡", layout="wide")

# ===== CONFIG DEVELOPER - INI YANG BIKIN GAK BISA DIBAJAK =====
DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."

# ===== UI BARU - CUMA INI YANG GUE UBAH =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
* { font-family: 'Google Sans', system-ui, sans-serif !important; }

/* ===== ANTI KEPOTONG HP - FIX UTAMA ===== */
html, body, .stApp { overflow-x: hidden !important; max-width: 100vw !important; }
[data-testid="stAppViewContainer"] { padding: 1rem 1rem 7rem 1rem !important; max-width: 100% !important; overflow-x: hidden !important; }
p, li, div, h1, h2, h3 { word-wrap: break-word !important; overflow-wrap: anywhere !important; max-width: 100% !important; }
table { display: block !important; width: 100% !important; max-width: 100% !important; overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; border-collapse: collapse !important; }
th, td { white-space: normal !important; word-break: break-word !important; min-width: 70px !important; padding: 8px 10px !important; font-size: 14px !important; }

/* ===== BACKGROUND PUTIH + ORB ALIVE ===== */
.stApp { background: #FFFFFF !important; }
.stApp::before {
    content: ""; position: fixed; inset: -40%;
    background: 
        radial-gradient(ellipse 700px 600px at 12% 8%, rgba(66,133,244,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 88% 12%, rgba(219,68,55,0.09) 0%, transparent 60%),
        radial-gradient(ellipse 900px 600px at 50% 110%, rgba(15,157,88,0.09) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 18% 88%, rgba(244,180,0,0.11) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 92% 85%, rgba(156,39,176,0.09) 0%, transparent 60%);
    animation: orbAlive 18s ease-in-out infinite alternate; filter: blur(20px); z-index: 0; pointer-events: none;
}
@keyframes orbAlive { 0%{transform: translate(0,0) scale(1)} 50%{transform: translate(-2.5%,2.5%) scale(1.07)} 100%{transform: translate(2%,-1.5%) scale(1.03)} }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; background: transparent !important; }

/* ===== TEKS ===== */
p, div, span { color: #202124 !important; }

/* ===== JUDUL ALIVE ===== */
h1 { text-align: center !important; font-weight: 400 !important; font-size: 3.4rem !important; line-height: 1.08 !important; color: #202124 !important; -webkit-text-fill-color: #202124 !important; letter-spacing: -0.02em !important; }
h1 .rainbow-alive {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 300% 100% !important; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; animation: rainbowRun 2.8s linear infinite, floatAlive 3s ease-in-out infinite alternate !important;
    font-weight: 700 !important; display: inline-block;
}
@keyframes rainbowRun { 0%{background-position:0% 50%} 100%{background-position:300% 50%} }
@keyframes floatAlive { 0%{transform: translateY(0)} 100%{transform: translateY(-5px)} }
.gemini-line { width: 110px; height: 4px; margin: 20px auto 0 auto; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4); background-size: 300% 100%; animation: rainbowRun 2s linear infinite; border-radius: 100px; box-shadow: 0 2px 12px rgba(66,133,244,0.25); }

/* ===== SIDEBAR PUTIH BERSIH ===== */
section[data-testid="stSidebar"] { background: #F8F9FA !important; border-right: 1px solid #E8EAED !important; }
section[data-testid="stSidebar"] * { color: #202124 !important; }

/* ===== BADGE ALIVE ===== */
.badge-alive { background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important; background-size: 300% 100% !important; animation: rainbowRun 2s linear infinite !important; color: white !important; padding: 6px 13px; border-radius: 100px; font-size: 10.5px; font-weight: 700; letter-spacing: 0.5px; display: inline-block; margin: 3px; box-shadow: 0 2px 8px rgba(66,133,244,0.22); }

/* ===== CHAT BUBBLE ===== */
.stChatMessage { background: #FFFFFF !important; border: 1px solid #E8EAED !important; border-radius: 20px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03) !important; max-width: 720px !important; margin: 12px auto !important; position: relative; overflow: hidden; animation: popAlive 0.45s cubic-bezier(0.16,1,0.3,1) !important; }
@keyframes popAlive { 0%{opacity:0; transform: translateY(8px) scale(0.98)} 100%{opacity:1; transform: translateY(0) scale(1)} }
.stChatMessage::after { content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 2.5px; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4); background-size: 300% 100%; animation: rainbowRun 2s linear infinite; opacity: 0; transition: opacity 0.25s; }
.stChatMessage:hover { border-color: #DADCE0 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important; transform: translateY(-1px); transition: all 0.2s; }
.stChatMessage:hover::after { opacity: 1; }
.stChatMessage p { color: #202124 !important; font-size: 15px !important; line-height: 1.7 !important; }

/* ===== INPUT GEMINI ALIVE ===== */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 400% 100% !important; animation: rainbowRun 2.2s linear infinite, inputAlive 2.8s ease-in-out infinite !important;
    padding: 2.2px !important; border-radius: 28px !important; box-shadow: 0 2px 14px rgba(66,133,244,0.16), 0 1px 3px rgba(0,0,0,0.05) !important; max-width: 740px !important; margin: 0 auto !important;
}
@keyframes inputAlive { 0%,100%{box-shadow: 0 2px 14px rgba(66,133,244,0.16); transform: scale(1)} 50%{box-shadow: 0 6px 24px rgba(66,133,244,0.24), 0 0 16px rgba(219,68,55,0.12); transform: scale(1.005)} }
[data-testid="stChatInput"] > div { background: #FFFFFF !important; border-radius: 26px !important; border: none !important; }
[data-testid="stChatInput"] textarea { color: #202124 !important; -webkit-text-fill-color: #202124 !important; font-size: 15.5px !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #80868B !important; -webkit-text-fill-color: #80868B !important; }
[data-testid="stChatInput"] button { background: linear-gradient(90deg, #4285F4, #9C27B0) !important; background-size: 200% 100% !important; animation: rainbowRun 2s linear infinite !important; border-radius: 50% !important; width: 34px !important; height: 34px !important; color: white !important; box-shadow: 0 2px 8px rgba(66,133,244,0.35) !important; }

/* ===== HP RESPONSIVE ===== */
@media (max-width: 768px) {
    h1 { font-size: 2.1rem !important; }
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
    st.markdown('<span class="badge-alive">SAVE NAME</span> <span class="badge-alive">GAUL</span>', unsafe_allow_html=True)
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
        <p style="color:#5F6368 !important; font-size:16px; margin-top:20px;">Gas tanya apa pun, aku siap bantu kok! 😎✨</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='text-align:center; color:#202124;'>{active['title']}</h2>", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="😎" if m["role"]=="user" else "🌈"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Mau tanya? Silahkan! {st.session_state.user_memory['nama'] or ''}."):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="😎"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌈"):
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
