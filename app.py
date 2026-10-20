import streamlit as st
from groq import Groq
import uuid, base64, requests

st.set_page_config(page_title="MasterAI v7.2 GPT", page_icon="🤖", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "chats" not in st.session_state:
    fid=str(uuid.uuid4())
    st.session_state.chats={fid:{"title":"Obrolan Baru ✨","messages":[{"role":"assistant","content":"Yo bang! v7.2 GPT + GEMINI VISION ON! 🤖 Chat=GPT-OSS 120B, Vision=Gemini 2.0 (support gambar)"}]}}
    st.session_state.active_chat=fid
if "last_upload" not in st.session_state:
    st.session_state.last_upload=None

active=st.session_state.chats[st.session_state.active_chat]
st.title(active["title"])
for m in active["messages"]:
    with st.chat_message(m["role"]): st.markdown(m["content"])

up = st.file_uploader("📎 Upload gambar (GPT Vision)", type=["png","jpg","jpeg","webp"])
if up:
    st.session_state.last_upload=up
    st.image(up, width=250)

if prompt := st.chat_input("Tanya soal gambar..."):
    if len(active["messages"]) <= 1:
        active["title"]=prompt[:25]
    active["messages"].append({"role":"user","content":prompt})
    with st.chat_message("assistant"):
        if st.session_state.last_upload:
            with st.spinner("👁️ Gemini Vision lagi ngeliat..."):
                try:
                    b64 = base64.b64encode(st.session_state.last_upload.getvalue()).decode('utf-8')
                    payload = {
                        "model": "gemini",  # GANTI KE GEMINI - SUPPORT GAMBAR!
                        "messages": [{"role":"user","content":[
                            {"type":"text","text": f"{prompt} Jawab Bahasa Indonesia gaul, jelasin gambar ini detail"},
                            {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                        ]}],
                        "max_tokens": 1000
                    }
                    r = requests.post("https://text.pollinations.ai/openai", json=payload, timeout=90)
                    data = r.json()
                    if 'choices' in data:
                        ans = data['choices'][0]['message']['content']
                    else:
                        ans = str(data)
                    st.markdown(ans)
                    active["messages"].append({"role":"assistant","content":ans})
                    st.session_state.last_upload=None
                except Exception as e:
                    st.error(f"Error vision: {e}")
        else:
            comp = client.chat.completions.create(
                messages=[{"role":"system","content":"Kamu MasterAI v7.2, WAJIB Bahasa Indonesia gaul."}]+active["messages"],
                model="openai/gpt-oss-120b"
            )
            ans=comp.choices[0].message.content
            st.markdown(ans)
            active["messages"].append({"role":"assistant","content":ans})
