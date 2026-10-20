import streamlit as st
from groq import Groq
import uuid, base64

st.set_page_config(page_title="MasterAI v6.7", page_icon="🐺", layout="wide")

st.markdown("""
<style>
    .stApp { background: radial-gradient(ellipse at top, #0f0f23 0%, #000000 100%); }
    h1 { background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; font-size:2.3rem !important; font-weight:800 !important; }
    .stChatMessage { background: rgba(255,255,255,0.06) !important; border-radius: 20px !important; border: 1px solid rgba(123,97,255,0.3) !important; }
    .badge { background: linear-gradient(90deg, #00F5FF, #7B61FF); padding: 5px 12px; border-radius: 20px; color: white; font-size: 11px; display:inline-block; margin:2px;}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Obrolan Baru ✨", "messages": [{"role":"assistant","content":"Yo bang! v6.7 ANTI-ECHO ON! 🐺"}]}}
    st.session_state.active_chat = fid
if "last_upload" not in st.session_state:
    st.session_state.last_upload = None

with st.sidebar:
    st.markdown("## 👨🏼‍💻 MasterAI v6.7")
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 {st.session_state.user_memory['nama']}")
    st.markdown('<span class="badge">👁️ VISION FIX 404</span> <span class="badge">🚫 ANTI-ECHO</span>', unsafe_allow_html=True)
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": []}
        st.session_state.active_chat = nid
        st.session_state.last_upload = None
        st.rerun()

active = st.session_state.chats[st.session_state.active_chat]
st.title(active["title"])

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "👨🏼‍💻"):
        st.markdown(m["content"])

st.markdown("---")
up_col, info_col = st.columns([1, 4])
with up_col:
    uploaded_file = st.file_uploader("📎", type=["png","jpg","jpeg","webp"], label_visibility="collapsed")
    if uploaded_file:
        st.session_state.last_upload = uploaded_file
        st.image(uploaded_file, width=140, caption="Siap 👁️")
with info_col:
    if st.session_state.last_upload:
        st.info(f"📎 {st.session_state.last_upload.name} siap - ketik di bawah")
        if st.button("❌ Hapus file"):
            st.session_state.last_upload = None
            st.rerun()

if prompt := st.chat_input("Tanya soal gambar / ketik /gambar kucing 🗿"):
    if len(active["messages"]) <= 1:
        active["title"] = prompt[:25]
    active["messages"].append({"role":"user","content": prompt})
    
    with st.chat_message("assistant", avatar="👨🏼‍💻"):
        if prompt.lower().startswith("/gambar"):
            q = prompt[7:].strip() or "hacker"
            url = f"https://image.pollinations.ai/prompt/{q.replace(' ','%20')}?nologo=true&width=1024&height=1024"
            st.image(url, caption=q)
            active["messages"].append({"role":"assistant","content": f"✅ Gambar '{q}' jadi!"})
        elif st.session_state.last_upload is not None:
            try:
                b64 = base64.b64encode(st.session_state.last_upload.getvalue()).decode('utf-8')
                nama = st.session_state.user_memory["nama"] or "bang"
                sys = f"Kamu MasterAI v6.7, teman {nama}. WAJIB Bahasa Indonesia gaul. Lihat gambar dan jawab akurat. Jangan echo."
                with st.spinner("👁️ Lagi ngeliat..."):
                    res = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[
                            {"role":"system","content": sys},
                            {"role":"user","content":[
                                {"type":"text","text": prompt},
                                {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                            ]}
                        ],
                        max_tokens=800
                    )
                ans = res.choices[0].message.content
                st.markdown(ans)
                active["messages"].append({"role":"assistant","content": ans})
                st.session_state.last_upload = None
            except Exception as e:
                st.error(f"Gagal liat gambar: {e}")
        else:
            try:
                nama = st.session_state.user_memory["nama"] or "bang"
                sys = f"Kamu MasterAI v6.7, teman {nama}. WAJIB Bahasa Indonesia."
                msgs = [{"role":"system","content": sys}] + [{"role": m["role"], "content": m["content"]} for m in active["messages"]]
                comp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b")
                ans = comp.choices[0].message.content
                st.markdown(ans)
                active["messages"].append({"role":"assistant","content": ans})
            except Exception as e:
                st.error(f"Error: {e}")
