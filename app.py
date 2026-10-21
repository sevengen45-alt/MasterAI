import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v20 - Ultimate Combine", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important; }

/* ===== 1 & 5. FIX KONTRAST - PAKSA HITAM PEKAT + BG PUTIH APPLE ===== */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], p, div, span, li, h1, h2, h3, h4 {
    color: #000000 !important;
}
.stApp { background: #FEFEFF !important; }
.stApp::before {
    content: ""; position: fixed; inset: 0;
    background: 
        radial-gradient(1200px at 10% -10%, rgba(255,45,85,0.04) 0%, transparent 60%),
        radial-gradient(1200px at 90% -10%, rgba(255,204,0,0.035) 0%, transparent 60%),
        radial-gradient(1000px at 50% 110%, rgba(0,122,255,0.03) 0%, transparent 60%);
    pointer-events: none; z-index: -1;
}

/* ===== 3 & 6. HEADER PREMIUM ===== */
.premium-header { max-width: 760px; margin: 0 auto; padding: 48px 24px 32px 24px; text-align: center; }
.premium-title {
    font-size: 3.25rem !important; font-weight: 900 !important; letter-spacing: -0.05em !important;
    line-height: 0.95 !important; color: #000000 !important; margin: 0 !important; display: inline-block;
}
.premium-title-gradient {
    background: linear-gradient(90deg, #FF2D55, #FF9500, #FFCC00, #34C759, #007AFF, #AF52DE, #FF2D55) !important;
    background-size: 300% 100% !important; -webkit-background-clip: text !important; background-clip: text !important; 
    -webkit-text-fill-color: transparent !important; color: transparent !important;
    animation: premiumRainbow 8s linear infinite !important;
}
@keyframes premiumRainbow { 0%{background-position:0%} 100%{background-position:300%} }
.premium-underline {
    width: 72px; height: 4px; margin: 20px auto 0 auto;
    background: linear-gradient(90deg, #FF2D55, #FF9500, #FFCC00, #34C759, #007AFF, #AF52DE) !important;
    background-size: 300% 100%; animation: premiumRainbow 8s linear infinite; border-radius: 100px;
}
.premium-sub { margin-top: 16px; font-size: 13px !important; font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; color: #000000 !important; opacity: 0.4; }

/* ===== SIDEBAR PREMIUM + RAINBOW 1.5PX ===== */
section[data-testid="stSidebar"] {
    background: rgba(249,249,251,0.9) !important; backdrop-filter: blur(40px) saturate(200%) !important;
    border-right: 0.5px solid rgba(0,0,0,0.08) !important;
}
section[data-testid="stSidebar"] * { color: #000000 !important; }
section[data-testid="stSidebar"]::after {
    content: ""; position: absolute; top: 0; right: 0; width: 1.5px; height: 100%;
    background: linear-gradient(180deg, #FF2D55, #FF9500, #FFCC00, #34C759, #007AFF, #AF52DE);
    background-size: 100% 400%; animation: sidebarFlow 10s linear infinite; opacity: 0.7;
}
@keyframes sidebarFlow { 0%{background-position:0% 0%} 100%{background-position:0% 400%} }
section[data-testid="stSidebar"] .stButton button {
    background: #FFFFFF !important; border: 1px solid rgba(0,0,0,0.1) !important;
    border-radius: 10px !important; font-weight: 600 !important; color: #000000 !important; text-align: left !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}

/* ===== CHAT - KONTRAST HITAM + CARD PREMIUM ===== */
.stChatMessage { max-width: 720px !important; margin: 0 auto !important; background: transparent !important; border: none !important; }
div[data-testid="stChatMessageContent"] {
    background: #FFFFFF !important; border: 1.5px solid rgba(0,0,0,0.1) !important;
    border-radius: 20px !important; padding: 16px 20px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}
.stChatMessage p, .stChatMessage div { color: #000000 !important; font-size: 16px !important; font-weight: 500 !important; line-height: 1.65 !important; }
.stChatMessage[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stChatMessageContent"] {
    background: #F5F5F7 !important;
}

/* ===== 2 & 4. TASKBAR PELANGI LIVE 2.5 DETIK + PLACEHOLDER PELANGI ===== */
div[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF2D55, #FF9500, #FFCC00, #34C759, #007AFF, #AF52DE, #FF2D55) !important;
    background-size: 500% 100% !important;
    animation: taskbarRainbowLive 2.5s linear infinite !important;
    padding: 3px !important; border-radius: 26px !important; max-width: 720px !important;
    margin: 0 auto !important; bottom: 28px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12), 0 0 30px rgba(255,45,85,0.12), 0 0 60px rgba(0,122,255,0.08) !important;
}
@keyframes taskbarRainbowLive { 0%{background-position:0% 50%} 100%{background-position:200% 50%} }
div[data-testid="stChatInput"] > div { background: #FFFFFF !important; border-radius: 24px !important; padding: 6px 8px 6px 20px !important; }
div[data-testid="stChatInput"] textarea { color: #000000 !important; -webkit-text-fill-color: #000000 !important; font-weight: 600 !important; font-size: 16px !important; }
div[data-testid="stChatInput"] textarea::placeholder {
    background: linear-gradient(90deg, #FF2D55, #FF9500, #FFCC00, #34C759, #007AFF, #AF52DE, #FF2D55) !important;
    background-size: 300% 100% !important; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; color: transparent !important;
    font-weight: 700 !important; animation: placeholderRainbow 3s linear infinite !important;
}
@keyframes placeholderRainbow { 0%{background-position:0%} 100%{background-position:300%} }
div[data-testid="stChatInput"] button { background: #000000 !important; border-radius: 50% !important; width: 36px !important; height: 36px !important; }
div[data-testid="stChatInput"] button * { color: white !important; }
</style>
""", unsafe_allow_html=True)

DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Memulai Obrolan?", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown('<div style="font-weight:800; font-size:13px; color:black !important;">✦ MasterAI • ULTIMATE</div>', unsafe_allow_html=True)
    st.markdown("## ")
    if st.session_state.user_memory["nama"]:
        st.markdown(f"<b style='color:black !important;'>👋 {st.session_state.user_memory['nama']}</b>", unsafe_allow_html=True)
    else:
        nama_input = st.text_input("Nama", placeholder="Your name", label_visibility="collapsed")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()
    if st.button("＋ New conversation", use_container_width=True):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": "New conversation", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.divider()
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True)[:10]:
        if st.button(f"{chat['title'][:26]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.markdown(f"""
<div class="premium-header">
    <h1 class="premium-title">Siap Memulai<br><span class="premium-title-gradient">Obrolan?</span></h1>
    <div class="premium-underline"></div>
    <div class="premium-sub">White • Rainbow Live • Premium • Fixed Contrast • by Juan</div>
</div>
""", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(f"<div style='color:black !important;'>{m['content']}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("Tanya apa saja! 👨🏼‍💻✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:40]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(f"<div style='color:black !important;'>{prompt}</div>", unsafe_allow_html=True)
    with st.chat_message("assistant"):
        ph = st.empty()
        try:
            nama = st.session_state.user_memory["nama"] or "there"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = DEVELOPER_INFO
                ph.markdown(f"<div style='color:black !important;'>{ans}</div>", unsafe_allow_html=True)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v20 Ultimate. Pembuat: {DEVELOPER_INFO}. User: {nama}. Gaya premium helpful."
                messages = [{"role": "system", "content": system_prompt}] + active["messages"]
                res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.6, max_tokens=1500)
                ans = res.choices[0].message.content
                full = ""
                for w in ans.split(" "):
                    full += w + " "
                    ph.markdown(f"<div style='color:black !important;'>{full}▌</div>", unsafe_allow_html=True)
                    time.sleep(0.012)
                ph.markdown(f"<div style='color:black !important;'>{full}</div>", unsafe_allow_html=True)
                active["messages"].append({"role": "assistant", "content": full})
        except Exception as e:
            ph.error(f"Error: {e}")
