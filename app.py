import streamlit as st
from groq import Groq
import uuid, base64, requests

st.set_page_config(page_title="MasterAI v7.0 GPT", page_icon="🤖", layout="wide")
st.markdown("""
<style>
    .stApp { background: radial-gradient(ellipse at top, #0f0f23 0%, #000000 100%); }
    h1 { background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; font-size:2.3rem !important; font-weight:800 !important; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "Obrolan Baru ✨", "messages": [{"role":"assistant","content":"Yo bang! v7.0 GPT ONLY ON! 🤖 No more Llama, no more 404! Chat = GPT-OSS 120B (Groq), Vision = GPT-4o (Pollinations)"}]}}
    st.session_state.active_chat = fid
if "last_upload" not in st.session_state:
    st.session_state.last_upload = None

active = st.session_state.chats[st.session_state.active_chat]
st.title(active["title"])

for m in active["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

up = st.file_uploader("📎 Upload gambar (GPT Vision)", type=["png","jpg","jpeg","webp"])
if up:
    st.session_state.last_upload = up
    st.image(up, width=200)

if prompt := st.chat_input("Tanya apa aja, soal gambar juga bisa..."):
    active["messages"].append({"role":"user","content": prompt})
    with st.chat_message("assistant"):
        if st.session_state.last_upload:
            with st.spinner("🤖 GPT lagi ngeliat gambar..."):
                try:
                    b64 = base64.b64encode(st.session_state.last_upload.getvalue()).decode('utf-8')
                    # PAKAI POLLINATIONS GPT-4o VISION GRATIS - 100% GPT, NO LLAMA
                    payload = {
                        "model": "openai",
                        "messages": [
                            {"role": "system", "content": "Kamu MasterAI v7.0, WAJIB Bahasa Indonesia gaul, jawab soal gambar dengan akurat dan santai."},
                            {"role": "user", "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                            ]}
                        ],
                        "max_tokens": 800
                    }
                    r = requests.post("https://text.pollinations.ai/openai", json=payload, timeout=60)
                    ans = r.json()['choices'][0]['message']['content']
                    st.markdown(ans)
                    active["messages"].append({"role":"assistant","content": ans})
                    st.session_state.last_upload = None
                except Exception as e:
                    st.error(f"GPT Vision error: {e}")
        else:
            # CHAT BIASA PAKAI GPT-OSS 120B DARI GROQ
            comp = client.chat.completions.create(
                messages=[{"role":"system","content":"Kamu MasterAI v7.0, WAJIB Bahasa Indonesia gaul."}] + active["messages"],
                model="openai/gpt-oss-120b"
            )
            ans = comp.choices[0].message.content
            st.markdown(ans)
            active["messages"].append({"role":"assistant","content": ans})
