import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v21.2 - Voice Fix", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', -apple-system, sans-serif !important; }
html, body, [data-testid="stAppViewContainer"], p, div, span { color: #000 !important; }
.stApp { background: #FFF !important; }
@keyframes geminiRainbow { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.premium-header { max-width: 760px; margin: 0 auto; padding: 36px 24px 20px 24px; text-align: center; }
.premium-title { font-size: 3rem !important; font-weight: 800 !important; letter-spacing: -0.05em !important; line-height: 1 !important; color: #000 !important; }
.gemini-gradient-text {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4);
    background-size: 400% 100%; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; animation: geminiRainbow 6s ease infinite !important;
}
.gemini-underline { width: 80px; height: 3px; margin: 18px auto 0 auto; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58); background-size: 300% 100%; animation: geminiRainbow 4s linear infinite; border-radius: 100px; }
section[data-testid="stSidebar"] { background: #F8F9FA !important; border-right: 1px solid rgba(0,0,0,0.06) !important; }
section[data-testid="stSidebar"] * { color: #000 !important; }
.stChatMessage { max-width: 740px !important; margin: 0 auto !important; background: transparent !important; border: none !important; }
div[data-testid="stChatMessageContent"] { background: #FFF !important; border: 1px solid rgba(0,0,0,0.08) !important; border-radius: 20px !important; padding: 14px 18px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
.stChatMessage p { color: #000 !important; font-size: 15.5px !important; font-weight: 450 !important; line-height: 1.6 !important; }
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
if "pending_files" not in st.session_state:
    st.session_state.pending_files = []

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown('<div style="font-weight:800; font-size:14px;">✦ MasterAI • Gemini</div>', unsafe_allow_html=True)
    st.caption("Premium by Juan Maumere")
    st.divider()
    if st.session_state.user_memory["nama"]:
        st.markdown(f"**👋 {st.session_state.user_memory['nama']}**")
    else:
        nama_input = st.text_input("Nama lu", placeholder="Nama kamu?", label_visibility="collapsed")
        if nama_input:
            st.session_state.user_memory["nama"] = nama_input
            st.rerun()
    if st.button("＋ New chat", use_container_width=True):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": "New conversation", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()

active = get_active()
st.markdown(f"""
<div class="premium-header">
    <div class="premium-title">Siap Memulai<br><span class="gemini-gradient-text">Obrolan?</span></div>
    <div class="gemini-underline"></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="padding-bottom: 120px;">', unsafe_allow_html=True)
for m in active["messages"]:
    with st.chat_message(m["role"]):
        if m.get("files"):
            for fn in m["files"]:
                st.markdown(f"📎 **{fn}**")
        st.markdown(f"<div style='color:black !important;'>{m['content']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===== TASKBAR DENGAN FILE + MIC DI KIRI TOMBOL UP =====
# Container bawah custom
bottom_container = st.container()
with bottom_container:
    st.markdown("""
    <style>
    .taskbar-fix {
        position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
        width: 92%; max-width: 740px; z-index: 9999;
        background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
        background-size: 500% 100% !important; animation: geminiRainbow 2.5s linear infinite !important;
        padding: 2.5px !important; border-radius: 28px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12) !important;
    }
    .taskbar-fix-inner { background: #FFF !important; border-radius: 26px !important; padding: 8px 12px !important; }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="taskbar-fix"><div class="taskbar-fix-inner">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([0.13, 0.13, 0.6, 0.14])
        
        with c1:
            with st.popover("📎", use_container_width=True):
                st.markdown("**Upload Foto / File**")
                up = st.file_uploader("file", type=["png","jpg","jpeg","webp","pdf","txt","docx","csv"], accept_multiple_files=True, label_visibility="collapsed", key="f1")
                if up:
                    st.session_state.pending_files = up
                    st.success(f"✓ {len(up)} file")
        
        with c2:
            with st.popover("🎙️", use_container_width=True):
                st.markdown("**Voice → Text**")
                st.caption("Ngomong, nanti otomatis pindah ke taskbar!")
                audio = st.audio_input("Rekam", label_visibility="collapsed", key="v1")
                if audio:
                    with st.spinner("Transkripsi..."):
                        try:
                            tr = client.audio.transcriptions.create(
                                file=(audio.name, audio.getvalue()),
                                model="whisper-large-v3",
                                response_format="json",
                                language="id"
                            )
                            # INI FIX NYA!
                            st.session_state["gemini_input"] = tr.text
                            st.success(f"✓ {tr.text}")
                            time.sleep(0.8)
                            st.rerun()
                        except Exception as e:
                            st.error(f"{e}")
        
        with c3:
            prompt = st.text_input("prompt", placeholder="Tanya apa saja! ✨", label_visibility="collapsed", key="gemini_input")
        
        with c4:
            send = st.button("↑", use_container_width=True, key="send")
        
        st.markdown('</div></div>', unsafe_allow_html=True)

# LOGIC KIRIM
if (prompt and prompt.strip()) and (send or True):
    # Hanya kirim kalau ada prompt dan user pencet enter atau tombol up
    # Streamlit text_input enter otomatis rerun, jadi kita cek prompt
    if prompt and prompt.strip() and "gemini_input" in st.session_state:
        # Cegah double kirim - cek apakah ini pesan baru
        if len(active["messages"]) == 0 or active["messages"][-1]["content"] != prompt:
            if len(active["messages"]) == 0:
                active["title"] = prompt[:40]
            
            file_names = [f.name for f in st.session_state.pending_files] if st.session_state.pending_files else []
            active["messages"].append({"role": "user", "content": prompt, "files": file_names})
            
            with st.chat_message("assistant"):
                ph = st.empty()
                try:
                    nama = st.session_state.user_memory["nama"] or "bang"
                    if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                        ans = DEVELOPER_INFO
                        ph.markdown(f"<div style='color:black !important;'>{ans}</div>", unsafe_allow_html=True)
                        active["messages"].append({"role": "assistant", "content": ans})
                    else:
                        sys_p = f"Kamu MasterAI. {DEVELOPER_INFO}. User: {nama}. File: {', '.join(file_names) if file_names else 'tidak ada'}"
                        msgs = [{"role": "system", "content": sys_p}] + [{"role": m["role"], "content": m["content"]} for m in active["messages"]]
                        res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=msgs, temperature=0.7, max_tokens=1500)
                        ans = res.choices[0].message.content
                        ph.markdown(f"<div style='color:black !important;'>{ans}</div>", unsafe_allow_html=True)
                        active["messages"].append({"role": "assistant", "content": ans})
                    
                    st.session_state.pending_files = []
                    st.session_state["gemini_input"] = ""
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    ph.error(f"{e}")
