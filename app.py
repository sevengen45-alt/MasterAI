import streamlit as st
from groq import Groq
import time, uuid, base64, io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

st.set_page_config(page_title="MasterAI v6.4", page_icon="👨🏼‍💻", layout="wide")

st.markdown("""
<style>
    .stApp { background: radial-gradient(ellipse at top, #0f0f23 0%, #000000 100%); }
    h1 { animation: wave 3s ease-in-out infinite; background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; font-size:2.5rem !important; font-weight:800 !important; }
    @keyframes wave { 0%{transform: translateY(0px)} 50%{transform: translateY(-6px)} 100%{transform: translateY(0px)} }
    .stChatMessage { background: rgba(255,255,255,0.06) !important; border-radius: 20px !important; backdrop-filter: blur(15px); border: 1px solid rgba(123,97,255,0.3) !important; }
    .badge { background: linear-gradient(90deg, #00F5FF, #7B61FF); padding: 5px 12px; border-radius: 20px; color: white; font-size: 11px; display: inline-block; margin: 3px; }
    /* Bikin file uploader jadi icon bulat */
    div[data-testid="stFileUploader"] section { padding: 0 !important; min-height: 0 !important; }
    div[data-testid="stFileUploader"] label { display: none !important; }
    div[data-testid="stFileUploader"] button { border-radius: 50% !important; width: 45px; height: 45px; }
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY belum ada di Secrets!")
    st.stop()

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.chats = {first_id: {"title": "Obrolan Baru ✨", "messages": [{"role": "assistant", "content": "Yo bang! v6.4 udah fix! 📎 ada di kiri tombol ↑ 🗿🔥"}], "created": datetime.now().strftime("%d %b")}}
    st.session_state.active_chat = first_id
if "uploaded_file_info" not in st.session_state:
    st.session_state.uploaded_file_info = None

# SIDEBAR - GAK ADA UPLOAD LAGI!
with st.sidebar:
    st.markdown("## 👨🏼‍💻 MasterAI v6.4")
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Halo, {st.session_state.user_memory['nama']}!")
    else:
        st.info("💭 Bilang 'panggil aku ...' dong!")
    st.markdown('<span class="badge">📎 Chat Fix</span> <span class="badge">🧠 GPT-120B</span> <span class="badge">🚫 No WM</span>', unsafe_allow_html=True)
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": datetime.now().strftime("%d %b")}
        st.session_state.active_chat = nid
        st.rerun()
    st.markdown("---")
    st.markdown("### 💬 Daftar Obrolan")
    for cid in reversed(list(st.session_state.chats.keys())):
        if st.button(f"{'👉' if cid==st.session_state.active_chat else '💭'} {st.session_state.chats[cid]['title'][:22]}", key=cid, use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()
    st.markdown("---")
    if st.button("🗑️ Hapus Chat", use_container_width=True):
        if len(st.session_state.chats) > 1:
            del st.session_state.chats[st.session_state.active_chat]
            st.session_state.active_chat = list(st.session_state.chats.keys())[-1]
            st.rerun()

active = st.session_state.chats[st.session_state.active_chat]
st.title(active["title"])

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "👨🏼‍💻"):
        st.markdown(m["content"])
        if "image_url" in m:
            st.image(m["image_url"])

# ===== INI BAGIAN KUNCI: CHAT BAR + 📎 DI KIRI TOMBOL ↑ =====
st.markdown("---")
st.markdown("#### 📎 Upload di sini (kiri tombol ↑)")

# Bar bawah custom: [📎] [Ketik...] [↑]
c1, c2, c3 = st.columns([1, 6, 1])

with c1:
    uploaded = st.file_uploader("📎", type=["png","jpg","jpeg","pdf","docx","txt","mp4","mp3","xlsx"], label_visibility="collapsed")

with c2:
    prompt = st.text_input("Ketik...", placeholder="Ketik... /gambar, /pdf, atau curhat 🗿", label_visibility="collapsed", key="chat_text")

with c3:
    send = st.button("↑", use_container_width=True, type="primary")

# Handle upload info
if uploaded:
    st.session_state.uploaded_file_info = uploaded.name
    if uploaded.type.startswith("image"):
        st.image(uploaded, width=150, caption=f"✅ {uploaded.name} siap!")

# LOGIC KIRIM PESAN
if (send and prompt) or (prompt and st.session_state.get('last_prompt') != prompt and prompt.endswith('\n')):
    # Gabung file + prompt
    full_prompt = prompt
    if st.session_state.uploaded_file_info:
        full_prompt = f"[File: {st.session_state.uploaded_file_info}] {prompt}"
        st.toast(f"📎 Mengirim dengan file {st.session_state.uploaded_file_info}")

    low = prompt.lower()
    if any(x in low for x in ["nama aku", "panggil aku", "namaku"]):
        try:
            potential_name = prompt.split()[-1].strip(",.!?").capitalize()
            if 2 < len(potential_name) < 15:
                st.session_state.user_memory["nama"] = potential_name
        except: pass

    if len(active["messages"]) <= 1:
        active["title"] = prompt[:30]

    active["messages"].append({"role": "user", "content": full_prompt})
    
    with st.chat_message("assistant", avatar="👨🏼‍💻"):
        if prompt.lower().startswith("/gambar"):
            query = prompt[7:].strip() or "hacker"
            img_url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?nologo=true&width=1024&height=1024"
            st.markdown(f"🎨 Render `{query}`...")
            st.image(img_url)
            active["messages"].append({"role": "assistant", "content": f"✅ Gambar '{query}' jadi!", "image_url": img_url})
        elif prompt.lower().startswith("/pdf"):
            isi = prompt[4:].strip() or "Laporan"
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(80, 750, f"MasterAI v6.4 - {isi[:40]}")
            c.save()
            buffer.seek(0)
            b64 = base64.b64encode(buffer.read()).decode()
            st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="MasterAI.pdf" style="background: linear-gradient(90deg,#00F5FF,#7B61FF); padding:10px 20px; border-radius:10px; color:white; text-decoration:none;">📄 Download PDF</a>', unsafe_allow_html=True)
            active["messages"].append({"role": "assistant", "content": "✅ PDF jadi!"})
        else:
            nama = st.session_state.user_memory["nama"] or "bang"
            system_prompt = f"Kamu MasterAI v6.4 buatan {nama}. User bisa upload file."
            msgs = [{"role": "system", "content": system_prompt}] + [{"role": m["role"], "content": m["content"]} for m in active["messages"] if "image_url" not in m]
            try:
                completion = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b")
                response = completion.choices[0].message.content
                placeholder = st.empty()
                full = ""
                for ch in response:
                    full += ch
                    placeholder.markdown(full + "▌")
                    time.sleep(0.003)
                placeholder.markdown(full)
                active["messages"].append({"role": "assistant", "content": full})
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.session_state.uploaded_file_info = None
    st.rerun()

# Fallback biar enter juga bisa
if prompt := st.chat_input("Atau ketik di sini juga bisa (backup) 🗿"):
    st.session_state.chat_text = prompt
    st.rerun()
