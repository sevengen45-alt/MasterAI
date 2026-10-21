import streamlit as st
from groq import Groq
import uuid
import time
import base64

st.set_page_config(page_title="MasterAI v21 - Gemini Premium", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', -apple-system, sans-serif !important; }

html, body, [data-testid="stAppViewContainer"], p, div, span { color: #000000 !important; }
.stApp { background: #FFFFFF !important; }

/* ===== GEMINI RAINBOW - LIVE HALUS ===== */
@keyframes geminiRainbow { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
@keyframes geminiShimmer { 0%{opacity:0.6} 100%{opacity:1} }

.premium-header { max-width: 760px; margin: 0 auto; padding: 36px 24px 20px 24px; text-align: center; }
.premium-title {
    font-size: 3rem !important; font-weight: 800 !important; letter-spacing: -0.05em !important;
    line-height: 1 !important; color: #000 !important;
}
.gemini-gradient-text {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4);
    background-size: 400% 100%; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; animation: geminiRainbow 6s ease infinite !important;
}
.gemini-underline {
    width: 80px; height: 3px; margin: 18px auto 0 auto;
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58);
    background-size: 300% 100%; animation: geminiRainbow 4s linear infinite; border-radius: 100px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #F8F9FA !important; border-right: 1px solid rgba(0,0,0,0.06) !important;
}
section[data-testid="stSidebar"] * { color: #000 !important; }
section[data-testid="stSidebar"] .stButton button {
    background: #FFF !important; border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 10px !important; font-weight: 500 !important; text-align: left !important;
}

/* UPLOAD AREA PREMIUM */
.upload-card {
    background: #FFF; border: 1px dashed rgba(0,0,0,0.12); border-radius: 16px; padding: 12px;
    margin: 10px 0;
}
.stFileUploader > div { border-radius: 16px !important; border: 1.5px dashed rgba(0,0,0,0.12) !important; background: #FFF !important; }
.stFileUploader label { color: #000 !important; font-weight: 600 !important; }

/* CHAT */
.stChatMessage { max-width: 740px !important; margin: 0 auto !important; background: transparent !important; border: none !important; }
div[data-testid="stChatMessageContent"] {
    background: #FFF !important; border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 20px !important; padding: 14px 18px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}
.stChatMessage p { color: #000 !important; font-size: 15.5px !important; font-weight: 450 !important; line-height: 1.6 !important; }
.preview-img { border-radius: 14px; border: 1px solid rgba(0,0,0,0.08); max-width: 280px; margin: 8px 0; }

/* ===== TASKBAR - GEMINI RAINBOW LIVE 2.5 DETIK ===== */
div[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important;
    background-size: 500% 100% !important; animation: geminiRainbow 2.5s linear infinite !important;
    padding: 2.5px !important; border-radius: 28px !important; max-width: 740px !important;
    margin: 0 auto !important; bottom: 24px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1), 0 0 0 1px rgba(0,0,0,0.04) !important;
}
div[data-testid="stChatInput"] > div { background: #FFF !important; border-radius: 26px !important; padding: 6px 8px 6px 18px !important; }
div[data-testid="stChatInput"] textarea { color: #000 !important; -webkit-text-fill-color: #000 !important; font-weight: 500 !important; font-size: 16px !important; }
div[data-testid="stChatInput"] textarea::placeholder {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400) !important;
    background-size: 300% 100% !important; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; font-weight: 600 !important; animation: geminiRainbow 3s linear infinite !important;
}
div[data-testid="stChatInput"] button { background: #000 !important; border-radius: 50% !important; width: 36px !important; height: 36px !important; }
div[data-testid="stChatInput"] button * { color: #FFF !important; }

/* Audio input premium */
div[data-testid="stAudioInput"] { background: #FFF !important; border: 1px solid rgba(0,0,0,0.08) !important; border-radius: 16px !important; }
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

# ===== SIDEBAR - UPLOAD & VOICE =====
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
    
    st.markdown("#### 📎 Upload")
    uploaded = st.file_uploader("Foto / Dokumen", type=["png","jpg","jpeg","webp","pdf","txt","docx","csv"], accept_multiple_files=True, label_visibility="collapsed")
    if uploaded:
        st.session_state.pending_files = uploaded
        for f in uploaded:
            st.success(f"✓ {f.name}")

    st.markdown("#### 🎙️ Voice Note")
    audio = st.audio_input("Rekam suara", label_visibility="collapsed")
    transcribed_text = None
    if audio:
        with st.spinner("Transkripsi suara..."):
            try:
                # Groq Whisper
                transcription = client.audio.transcriptions.create(
                    file=(audio.name, audio.getvalue()),
                    model="whisper-large-v3",
                    response_format="json",
                    language="id"
                )
                transcribed_text = transcription.text
                st.success(f"Transkrip: {transcribed_text[:80]}...")
                st.session_state["voice_transcript"] = transcribed_text
            except Exception as e:
                st.error(f"Gagal transkrip: {e}")

    st.divider()
    if st.button("＋ New chat", use_container_width=True):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": "New conversation", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    
    st.caption("Recent")
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True)[:8]:
        if st.button(f"{chat['title'][:24]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()

# HEADER
st.markdown(f"""
<div class="premium-header">
    <div class="premium-title">Siap Memulai<br><span class="gemini-gradient-text">Obrolan?</span></div>
    <div class="gemini-underline"></div>
    <div style="margin-top:12px; font-size:12px; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:rgba(0,0,0,0.4);">Gemini • Rainbow Live • Voice • by Juan</div>
</div>
""", unsafe_allow_html=True)

# DISPLAY CHAT
for m in active["messages"]:
    with st.chat_message(m["role"]):
        if "files" in m:
            for fname in m["files"]:
                st.markdown(f"📎 **{fname}**")
        st.markdown(f"<div style='color:black !important;'>{m['content']}</div>", unsafe_allow_html=True)
        if "image" in m:
            st.image(m["image"], width=320)

# INPUT LOGIC
# Cek voice transcript
voice_prefill = st.session_state.pop("voice_transcript", None)

if voice_prefill:
    prompt = voice_prefill
    st.toast(f"🎙️ Voice: {prompt[:50]}...")
else:
    prompt = st.chat_input("Tanya apa saja! ✨")

if prompt:
    # handle files
    file_names = []
    file_images = []
    if st.session_state.pending_files:
        for f in st.session_state.pending_files:
            file_names.append(f.name)
            if f.type.startswith("image/"):
                file_images.append(f)
    
    if len(active["messages"]) == 0: 
        active["title"] = prompt[:40]
    
    user_msg = {"role": "user", "content": prompt, "files": file_names}
    active["messages"].append(user_msg)
    
    with st.chat_message("user"):
        if file_names:
            for fn in file_names:
                st.markdown(f"📎 {fn}")
        st.markdown(f"<div style='color:black !important;'>{prompt}</div>", unsafe_allow_html=True)
        for img in file_images:
            st.image(img, width=320)

    with st.chat_message("assistant"):
        ph = st.empty()
        ph.markdown("▌")
        try:
            nama = st.session_state.user_memory["nama"] or "bang"
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = DEVELOPER_INFO
                ph.markdown(f"<div style='color:black !important;'>{ans}</div>", unsafe_allow_html=True)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                # Jika ada gambar, kasih konteks
                context_extra = ""
                if file_names:
                    context_extra = f"User upload file: {', '.join(file_names)}. "
                
                system_prompt = f"Kamu MasterAI v21 Gemini Premium. {DEVELOPER_INFO}. User: {nama}. {context_extra}Jawab premium, clean, helpful. Jika user tanya tentang gambar/file yang diupload, jelaskan kamu bisa melihat nama file nya dan bantu analisis."
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
        except Exception as e:
            ph.error(f"Error: {e}")
