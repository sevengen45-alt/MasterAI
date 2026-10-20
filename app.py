import streamlit as st
from groq import Groq
import uuid, base64, requests, json

st.set_page_config(page_title="MasterAI v7.1", page_icon="🤖", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "chats" not in st.session_state:
    fid=str(uuid.uuid4())
    st.session_state.chats={fid:{"title":"Obrolan Baru ✨","messages":[{"role":"assistant","content":"v7.1 GPT ONLY ON! 🤖"}]}}
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
    active["messages"].append({"role":"user","content":prompt})
    with st.chat_message("assistant"):
        if st.session_state.last_upload:
            with st.spinner("🤖 GPT lagi ngeliat..."):
                try:
                    b64 = base64.b64encode(st.session_state.last_upload.getvalue()).decode('utf-8')
                    payload = {
                        "model": "openai",
                        "messages": [{"role":"user","content":[
                            {"type":"text","text":prompt},
                            {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                        ]}]
                    }
                    r = requests.post("https://text.pollinations.ai/openai", json=payload, timeout=90)
                    data = r.json()
                    ans = data['choices'][0]['message']['content'] if 'choices' in data else str(data)
                    st.markdown(ans)
                    active["messages"].append({"role":"assistant","content":ans})
                    st.session_state.last_upload=None
                except Exception as e:
                    st.error(f"Error: {e} - Coba lagi, Pollinations kadang lemot")
                    st.json(r.text[:1000] if 'r' in locals() else "no response")
        else:
            comp = client.chat.completions.create(messages=[{"role":"system","content":"Wajib Indo gaul"}]+active["messages"], model="openai/gpt-oss-120b")
            ans=comp.choices[0].message.content
            st.markdown(ans)
            active["messages"].append({"role":"assistant","content":ans})
