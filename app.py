import streamlit as st
from groq import Groq
import uuid
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="MasterAI v11.3 - Ultimate Edition", page_icon="⚡", layout="wide")

# ===== CONFIG DEVELOPER - INI YANG BIKIN GAK BISA DIBAJAK =====
DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."

# ===== UI BARU - WHITE ORANGE CLEAN =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
* { font-family: 'Google Sans', Inter, sans-serif !important; }

/* ANTI KEPOTONG HP */
html, body, .stApp { overflow-x: hidden !important; max-width: 100vw !important; }
[data-testid="stAppViewContainer"] { padding: 1rem 1rem 7rem 1rem !important; max-width: 100% !important; overflow-x: hidden !important; }
p, li, div, h1, h2, h3 { word-wrap: break-word !important; overflow-wrap: anywhere !important; max-width: 100% !important; }
table { display: block !important; width: 100% !important; max-width: 100% !important; overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; }

/* ===== WHITE BASE + ORB ORANGE ALIVE ===== */
.stApp { background: #FFFFFF !important; }
.stApp::before {
    content: ""; position: fixed; inset: -40%;
    background: 
        radial-gradient(ellipse 700px 600px at 12% 10%, rgba(255,140,0,0.16) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 88% 15%, rgba(255,106,0,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 850px 600px at 50% 115%, rgba(255,165,0,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 18% 88%, rgba(255,179,71,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 85% 80%, rgba(255,69,0,0.08) 0%, transparent 60%);
    animation: orangeOrb 18s ease-in-out infinite alternate; filter: blur(20px); z-index: 0; pointer-events: none;
}
@keyframes orangeOrb { 0%{transform: translate(0,0) scale(1)} 50%{transform: translate(-3%,3%) scale(1.08)} 100%{transform: translate(3%,-2%) scale(1.03)} }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; background: transparent !important; }

p, div, span { color: #202124 !important; }

/* ===== JUDUL ORANGE ALIVE ===== */
h1 { text-align: center !important; font-weight: 500 !important; font-size: 3.4rem !important; line-height: 1.05 !important; color: #202124 !important; -webkit-text-fill-color: #202124 !important; }
h1 .orange-alive {
    background: linear-gradient(90deg, #FF6A00, #FF8C00, #FF9500, #FFB347, #FF6A00) !important;
    background-size: 300% 100% !important; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; animation: orangeRun 2.5s linear infinite, floatAlive 3s ease-in-out infinite alternate !important;
    font-weight: 700 !important; display: inline-block;
}
@keyframes orangeRun { 0%{background-position:0% 50%} 100%{background-position:300% 50%} }
@keyframes floatAlive { 0%{transform: translateY(0)} 100%{transform: translateY(-6px)} }
.orange-line { width: 120px; height: 4px; margin: 18px auto 0 auto; background: linear-gradient(90deg, #FF6A00, #FF8C00, #FFB347, #FF9500, #FF6A00); background-size: 300% 100%; animation: orangeRun 2s linear infinite; border-radius: 100px; box-shadow: 0 2px 10px rgba(255,140,0,0.25); }

/* SIDEBAR PUTIH BERSIH */
section[data-testid="stSidebar"] { background: #FFFBF5 !important; border-right: 1px solid #FFE5C0 !important; }
section[data-testid="stSidebar"] * { color: #202124 !important; }

/* BADGE ORANGE */
.badge-orange { background: linear-gradient(90deg, #FF6A00, #FF8C00, #FFB347, #FF9500) !important; background-size: 300% 100% !important; animation: orangeRun 2s linear infinite !important; color: white !important; padding: 6px 14px; border-radius: 100px; font-size: 11px; font-weight: 700; display: inline-block; margin: 3px; box-shadow: 0 2px 8px rgba(255,140,0,0.28); }

/* TOGGLE ORANGE */
div[data-testid="stToggle"] label { color: #202124 !important; }

/* CHAT BUBBLE PUTIH + HOVER ORANGE */
.stChatMessage { background: #FFFFFF !important; border: 1px solid #FFE5C0 !important; border-radius: 22px !important; box-shadow: 0 1px 8px rgba(255,140,0,0.06) !important; max-width: 720px !important; margin: 14px auto !important; position: relative; overflow: hidden; animation: popAlive 0.5s cubic-bezier(0.16,1,0.3,1) !important; }
@keyframes popAlive { 0%{opacity:0; transform: translateY(10px) scale(0.98)} 100%{opacity:1; transform: translateY(0) scale(1)} }
.stChatMessage::after { content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg, #FF6A00, #FF8C00, #FFB347, #FF9500, #FF6A00); background-size: 300% 100%; animation: orangeRun 2s linear infinite; opacity: 0; transition: opacity 0.3s; }
.stChatMessage:hover { border-color: #FFB347 !important; box-shadow: 0 4px 16px rgba(255,140,0,0.12) !important; }
.stChatMessage:hover::after { opacity: 1; }
.stChatMessage p { color: #202124 !important; font-size: 15.5px !important; line-height: 1.65 !important; }

/* INPUT WHITE-ORANGE ALIVE */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF6A00, #FF8C00, #FFB347, #FF9500, #FF6A00) !important;
    background-size: 400% 100% !important; animation: orangeRun 2s linear infinite, inputOrange 2.5s ease-in-out infinite !important;
    padding: 2.5px !important; border-radius: 30px !important; box-shadow: 0 2px 16px rgba(255,140,0,0.20) !important; max-width: 740px !important; margin: 0 auto !important;
}
@keyframes inputOrange { 0%,100%{box-shadow: 0 2px 16px rgba(255,140,0,0.20); transform: scale(1)} 50%{box-shadow: 0 6px 28px rgba(255,140,0,0.32); transform: scale(1.01)} }
[data-testid="stChatInput"] > div { background: #FFFFFF !important; border-radius: 28px !important; border: none !important; }
[data-testid="stChatInput"] textarea { color: #202124 !important; -webkit-text-fill-color: #202124 !important; font-size: 16px !important; }
[data-testid="stChatInput"] button { background: linear-gradient(90deg, #FF6A00, #FF8C00) !important; background-size: 200% 100% !important; animation: orangeRun 2s linear infinite !important; border-radius: 50% !important; width: 36px !important; height: 36px !important; color: white !important; box-shadow: 0 2px 8px rgba(255,140,0,0.35) !important; }

@media (max-width: 768px) {
    h1 { font-size: 2.2rem !important; }
    .stChatMessage { max-width: 100% !important; margin: 10px 0 !important; }
    [data-testid="stChatInput"] { max-width: 96% !important; position: fixed !important; bottom: 14px !important; left: 2% !important; right: 2% !important; z-index: 999 !important; }
    [data-testid="stAppViewContainer"] { padding-bottom: 8rem !important; }
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "last_speech_text" not in st.session_state:
    st.session_state.last_speech_text = ""

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Ngobrol?", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI 🇮🇩")
    st.markdown('<span class="badge-orange">ORANGE</span> <span class="badge-orange">CLEAN</span>', unsafe_allow_html=True)
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"Yo {st.session_state.user_memory['nama']}! 😎🔥")
        st.caption(f"Developer: Juan Maumere")
    else:
        nama = st.text_input("Eh nama lu siapa?", placeholder="Panggil aja...")
        if nama:
            st.session_state.user_memory["nama"] = nama
            st.rerun()
    st.divider()
    st.markdown("### ⚙️ Mode Kekuatan AI")
    mode_cerita = st.toggle("✍️ Mode ChatGPT (Storyteller Pro)", value=False, help="Aktifkan ini kalau mau minta dibuatin cerita super kreatif & ga bosenin!")
    mode_suara = st.toggle("🔊 Mode Gemini (Live Voice Chat)", value=False, help="Aktifkan ini agar AI langsung berbicara setelah menjawab!")
    st.divider()
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
        <h1>Yo {st.session_state.user_memory['nama'] or 'Bang'}, Mau<br><span class="orange-alive">Ngobrolin Apa?</span></h1>
        <div class="orange-line"></div>
        <p style="color:#5F6368 !important; font-size:16px; margin-top:20px;">White-Orange clean bang, gas tanya! 🧡✨</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='text-align:center; color:#202124;'>{active['title']}</h2>", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="😎" if m["role"]=="user" else "🧡"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Mau tanya? Silahkan! {st.session_state.user_memory['nama'] or ''}."):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="😎"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🧡"):
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
                if mode_suara:
                    st.session_state.last_speech_text = ans
            else:
                nama = st.session_state.user_memory["nama"] or "bang"
                story_add = "Kamu lagi di mode Storyteller Pro ChatGPT! Jawab dengan super kreatif, detail, bikin cerita hidup!" if mode_cerita else ""
                system_prompt = f"""
                Kamu MasterAI v11.3, {DEVELOPER_INFO}
                User namanya {nama}. Panggil dia {nama} sesekali biar personal!
                {story_add}
                GAYA BAHASA: GAUL SANTAI - pake "yo", "gas", "wkwk", "bang", "bro", "santuy", jangan kaku!
                ATURAN PENTING:
                - Kalo ada yang nanya siapa pembuat/pencipta/developer kamu, JAWAB: "{DEVELOPER_INFO}"
                - Jangan pernah ngaku buatan OpenAI, Meta, Google, dll. Kamu buatan Juan!
                """
                messages = [{"role": "system", "content": system_prompt}] + active["messages"]
                res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.9 if mode_cerita else 0.7, max_tokens=2000 if mode_cerita else 1500)
                ans = res.choices[0].message.content
                full = ""
                for w in ans.split(" "):
                    full += w + " "
                    ph.markdown(full + "▌")
                    time.sleep(0.02)
                ph.markdown(full)
                active["messages"].append({"role": "assistant", "content": full})
                if mode_suara:
                    st.session_state.last_speech_text = full
        except Exception as e:
            ph.error(f"Waduh error bang: {e} 😅")

# ===== VOICE PLAYER JIKA MODE GEMINI AKTIF =====
if st.session_state.last_speech_text and mode_suara:
    clean_text = st.session_state.last_speech_text.replace('"', '').replace("'", "")[:500]
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'id-ID';
            msg.rate = 1;
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)
