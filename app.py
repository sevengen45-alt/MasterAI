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
html, body, .stApp { overflow-x: hidden !important; max-width: 100vw !important; }
[data-testid="stAppViewContainer"] { padding: 1rem 1rem 7rem 1rem !important; max-width: 100% !important; overflow-x: hidden !important; }
p, li, div, h1, h2, h3 { word-wrap: break-word !important; overflow-wrap: anywhere !important; max-width: 100% !important; }
table { display: block !important; width: 100% !important; max-width: 100% !important; overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; border-collapse: collapse !important; }
th, td { white-space: normal !important; word-break: break-word !important; min-width: 70px !important; padding: 8px 10px !important; }

/* ===== WHITE BASE + SUPER HEBOH ORB ===== */
.stApp { background: #FFFFFF !important; overflow: hidden; }
.stApp::before {
    content: ""; position: fixed; inset: -60%;
    background: 
        radial-gradient(ellipse 850px 700px at 10% 10%, rgba(66,133,244,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 750px 600px at 90% 15%, rgba(219,68,55,0.14) 0%, transparent 55%),
        radial-gradient(ellipse 1000px 700px at 50% 120%, rgba(15,157,88,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 700px 600px at 15% 85%, rgba(244,180,0,0.16) 0%, transparent 55%),
        radial-gradient(ellipse 650px 500px at 90% 80%, rgba(156,39,176,0.13) 0%, transparent 55%),
        radial-gradient(ellipse 500px 400px at 50% 50%, rgba(66,133,244,0.06) 0%, transparent 70%);
    animation: superOrb 12s ease-in-out infinite alternate; filter: blur(22px); z-index: 0; pointer-events: none;
}
@keyframes superOrb {
    0% { transform: translate(0,0) scale(1) rotate(0deg); filter: blur(22px) hue-rotate(0deg); }
    33% { transform: translate(-4%,5%) scale(1.15) rotate(2deg); filter: blur(26px) hue-rotate(10deg); }
    66% { transform: translate(4%,-3%) scale(0.95) rotate(-2deg); filter: blur(20px) hue-rotate(-10deg); }
    100% { transform: translate(-2%,-4%) scale(1.08) rotate(1deg); filter: blur(24px) hue-rotate(5deg); }
}
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; background: transparent !important; }

/* PARTIKEL PELANGI MELAYANG */
.stApp::after {
    content: "🌈 ✨ 🔵 🔴 🟡 🟢 🟣"; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    font-size: 18px; letter-spacing: 120px; line-height: 180px; white-space: pre-wrap;
    opacity: 0.04; animation: floatParticle 25s linear infinite; pointer-events: none; z-index: 0;
}
@keyframes floatParticle { 0%{transform: translateY(100vh)} 100%{transform: translateY(-100vh)} }

p, div, span { color: #202124 !important; }

/* ===== JUDUL SUPER HEBOH ===== */
h1 { text-align: center !important; font-weight: 400 !important; font-size: 3.6rem !important; line-height: 1.05 !important; color: #202124 !important; -webkit-text-fill-color: #202124 !important; }
h1 .rainbow-alive {
    background: linear-gradient(90deg, #4285F4, #EA4335, #FBBC05, #34A853, #9C27B0, #4285F4, #EA4335, #FBBC05) !important;
    background-size: 400% 100% !important; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; 
    animation: rainbowSuper 1.8s linear infinite, floatSuper 2s ease-in-out infinite alternate, glowRainbow 2s ease-in-out infinite alternate !important;
    font-weight: 800 !important; display: inline-block;
}
@keyframes rainbowSuper { 0%{background-position:0% 50%} 100%{background-position:400% 50%} }
@keyframes floatSuper { 0%{transform: translateY(0) rotate(0deg)} 50%{transform: translateY(-8px) rotate(0.5deg)} 100%{transform: translateY(-4px) rotate(-0.5deg)} }
@keyframes glowRainbow { 0%{filter: drop-shadow(0 2px 8px rgba(66,133,244,0.3))} 100%{filter: drop-shadow(0 6px 20px rgba(234,67,53,0.4))} }

.gemini-line { width: 140px; height: 5px; margin: 22px auto 0 auto; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4); background-size: 400% 100%; animation: rainbowSuper 1.5s linear infinite, linePulse 1.5s ease-in-out infinite alternate; border-radius: 100px; }
@keyframes linePulse { 0%{transform: scaleX(0.8); box-shadow: 0 2px 10px rgba(66,133,244,0.3)} 100%{transform: scaleX(1.2); box-shadow: 0 4px 20px rgba(219,68,55,0.4)} }

/* SIDEBAR */
section[data-testid="stSidebar"] { background: #F8F9FA !important; border-right: 1px solid #E8EAED !important; }
section[data-testid="stSidebar"] * { color: #202124 !important; }

/* BADGE SUPER ALIVE MANTUL-MANTUL */
.badge-alive { 
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important; 
    background-size: 400% 100% !important; animation: rainbowSuper 1.5s linear infinite, badgeBounce 1.2s ease-in-out infinite alternate !important; 
    color: white !important; padding: 7px 14px; border-radius: 100px; font-size: 11px; font-weight: 800; letter-spacing: 0.6px; display: inline-block; margin: 4px; 
    box-shadow: 0 3px 12px rgba(66,133,244,0.3), 0 0 0 1px rgba(255,255,255,0.5) inset;
}
@keyframes badgeBounce { 0%{transform: translateY(0) scale(1)} 100%{transform: translateY(-4px) scale(1.05)} }

/* CHAT BUBBLE SUPER ALIVE */
.stChatMessage { 
    background: rgba(255,255,255,0.92) !important; backdrop-filter: blur(8px) !important;
    border: 1px solid #E8EAED !important; border-radius: 22px !important; 
    box-shadow: 0 2px 12px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.04) !important; 
    max-width: 720px !important; margin: 14px auto !important; position: relative; overflow: hidden; 
    animation: popSuper 0.6s cubic-bezier(0.34,1.56,0.64,1) !important; 
}
@keyframes popSuper { 0%{opacity:0; transform: translateY(15px) scale(0.92)} 60%{transform: translateY(-4px) scale(1.02)} 100%{opacity:1; transform: translateY(0) scale(1)} }
.stChatMessage::before {
    content: ""; position: absolute; top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4);
    background-size: 400% 100%; animation: rainbowSuper 2s linear infinite;
    border-radius: 22px; z-index: -1; opacity: 0; transition: opacity 0.3s;
}
.stChatMessage:hover::before { opacity: 0.15; }
.stChatMessage::after { content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4); background-size: 400% 100%; animation: rainbowSuper 1.5s linear infinite; }
.stChatMessage:hover { border-color: #DADCE0 !important; box-shadow: 0 8px 24px rgba(0,0,0,0.08), 0 0 20px rgba(66,133,244,0.1) !important; transform: translateY(-2px) scale(1.005); }
.stChatMessage p { color: #202124 !important; font-size: 15.5px !important; line-height: 1.7 !important; }

/* INPUT SUPER HEBOH BERNAFAS + GLOW */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4, #4285F4) !important;
    background-size: 500% 100% !important; animation: rainbowSuper 1.5s linear infinite, inputSuper 2s ease-in-out infinite !important;
    padding: 3px !important; border-radius: 30px !important; box-shadow: 0 4px 20px rgba(66,133,244,0.2), 0 0 0 1px rgba(255,255,255,0.8) inset !important; max-width: 740px !important; margin: 0 auto !important;
}
@keyframes inputSuper { 
    0%,100%{box-shadow: 0 4px 20px rgba(66,133,244,0.2), 0 0 15px rgba(66,133,244,0.1); transform: scale(1) rotate(0deg)} 
    25%{box-shadow: 0 8px 30px rgba(219,68,55,0.25), 0 0 20px rgba(244,180,0,0.15); transform: scale(1.01) rotate(0.2deg)} 
    50%{box-shadow: 0 10px 35px rgba(15,157,88,0.25), 0 0 25px rgba(156,39,176,0.15); transform: scale(1.015) rotate(0deg)} 
    75%{box-shadow: 0 8px 30px rgba(244,180,0,0.25), 0 0 20px rgba(66,133,244,0.15); transform: scale(1.01) rotate(-0.2deg)} 
}
[data-testid="stChatInput"] > div { background: #FFFFFF !important; border-radius: 27px !important; border: none !important; }
[data-testid="stChatInput"] textarea { color: #202124 !important; -webkit-text-fill-color: #202124 !important; font-size: 16px !important; font-weight: 500 !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #80868B !important; -webkit-text-fill-color: #80868B !important; }
[data-testid="stChatInput"] button { 
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437) !important; background-size: 300% 100% !important; 
    animation: rainbowSuper 1.2s linear infinite, buttonPulse 1s ease-in-out infinite alternate !important; 
    border-radius: 50% !important; width: 38px !important; height: 38px !important; color: white !important; 
    box-shadow: 0 3px 12px rgba(66,133,244,0.4) !important; 
}
@keyframes buttonPulse { 0%{transform: scale(1)} 100%{transform: scale(1.1)} }

@media (max-width: 768px) {
    h1 { font-size: 2.2rem !important; }
    .stChatMessage { max-width: 100% !important; margin: 12px 0 !important; }
    [data-testid="stChatInput"] { max-width: 96% !important; position: fixed !important; bottom: 14px !important; left: 2% !important; right: 2% !important; z-index: 999 !important; }
    [data-testid="stAppViewContainer"] { padding-bottom: 8rem !important; }
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ===== SAVE MEMORY - TETAP SAMA =====
if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Ngobrol?", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI 🇮🇩")
    st.markdown('<span class="badge-alive">SUPER ALIVE</span> <span class="badge-alive">HEBOH</span> <span class="badge-alive">🌈</span>', unsafe_allow_html=True)
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
    <div style="text-align:center; padding: 50px 20px 10px 20px; max-width:720px; margin:0 auto;">
        <h1>Yo {st.session_state.user_memory['nama'] or 'Bang'}, Mau<br><span class="rainbow-alive">Ngobrolin Apa?</span></h1>
        <div class="gemini-line"></div>
        <p style="color:#5F6368 !important; font-size:16px; margin-top:20px;">White-Rainbow Super Alive nih bang! 🌈💥 Gas tanya!</p>
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
