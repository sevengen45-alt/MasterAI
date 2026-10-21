import streamlit as st
from groq import Groq
import uuid
import time
import base64

st.set_page_config(page_title="MasterAI v22 - Vision Fix", page_icon="👁️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', -apple-system, sans-serif !important; }
html, body, [data-testid="stAppViewContainer"], p, div, span { color: #000 !important; }
.stApp { background: #FFF !important; }
@keyframes geminiRainbow { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.premium-header { max-width: 760px; margin: 0 auto; padding: 36px 24px 20px 24px; text-align: center; }
.premium-title { font-size: 3rem !important; font-weight: 800 !important; letter-spacing: -0.05em !important; color: #000 !important; }
.gemini-gradient-text {
    background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4);
    background-size: 400% 100%; -webkit-background-clip: text !important; background-clip: text !important;
    -webkit-text-fill-color: transparent !important; animation: geminiRainbow 6s ease infinite !important;
}
.gemini-underline { width: 80px; height: 3px; margin: 18px auto 0 auto; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58); background-size: 300% 100%; animation: geminiRainbow 4s linear infinite; border-radius: 100px; }
section[data-testid="stSidebar"] { background: #F8F9FA !important; }
section[data-testid="stSidebar"] * { color: #000 !important; }
.stChatMessage { max-width: 740px !important; margin: 0 auto !important; background: transparent !important; border: none !important; }
div[data-testid="stChatMessageContent"] { background: #FFF !important; border: 1px solid rgba(0,0,0,0.08) !important; border-radius: 20px !important; padding: 14px 18px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
.stChatMessage p { color: #000 !important; font-size: 15.5px !important; }
</style>
""", unsafe_allow_html=True)

DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def to_b64(file):
    return base64.b64encode(file.getvalue()).decode('utf-8')

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Siap Memulai Obrolan?", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid
if "pending_files" not in st.session_state:
    st.session_state.pending_files = []
if "pending_b64" not in st.session_state:
    st.session_state.pending_b64 = []

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown('<div style="font-weight:800;">✦ MasterAI • Vision</div>', unsafe_allow_html=True)
    st.caption("Bisa baca foto by Juan")
    if st.session_state.user_memory["nama"]:
        st.markdown(f"**👋 {st.session_state.user_memory['nama']}**")
    else:
        nama = st.text_input("Nama", placeholder="Nama kamu?", label_visibility="collapsed")
        if nama:
            st.session_state.user_memory["nama"] = nama
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

st.markdown('<div style="padding-bottom: 130px;">', unsafe_allow_html=True)
for m in active["messages"]:
    with st.chat_message(m["role"]):
        if m.get("images"):
            for img_b64 in m["images"]:
                st.image(base64.b64decode(img_b64), width=400)
        if m.get("files"):
            for fn in m["files"]:
                st.markdown(f"📎 {fn}")
        st.markdown(f"<div style='color:black !important;'>{m['content']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# TASKBAR - CUMA 📎 + INPUT + ↑ (VOICE SUDAH HILANG)
st.markdown("""
<style>
.taskbar-fix { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); width: 92%; max-width: 740px; z-index: 9999; background: linear-gradient(90deg, #4285F4, #9C27B0, #DB4437, #F4B400, #0F9D58, #4285F4) !important; background-size: 500% 100% !important; animation: geminiRainbow 2.5s linear infinite !important; padding: 2.5px !important; border-radius: 28px !important; box-shadow: 0 8px 32px rgba(0,0,0,0.12) !important; }
.taskbar-fix-inner { background: #FFF !important; border-radius: 26px !important; padding: 8px 12px !important; }
div[data-testid="stPopover"] button { border-radius: 50% !important; width: 38px !important; height: 38px !important; background: #F5F5F7 !important; border: 1px solid rgba(0,0,0,0.08) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="taskbar-fix"><div class="taskbar-fix-inner">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([0.15, 0.65, 0.2])

with c1:
    with st.popover("📎", use_container_width=True):
        st.markdown("**Upload Foto**")
        st.caption("AI akan baca isi fotonya!")
        ups = st.file_uploader("Upload", type=["png","jpg","jpeg","webp"], accept_multiple_files=True, label_visibility="collapsed", key="up")
        if ups:
            b64s = []
            for f in ups:
                b64 = to_b64(f)
                b64s.append(b64)
                st.image(f, width=180)
                st.success(f"✓ {f.name}")
            st.session_state.pending_files = ups
            st.session_state.pending_b64 = b64s
            st.info("Foto siap! Sekarang ketik pertanyaan di taskbar lalu ↑")

with c2:
    prompt = st.text_input("prompt", placeholder="Tanya apa saja! ✨", label_visibility="collapsed", key="gemini_input")

with c3:
    send = st.button("↑", use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)

if prompt and prompt.strip():
    if len(active["messages"]) == 0 or active["messages"][-1].get("content") != prompt:
        if len(active["messages"]) == 0:
            active["title"] = prompt[:40]
        
        files = [f.name for f in st.session_state.pending_files] if st.session_state.pending_files else []
        b64s = st.session_state.pending_b64 if st.session_state.pending_b64 else []
        
        active["messages"].append({"role": "user", "content": prompt, "files": files, "images": b64s})
        
        with st.chat_message("assistant"):
            ph = st.empty()
            ph.markdown("👁️ Menganalisis gambar...")
            try:
                nama = st.session_state.user_memory["nama"] or "bang"
                if any(k in prompt.lower() for k in ["siapa yang membuat","siapa pembuat","who made you","dibuat siapa","developer"]):
                    ans = DEVELOPER_INFO
                    ph.markdown(f"<div style='color:black !important;'>{ans}</div>", unsafe_allow_html=True)
                    active["messages"].append({"role": "assistant", "content": ans})
                else:
                    if b64s:
                        # MODEL VISION - BISA BACA GAMBAR BENERAN!
                        content = [{"type": "text", "text": f"User: {prompt}\nTolong jelaskan isi gambar ini dengan sangat detail. Ada apa saja di dalam gambar?"}]
                        for b in b64s:
                            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b}"}})
                        
                        resp = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[
                                {"role": "system", "content": f"Kamu MasterAI Vision. {DEVELOPER_INFO}. Kamu HARUS menganalisis gambar yang dikirim user. Jelaskan detail, teks, objek, warna yang ada di gambar. User: {nama}"},
                                {"role": "user", "content": content}
                            ],
                            temperature=0.5,
                            max_tokens=2000
                        )
                        ans = resp.choices[0].message.content
                    else:
                        resp = client.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[
                                {"role": "system", "content": f"Kamu MasterAI. {DEVELOPER_INFO}"},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=1500
                        )
                        ans = resp.choices[0].message.content
                    
                    ph.markdown(f"<div style='color:black !important;'>{ans}</div>", unsafe_allow_html=True)
                    active["messages"].append({"role": "assistant", "content": ans})
                
                st.session_state.pending_files = []
                st.session_state.pending_b64 = []
                st.session_state["gemini_input"] = ""
                time.sleep(0.5)
                st.rerun()
            except Exception as e:
                ph.error(f"Error: {e}\n\nCoba ganti model ke: llama-3.2-11b-vision-preview")
                # Fallback otomatis
                try:
                    content = [{"type": "text", "text": prompt}]
                    for b in b64s:
                        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b}"}})
                    resp = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{"role": "user", "content": content}],
                        max_tokens=1500
                    )
                    ans = resp.choices[0].message.content
                    ph.markdown(f"<div style='color:black !important;'>{ans}</div>", unsafe_allow_html=True)
                    active["messages"].append({"role": "assistant", "content": ans})
                    st.session_state.pending_files = []
                    st.session_state.pending_b64 = []
                    st.rerun()
                except Exception as e2:
                    ph.error(f"Vision gagal: {e2}")
