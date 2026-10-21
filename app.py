import streamlit as st
from groq import Groq
import uuid, time
st.set_page_config(page_title="MasterAI v14 - Rainbow Elegan", page_icon="🌈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}

.stApp {
    background: #08080A !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(255,0,85,0.25) 0%, transparent 50%),
        radial-gradient(at 100% 0%, rgba(255,171,0,0.2) 0%, transparent 50%),
        radial-gradient(at 50% 50%, rgba(0,230,118,0.15) 0%, transparent 60%),
        radial-gradient(at 0% 100%, rgba(41,121,255,0.25) 0%, transparent 50%),
        radial-gradient(at 100% 100%, rgba(170,0,255,0.25) 0%, transparent 50%) !important;
    animation: bgSlow 20s ease infinite alternate !important;
}
@keyframes bgSlow { 0%{filter:hue-rotate(0deg)} 100%{filter:hue-rotate(20deg)} }

.live-rainbow-title {
    background: linear-gradient(90deg, #FF0055, #FFAB00, #00E676, #2979FF, #AA00FF, #FF0055) !important;
    background-size: 400% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 900 !important; font-size: 4.8rem !important; text-align: center !important;
    animation: rainbowSlow 5s linear infinite !important;
}
@keyframes rainbowSlow { 0%{background-position:0%} 100%{background-position:400%} }
@media (max-width: 600px) { .live-rainbow-title {font-size: 2.8rem !important;} }

[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0055, #FFAB00, #00E676, #2979FF, #AA00FF, #FF0055) !important;
    background-size: 500% 100% !important;
    animation: rainbowSlow 3s linear infinite !important;
    padding: 3px !important; border-radius: 28px !important;
    box-shadow: 0 0 25px rgba(170,0,255,0.3), 0 0 50px rgba(41,121,255,0.15) !important;
}
[data-testid="stChatInput"] > div { background: #121214 !important; border-radius: 25px !important; }
[data-testid="stChatInput"] textarea { color: white !important; }

.badge {
    background: linear-gradient(90deg, #FF0055, #2979FF) !important;
    background-size: 200% 100% !important;
    animation: rainbowSlow 4s linear infinite !important;
    padding: 5px 12px; border-radius: 20px; color: white; font-weight: 800; font-size: 11px; margin: 3px; display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# === OTAK TETAP SAMA ===
DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Memulai Obrolan!", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid
def get_active(): return st.session_state.chats[st.session_state.active_chat]
active = get_active()
st.markdown(f"<h1 class='live-rainbow-title'>{active['title']}</h1>", unsafe_allow_html=True)
# ... LANJUTAN KODE LU YANG LAMA (sidebar + chat loop) ...
