import streamlit as st
from groq import Groq
import uuid
import time
import requests
from datetime import datetime

st.set_page_config(page_title="MasterAI v11.4 - 2026 Updated", page_icon="🌐", layout="wide")

DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! 15 tahun, SMAK St. Maria Monte Carmelo Maumere, panggilan Juan."
DEVELOPER_BIO = {
    "nama": "Jonathan Kristian Sergio Marut", "panggilan": "Juan", "umur": "15 Tahun",
    "sekolah": "SMAK St. Maria Monte Carmelo Maumere", "role": "AI Developer", "lokasi": "Maumere, NTT 🇮🇩"
}

# ===== TEKNOLOGI SEARCH 2026 - WAJIB INI! =====
def search_2026(query):
    """Searching real-time biar tau data 2026"""
    try:
        from duckduckgo_search import DDGS
        results = ""
        with DDGS() as ddgs:
            # Cari yang terbaru - add tahun 2026 biar akurat
            search_q = f"{query} 2026 latest news"
            data = list(ddgs.text(search_q, max_results=5))
            for i, r in enumerate(data, 1):
                results += f"{i}. {r['title']}: {r['body']} ({r['href']})\n\n"
            
            # Juga cari news khusus
            news = list(ddgs.news(search_q, max_results=3))
            for n in news:
                results += f"NEWS: {n['title']}: {n['body']} ({n['url']})\n\n"
        return results if results else "No result"
    except Exception as e:
        return f"Search error: {e} - but current date is 2026"

def is_need_search(prompt):
    keywords = ["apakah benar", "sudah wafat", "meninggal", "berita", "hari ini", "terbaru", "2025", "2026", "sekarang", "update", "el mencho", "presiden", "harga", "skor", "cuaca"]
    return any(k in prompt.lower() for k in keywords)

# ===== UI LIGHT =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}
.stApp { background: #0A0A12 !important; }
h1 { background: linear-gradient(90deg, #FF0040, #FFE600, #00F5FF) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; text-align: center !important; font-weight: 800 !important; font-size: 3.5rem !important; }
section[data-testid="stSidebar"] { background: #12121E !important; }
.stChatMessage { background: #181828 !important; border-radius: 16px !important; border: 1px solid rgba(255,255,255,0.08) !important; max-width: 720px !important; margin: 10px auto !important; }
.stChatMessage p { color: #E8E8F0 !important; }
.badge { background: #00F5FF !important; color: #000 !important; padding: 5px 12px; border-radius: 20px; font-size: 10px; font-weight: 800; display: inline-block; margin: 2px; }
[data-testid="stChatInput"] { background: #2A2A3A !important; border: 1px solid #3A3A4A !important; border-radius: 20px !important; max-width: 700px !important; margin: 0 auto !important; }
[data-testid="stChatInput"] > div { background: #16161F !important; border-radius: 18px !important; }
[data-testid="stChatInput"] textarea { color: #FFF !important; }
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
    st.markdown("### MasterAI 🌐 2026")
    st.markdown('<span class="badge">UPDATED 2026</span> <span class="badge">REAL-TIME</span>', unsafe_allow_html=True)
    st.divider()
    st.caption(f"👨‍💻 {DEVELOPER_BIO['nama']} - {DEVELOPER_BIO['umur']}")
    st.markdown("### ⚙️ Mode 2026")
    mode_search = st.toggle("🌐 Google Real-Time 2026", value=True, help="WAJIB AKTIF biar data gak stuck 2024!")
    st.info(f"📅 Hari ini: {datetime.now().strftime('%d %B %Y')} \nAI cutoff 2024, tapi search akan update ke 2026!")
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.success(f"Yo {st.session_state.user_memory['nama']}!")
    else:
        nama = st.text_input("Nama lu?", placeholder="Juan")
        if nama:
            st.session_state.user_memory["nama"] = nama
            st.rerun()
    if st.button("➕ Baru", use_container_width=True):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()

active = get_active()
st.title(active["title"])

# Tampilkan tanggal
st.markdown(f"<div style='text-align:center; color:#00F5FF; font-size:12px; margin-bottom:15px;'>🌐 Live Data: {datetime.now().strftime('%d %B %Y')} | Model + Google Search 2026</div>", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="👤" if m["role"]=="user" else "🌐"):
        st.markdown(m["content"])

if prompt := st.chat_input(f"Tanya apa? (auto update 2026) 🔍"):
    if len(active["messages"]) == 0: active["title"] = prompt[:30]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌐"):
        ph = st.empty()
        ph.markdown("🌐 _Cek data terbaru 2026..._")
        try:
            if any(k in prompt.lower() for k in ["siapa yang membuat","siapa pembuat","dibuat siapa"]):
                ans = DEVELOPER_INFO
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                # ===== FIX UTAMA: SELALU SEARCH KALO BUTUH DATA TERBARU =====
                search_data = ""
                if mode_search and is_need_search(prompt):
                    ph.markdown("🔍 _Searching Google untuk data 2026 terbaru..._")
                    search_data = search_2026(prompt)
                    with st.expander("🌐 Sumber Real-Time 2026", expanded=False):
                        st.text(search_data[:1500])

                # Inject tanggal 2026 biar AI sadar sekarang 2026!
                now = datetime.now()
                system_prompt = f"""
                Kamu MasterAI v11.4 UPDATED 2026!
                {DEVELOPER_INFO}
                User: {st.session_state.user_memory['nama'] or 'bang'}
                
                PENTING - TANGGAL SEKARANG:
                Hari ini adalah {now.strftime('%d %B %Y')}, tahun 2026!
                Model kamu cutoff Juni 2024, TAPI kamu sekarang punya akses GOOGLE SEARCH REAL-TIME!
                
                JADI:
                - JANGAN bilang "data terakhir Juni 2024" lagi!
                - PAKAI hasil search di bawah ini
