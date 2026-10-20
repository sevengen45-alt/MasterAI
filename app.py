import streamlit as st
from groq import Groq
import time, uuid, base64, io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

st.set_page_config(page_title="MasterAI v6", page_icon="👨🏼‍💻", layout="wide")

# VISI 1: ANIMASI GLOW + WAVE
st.markdown("""
<style>
    .stApp { background: radial-gradient(ellipse at top, #0f0f23 0%, #000000 100%); }
    @keyframes glow { 0%{box-shadow: 0 0 15px #7B61FF} 50%{box-shadow: 0 0 35px #00F5FF} 100%{box-shadow: 0 0 15px #7B61FF} }
    @keyframes wave { 0%{transform: translateY(0px)} 50%{transform: translateY(-6px)} 100%{transform: translateY(0px)} }
    h1 { animation: wave 3s ease-in-out infinite; background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; font-size:3rem !important; font-weight:800 !important; }
    .stChatMessage { animation: glow 4s infinite; background: rgba(255,255,255,0.06) !important; border-radius: 20px !important; backdrop-filter: blur(15px); border: 1px solid rgba(123,97,255,0.3) !important; }
    div[data-testid="stChatInput"] { background: rgba(255,255,255,0.08) !important; border-radius: 30px !important; border: 1px solid rgba(0,245,255,0.4) !important; }
    .badge { background: linear-gradient(90deg, #00F5FF, #7B61FF); padding: 5px 12px; border-radius: 20px; color: white; font-size: 11px; display: inline-block; margin: 3px; }
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
    st.session_state.chats = {
        first_id: {
            "title": "Obrolan Baru ✨", 
            "messages": [{"role": "assistant", "content": "Yo bang! Selamat datang yaa! 🗿🔥\n\nCoba:\n- `panggil aku Bagas`\n- `/gambar kucing hacker`\n- `/pdf buatkan laporan`"}],
            "created": datetime.now().strftime("%d %b")
        }
    }
    st.session_state.active_chat = first_id

with st.sidebar:
    st.markdown("## 👨🏼‍💻 MasterAI v6.1")
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Halo, {st.session_state.user_memory['nama']}!")
    else:
        st.info("💭 Bilang 'panggil aku ...' dong!")
    st.markdown('<span class="badge">📱 ARM</span> <span class="badge">💻 x86</span> <span class="badge">🚫 No WM</span>', unsafe_allow_html=True)
    
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": datetime.now().strftime("%d %b")}
        st.session_state.active_chat = nid
        st.rerun()

    st.markdown("---")
    st.markdown("### 💬 Daftar Obrolan")
    for cid in reversed(list(st.session_state.chats.keys())):
        chat = st.session_state.chats[cid]
        is_active = cid == st.session_state.active_chat
        if st.button(f"{'👉' if is_active else '💭'} {chat['title'][:22]}", key=cid, use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📤 Upload")
    uploaded = st.file_uploader("File", type=["png","jpg","jpeg","pdf","docx","txt","mp4","mp3"], label_visibility="collapsed")
    if uploaded:
        st.success(f"✅ {uploaded.name} - {uploaded.size//1024} KB")
        if uploaded.type.startswith("image"):
            st.image(uploaded, use_container_width=True)

    if st.button("🗑️ Hapus Chat", use_container_width=True):
        if len(st.session_state.chats) > 1:
            del st.session_state.chats[st.session_state.active_chat]
            st.session_state.active_chat = list(st.session_state.chats.keys())[-1]
            st.rerun()

active = st.session_state.chats[st.session_state.active_chat]
st.title(active["title"])
st.caption(f"User: {st.session_state.user_memory['nama'] or 'Unknown'} • Glowing Active ✨")

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "👨🏼‍💻"):
        st.markdown(m["content"])
        if "image_url" in m:
            st.image(m["image_url"])

if prompt := st.chat_input("Ketik... /gambar, /pdf, atau curhat 🗿"):
    low = prompt.lower()
    if any(x in low for x in ["nama aku", "panggil aku", "namaku"]):
        try:
            potential_name = prompt.split()[-1].strip(",.!?").capitalize()
            if len(potential_name) > 2 and len(potential_name) < 15:
                st.session_state.user_memory["nama"] = potential_name
                st.toast(f"Siap {potential_name}! 🫵🏼")
        except: pass

    if len(active["messages"]) <= 1:
        active["title"] = prompt[:30]

    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👨🏼‍💻"):
        if prompt.lower().startswith("/gambar"):
            query = prompt[7:].strip() or "hacker cool"
            safe_query = query.replace(" ", "%20")
            img_url = f"https://image.pollinations.ai/prompt/{safe_query}?nologo=true&enhance=true&width=1024&height=1024"
            st.markdown(f"🎨 Nge-render `{query}` (No Watermark)...")
            st.image(img_url, caption=f"✅ {query}")
            active["messages"].append({"role": "assistant", "content": f"✅ Gambar '{query}' jadi! 🗿🔥", "image_url": img_url})

        elif prompt.lower().startswith("/pdf"):
            isi = prompt[4:].strip() or "Laporan MasterAI"
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(80, 750, "MasterAI v6.1 - Document")
            c.setFont("Helvetica", 11)
            c.drawString(80, 730, f"Untuk: {st.session_state.user_memory['nama'] or 'User'}")
            c.drawString(80, 710, f"Tanggal: {datetime.now()}")
            text_obj = c.beginText(80, 660)
            text_obj.textLines(f"{isi}\n\n---\nMade by MasterAI v6.1 - No Watermark")
            c.drawText(text_obj)
            c.save()
            buffer.seek(0)
            b64 = base64.b64encode(buffer.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="MasterAI.pdf" style="background: linear-gradient(90deg, #00F5FF, #7B61FF); padding: 12px 20px; border-radius: 10px; color: white; text-decoration: none;">📄 Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
            active["messages"].append({"role": "assistant", "content": "✅ PDF jadi tanpa watermark!"})

        else:
            nama = st.session_state.user_memory["nama"] or "bang"
            system_prompt = f"Kamu MasterAI v6.1, AI gaul Jaksel buatan {nama}. Ingat nama user {nama}, panggil kadang aja. Bahasa gaul, pake emoji 🗿😉🔥, jangan kaku. Bisa bikin gambar /gambar, pdf /pdf, baca file, support ARM & x86."
            msgs = [{"role": "system", "content": system_prompt}] + [{"role": m["role"], "content": m["content"]} for m in active["messages"] if "image_url" not in m]
            try:
                completion = client.chat.completions.create(messages=msgs, model="llama-3.3-70b-versatile")
                response = completion.choices[0].message.content
                placeholder = st.empty()
                full = ""
                for ch in response:
                    full += ch
                    placeholder.markdown(full + "▌")
                    time.sleep(0.004)
                placeholder.markdown(full)
                active["messages"].append({"role": "assistant", "content": full})
            except Exception as e:
                st.error(f"Error: {e}")
