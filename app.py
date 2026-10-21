import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v21.1 - Inside Taskbar", page_icon="✦", layout="wide")

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

/* SIDEBAR BIAR BERSIH - GAK ADA UPLOAD LAGI */
section[data-testid="stSidebar"] { background: #F8F9FA !important; border-right: 1px solid rgba(0,0,0,0.06) !important; }
section[data-testid="stSidebar"] * { color: #000 !important; }
section[data-testid="stSidebar"] .stButton button { background: #FFF !important; border: 1px solid rgba(0,0,0,0.08) !important; border-radius: 10px !important; text-align: left !important; }

/* CHAT */
.stChatMessage { max-width: 740px !important; margin: 0 auto !important; background: transparent !important; border: none !important; }
div[data-testid="stChatMessageContent"] { background: #FFF !important; border: 1px solid rgba(0,0,0,0.08) !important; border-radius: 20px !important; padding: 14px 18px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
.stChatMessage p { color: #000 !important; font-size: 15.5px !important; font-weight: 450 !important; line-height: 1.6 !important; }

/* ===== TASKBAR CUSTOM - GEMINI STYLE DI DALAM ===== */
.custom-taskbar-wrapper {
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    width: 92%; max-width: 740px; z-index: 9999;
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 500% 100% !important; animation: geminiRainbow 2.5s linear infinite !important;
    padding: 2.5px !important; border-radius: 28px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12) !important;
}
.custom-taskbar-inner {
    background: #FFF !important; border-radius: 26px !important;
    display: flex; align-items: center; gap: 6px; padding: 8px 10px 8px 14px !important;
}
.taskbar-input {
    flex: 1; border: none !important; outline: none !important;
    font-size: 16px !important; font-weight: 500 !important; color: #000 !important;
    background: transparent !important; padding: 8px 0 !important;
}
.taskbar-input::placeholder {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400) !important;
    background-size: 300% 100% !important; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; font-weight: 600 !important; animation: geminiRainbow 3s linear infinite !important;
}
.icon-btn {
    width: 36px; height: 36px; border-radius: 50%; border: 1px solid rgba(0,0,0,0.08);
    background: #F8F9FA; display: flex; align-items: center; justify-content: center;
    cursor: pointer; font-size: 16px; transition: all 0.2s; flex-shrink: 0;
}
.icon-btn:hover { background: #EEE; transform: scale(1.05); }
.send-btn {
    width: 38px; height: 38px; border-radius: 50%; background: #000 !important; color: #FFF !important;
    border: none; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 18px; flex-shrink: 0;
}

/* File uploader di popover */
div[data-testid="stPopover"] button { border-radius: 50% !important; width: 36px !important; height: 36px !important; border: 1px solid rgba(0,0,0,0.08) !important; background: #F8F9FA !important; }
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
    st.divider()
    st.caption("Recent")
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True)[:8]:
        if st.button(f"{chat['title'][:24]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.markdown(f"""
<div class="premium-header">
    <div class="premium-title">Siap Memulai<br><span class="gemini-gradient-text">Obrolan?</span></div>
    <div class="gemini-underline"></div>
    <div style="margin-top:12px; font-size:11px; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:rgba(0,0,0,0.4);">GEMINI • INSIDE TASKBAR • by Juan</div>
</div>
""", unsafe_allow_html=True)

# DISPLAY CHAT - KASIH JARAK BAWAH BIAR GAK KETUTUP TASKBAR
st.markdown('<div style="padding-bottom: 100px;">', unsafe_allow_html=True)
for m in active["messages"]:
    with st.chat_message(m["role"]):
        if m.get("files"):
            for fn in m["files"]:
                st.markdown(f"📎 **{fn}**")
        st.markdown(f"<div style='color:black !important;'>{m['content']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===== CUSTOM TASKBAR - FILE + MIC DI KIRI TOMBOL UP =====
st.markdown('<div class="custom-taskbar-wrapper"><div class="custom-taskbar-inner">', unsafe_allow_html=True)

# Kita pakai columns di dalam wrapper custom biar bisa pasang popover di kiri tombol up
col_file, col_mic, col_input, col_send = st.columns([0.12, 0.12, 0.58, 0.18])

with col_file:
    with st.popover("📎", use_container_width=True):
        st.markdown("**Upload Foto / File**")
        uploaded = st.file_uploader("Pilih file", type=["png","jpg","jpeg","webp","pdf","txt","docx","csv"], accept_multiple_files=True, label_visibility="collapsed", key="inside_file")
        if uploaded:
            st.session_state.pending_files = uploaded
            for f in uploaded:
                st.success(f"✓ {f.name[:20]}")

with col_mic:
    with st.popover("🎙️", use_container_width=True):
        st.markdown("**Voice Note → Text**")
        audio = st.audio_input("Rekam", label_visibility="collapsed", key="inside_voice")
        if audio:
            with st.spinner("Transkripsi..."):
                try:
                    transcription = client.audio.transcriptions.create(
                        file=(audio.name, audio.getvalue()),
                        model="whisper-large-v3",
                        response_format="json",
                        language="id"
                    )
                    # FIX INI - LANGSUNG PINDAH KE TASKBAR!
                    st.session_state["gemini_input"] = transcription.text
                    st.session_state["voice_transcript"] = transcription.text
                    st.success(f"✓ {transcription.text[:60]}...")
                    time.sleep(0.5)
                    st.rerun() # INI KUNCINYA! BIAR LANGSUNG MUNCUL DI TASKBAR!
                except Exception as e:
                    st.error(f"{e}")

with col_input:
    # Input text custom - pakai text_input biasa tapi styling kayak Gemini
    if "voice_transcript" in st.session_state:
        default_val = st.session_state.pop("voice_transcript")
    else:
        default_val = ""
    
    prompt = st.text_input("input", placeholder="Tanya apa saja! ✨", label_visibility="collapsed", value=default_val, key="gemini_input")

with col_send:
    send_clicked = st.button("↑", key="send_btn", use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# LOGIC KIRIM
if (prompt and prompt.strip() != "") or send_clicked:
    if prompt and prompt.strip() != "":
        final_prompt = prompt
    else:
        final_prompt = ""
    
    if final_prompt:
        file_names = [f.name for f in st.session_state.pending_files] if st.session_state.pending_files else []
        
        if len(active["messages"]) == 0:
            active["title"] = final_prompt[:40]
        
        active["messages"].append({"role": "user", "content": final_prompt, "files": file_names})
        
        # Tampilkan langsung
        with st.chat_message("user"):
            if file_names:
                for fn in file_names:
                    st.markdown(f"📎 {fn}")
            st.markdown(f"<div style='color:black !important;'>{final_prompt}</div>", unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            ph = st.empty()
            try:
                nama = st.session_state.user_memory["nama"] or "bang"
                if any(k in final_prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                    ans = DEVELOPER_INFO
                    ph.markdown(f"<div style='color:black !important;'>{ans}</div>", unsafe_allow_html=True)
                    active["messages"].append({"role": "assistant", "content": ans})
                else:
                    context_extra = f"File: {', '.join(file_names)}. " if file_names else ""
                    system_prompt = f"Kamu MasterAI Gemini. {DEVELOPER_INFO}. User: {nama}. {context_extra}"
                    messages = [{"role": "system", "content": system_prompt}] + [{"role": m["role"], "content": m["content"]} for m in active["messages"]]
                    res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.7, max_tokens=1500)
                    ans = res.choices[0].message.content
                    full = ""
                    for w in ans.split(" "):
                        full += w + " "
                        ph.markdown(f"<div style='color:black !important;'>{full}▌</div>", unsafe_allow_html=True)
                        time.sleep(0.01)
                    ph.markdown(f"<div style='color:black !important;'>{full}</div>", unsafe_allow_html=True)
                    active["messages"].append({"role": "assistant", "content": full})
                st.session_state.pending_files = []
                time.sleep(0.3)
                st.rerun()
            except Exception as e:
                ph.error(f"Error: {e}")
