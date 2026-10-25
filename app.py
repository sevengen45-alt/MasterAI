import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v11.3 - Save Name", page_icon="⚡", layout="wide")

DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
* { font-family: 'Google Sans', system-ui, sans-serif !important; }

/* ANTI KEPOTONG HP */
html, body, .stApp { overflow-x: hidden !important; }
[data-testid="stAppViewContainer"] { padding: 1rem 1rem 7rem 1rem !important; }
p, li, div { word-wrap: break-word !important; overflow-wrap: anywhere !important; }
table { display: block !important; max-width: 100% !important; overflow-x: auto !important; }

/* WHITE + ORB HALUS */
.stApp { background: #FFFFFF !important; }
.stApp::before {
    content: ""; position: fixed; inset: -35%;
    background: 
        radial-gradient(ellipse 600px 500px at 10% 15%, rgba(66,133,244,0.11) 0%, transparent 60%),
        radial-gradient(ellipse 550px 450px at 90% 20%, rgba(219,68,55,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 800px 500px at 50% 110%, rgba(15,157,88,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 550px 400px at 20% 85%, rgba(244,180,0,0.10) 0%, transparent 60%);
    animation: orbSoft 20s ease-in-out infinite alternate; filter: blur(18px); z-index: 0; pointer-events: none;
}
@keyframes orbSoft { 0%{transform: translate(0,0) scale(1)} 100%{transform: translate(-2%,3%) scale(1.05)} }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; background: transparent !important; }
p, div, span { color: #202124 !important; }

/* JUDUL - SEDIKIT UBAH LEBIH TIPIS & ELEGAN */
h1 { text-align: center !important; font-weight: 400 !important; font-size: 3.2rem !important; line-height: 1.1 !important; letter-spacing: -0.02em !important; color: #202124 !important; -webkit-text-fill-color: #202124 !important; }
h1 .rainbow-alive {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 250% 100% !important; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; animation: rainbowMove 3s linear infinite !important;
    font-weight: 600 !important; display: inline-block;
}
@keyframes rainbowMove { 0%{background-position:0% 50%} 100%{background-position:250% 50%} }
.gemini-line { width: 80px; height: 3px; margin: 16px auto 0 auto; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58); background-size: 250% 100%; animation: rainbowMove 2s linear infinite; border-radius: 100px; opacity: 0.9; }

/* SIDEBAR - LEBIH BERSIH */
section[data-testid="stSidebar"] { background: #F8F9FA !important; border-right: 1px solid #E8EAED !important; }
section[data-testid="stSidebar"] * { color: #202124 !important; }

/* BADGE - SEDIKIT UBAH JADI LEBIH KECIL & SOFT */
.badge-alive { background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important; background-size: 250% 100% !important; animation: rainbowMove 2.5s linear infinite !important; color: white !important; padding: 5px 12px; border-radius: 100px; font-size: 10px; font-weight: 700; display: inline-block; margin: 3px; opacity: 0.95; }

/* CHAT BUBBLE - SEDIKIT UBAH JADI LEBIH TIPIS & RAPI */
.stChatMessage { background: #FFFFFF !important; border: 1px solid #E8EAED !important; border-radius: 18px !important; box-shadow: none !important; max-width: 700px !important; margin: 10px auto !important; animation: fadeIn 0.4s ease !important; }
@keyframes fadeIn { 0%{opacity:0; transform: translateY(6px)} 100%{opacity:1; transform: translateY(0)} }
.stChatMessage:hover { border-color: #DADCE0 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important; }
.stChatMessage::after { content: ""; position: absolute; bottom: 0; left: 20%; right: 20%; height: 2px; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4); background-size: 250% 100%; animation: rainbowMove 2s linear infinite; border-radius: 100px; opacity: 0; transition: opacity 0.3s; }
.stChatMessage:hover::after { opacity: 1; }
.stChatMessage p { color: #202124 !important; font-size: 15px !important; line-height: 1.65 !important; }

/* INPUT - SEDIKIT UBAH JADI LEBIH TIPIS TAPI TETEP PELANGI */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 300% 100% !important; animation: rainbowMove 2s linear infinite !important;
    padding: 2px !important; border-radius: 24px !important; box-shadow: 0 1px 6px rgba(0,0,0,0.08) !important; max-width: 700px !important; margin: 0 auto !important;
}
[data-testid="stChatInput"] > div { background: #FFFFFF !important; border-radius: 22px !important; border: none !important; }
[data-testid="stChatInput"] textarea { color: #202124 !important; -webkit-text-fill-color: #202124 !important; font-size: 15px !important; }
[data-testid="stChatInput"] button { background: #202124 !important; border-radius: 50% !important; width: 32px !important; height: 32px !important; color: white !important; }

@media (max-width: 768px) {
    h1 { font-size: 2rem !important; }
    .stChatMessage { max-width: 100% !important; margin: 8px 0 !important; }
    [data-testid="stChatInput"] { max-width: 96% !important; position: fixed !important; bottom: 12px !important; left: 2% !important; right: 2% !important; z-index: 999 !important; }
    [data-testid="stAppViewContainer"] { padding-bottom: 7rem !important; }
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Ngobrol?", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI 🇮🇩")
    st.markdown('<span class="badge-alive">WHITE</span> <span class="badge-alive">RAINBOW</span>', unsafe_allow_html=True)
    st.divider()
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
    <div style="text-align:center; padding: 50px 20px 10px 20px; max-width:700px; margin:0 auto;">
        <h1>Yo {st.session_state.user_memory['nama'] or 'Bang'}, Mau<br><span class="rainbow-alive">Ngobrolin Apa?</span></h1>
        <div class="gemini-line"></div>
        <p style="color:#5F6368 !important; font-size:15px; margin-top:18px;">Gas tanya apa pun, aku siap bantu kok! 😎✨</p>
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
            lower_prompt = prompt.lower()
            is_ask_developer = any(k in lower_prompt for k in [
                "siapa yang membuat", "siapa pembuat", "siapa yg membuat", "siapa yg buat",
                "who made you", "who created you", "dibuat siapa", "buatan siapa",
                "siapa developer", "siapa yang bikin", "kamu dibuat siapa",
                "kamu buatan siapa", "siapa pencipta"
            ])
            if is_ask_developer:
                ans = DEVELOPER_INFO + f" Btw, lu kah {st.session_state.user_memory['nama'] or 'bang?'}😎"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
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
