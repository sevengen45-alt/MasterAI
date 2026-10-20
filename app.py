import streamlit as st
from groq import Groq
import uuid, base64

st.set_page_config(page_title="MasterAI v8.0", page_icon="🤖", layout="wide")
st.markdown("""
<style>
.stApp{background: radial-gradient(ellipse at top, #0f0f23 0%, #000 100%)}
h1{background:linear-gradient(90deg,#00F5FF,#7B61FF,#FF00E5);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "chats" not in st.session_state:
    fid=str(uuid.uuid4())
    st.session_state.chats={fid:{"title":"Obrolan Baru ✨","messages":[{"role":"assistant","content":"Yo bang! v8.0 COMPOUND ON! 🤖 Chat=GPT-OSS 120B, Vision=Compound-Mini (model baru Groq pengganti Llama Vision yang mati)"}]}}
    st.session_state.active_chat=fid
if "last_upload" not in st.session_state:
    st.session_state.last_upload=None

active=st.session_state.chats[st.session_state.active_chat]
st.title(active["title"])
for m in active["messages"]:
    with st.chat_message(m["role"]): st.markdown(m["content"])

up = st.file_uploader("📎 Upload gambar (Vision Baru)", type=["png","jpg","jpeg","webp"])
if up:
    st.session_state.last_upload=up
    st.image(up, width=250, caption="Siap dianalisa")

if prompt := st.chat_input("Tanya soal gambar / chat biasa..."):
    if len(active["messages"])<=1:
        active["title"]=prompt[:30]
    active["messages"].append({"role":"user","content":prompt})
    
    with st.chat_message("assistant"):
        if st.session_state.last_upload is not None:
            with st.spinner("🤖 Compound Vision lagi ngeliat..."):
                try:
                    b64 = base64.b64encode(st.session_state.last_upload.getvalue()).decode('utf-8')
                    # MODEL BARU GROQ - COMPOUND MINI SUPPORT VISION
                    res = client.chat.completions.create(
                        model="groq/compound-mini",
                        messages=[
                            {"role":"system","content":"Kamu MasterAI v8.0. WAJIB Bahasa Indonesia gaul, jelasin gambar dengan detail akurat. Grid icon ya sebut grid icon."},
                            {"role":"user","content":[
                                {"type":"text","text": prompt},
                                {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                            ]}
                        ],
                        max_tokens=1200
                    )
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    active["messages"].append({"role":"assistant","content":ans})
                    st.session_state.last_upload=None
                except Exception as e:
                    # Kalau compound-mini gak ada, coba compound biasa
                    try:
                        res2 = client.chat.completions.create(
                            model="groq/compound",
                            messages=[
                                {"role":"system","content":"Kamu MasterAI v8.0. WAJIB Bahasa Indonesia gaul."},
                                {"role":"user","content":[
                                    {"type":"text","text": prompt},
                                    {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                                ]}
                            ],
                            max_tokens=1200
                        )
                        ans = res2.choices[0].message.content
                        st.markdown(ans)
                        active["messages"].append({"role":"assistant","content":ans})
                        st.session_state.last_upload=None
                    except Exception as e2:
                        st.error(f"Compound error: {e2}")
                        st.info(f"Detail pertama: {e}")
                        st.warning("Kalau masih error, enable Compound di console.groq.com -> Models")
        else:
            # CHAT BIASA - GPT ONLY
            try:
                comp = client.chat.completions.create(
                    messages=[{"role":"system","content":"Kamu MasterAI v8.0, WAJIB Bahasa Indonesia gaul, kocak, santai."}] + active["messages"],
                    model="openai/gpt-oss-120b"
                )
                ans = comp.choices[0].message.content
                st.markdown(ans)
                active["messages"].append({"role":"assistant","content":ans})
            except Exception as e:
                st.error(f"Chat error: {e}")
