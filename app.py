import streamlit as st
from groq import Groq
import time, uuid, base64
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

st.set_page_config(page_title="MasterAI v6.5 VISION", page_icon="👁️", layout="wide")

st.markdown("""
<style>
    .stApp { background: radial-gradient(ellipse at top, #0f0f23 0%, #000000 100%); }
    h1 { background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; font-size:2.4rem !important; font-weight:800 !important; }
    .stChatMessage { background: rgba(255,255,255,0.06) !important; border-radius: 20px !important; border: 1px solid rgba(123,97,255,0.3) !important; }
    .badge { background: linear-gradient(90deg, #00F5FF, #7B61FF); padding: 5px 12px; border-radius: 20px; color: white; font-size: 11px; margin: 3px; display:inline-block;}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "user_memory" not in st.session_state:
    st.session_state.user_memory = {"nama": None}
if "chats" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.chats = {first_id: {"title": "Obrolan Baru ✨", "messages": [{"role": "assistant", "content": "Yo bang! v6.5 VISION ON! Sekarang gue bisa LIAT gambar lu, gak ngarang trenggiling lagi! 👁️🔥"}], "created": datetime.now().strftime("%d %b")}}
    st.session_state.active_chat = first_id

# SIDEBAR - BERSIH
with st.sidebar:
    st.markdown("## 👨🏼‍💻 MasterAI v6.5")
    if st.session_state.user_memory["nama"]:
        st.success(f"👋 Halo, {st.session_state.user_memory['nama']}!")
    st.markdown('<span class="badge">👁️ VISION FIX</span> <span class="badge">🇮🇩 Indo Only</span> <span class="badge">📎 Chat Fix</span>', unsafe_allow_html=True)
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": datetime.now().strftime("%d %b")}
        st.session_state.active_chat = nid
        st.rerun()

active = st.session_state.chats[st.session_state.active_chat]
st.title(active["title"])

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "👨🏼‍💻"):
        st.markdown(m["content"])
        if "image" in m:
            st.image(m["image"])

st.markdown("---")
c1, c2, c3 = st.columns([1, 6, 1])
with c1:
    uploaded = st.file_uploader("📎", type=["png","jpg","jpeg","webp"], label_visibility="collapsed")
with c2:
    prompt_text = st.text_input("chat", placeholder="Ketik... /gambar, /pdf, atau tanya soal gambar 🗿", label_visibility="collapsed", key="chat_text_v65")
with c3:
    send_btn = st.button("↑", use_container_width=True, type="primary")

if uploaded:
    st.image(uploaded, width=180, caption=f"👁️ {uploaded.name} terdeteksi")

def encode_image(file):
    return base64.b64encode(file.getvalue()).decode('utf-8')

if send_btn and prompt_text:
    low = prompt_text.lower()
    if any(x in low for x in ["nama aku", "panggil aku", "namaku"]):
        try:
            potential = prompt_text.split()[-1].strip(",.!?").capitalize()
            if 2 < len(potential) < 15:
                st.session_state.user_memory["nama"] = potential
        except: pass

    if len(active["messages"]) <= 1:
        active["title"] = prompt_text[:30]

    # Simpan user msg + gambar
    user_msg = {"role": "user", "content": prompt_text}
    if uploaded:
        user_msg["image"] = uploaded
        user_msg["content"] = f"{prompt_text} [dengan gambar {uploaded.name}]"
    active["messages"].append(user_msg)

    with st.chat_message("assistant", avatar="👨🏼‍💻"):
        # CASE 1: /gambar
        if prompt_text.lower().startswith("/gambar"):
            query = prompt_text[7:].strip() or "hacker"
            img_url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}?nologo=true&width=1024&height=1024"
            st.image(img_url, caption=query)
            active["messages"].append({"role": "assistant", "content": f"✅ Gambar '{query}' jadi!"})
        # CASE 2: ADA GAMBAR = PAKAI VISION MODEL
        elif uploaded:
            with st.spinner("👁️ Lagi ngeliat gambar lu..."):
                try:
                    b64 = encode_image(uploaded)
                    nama = st.session_state.user_memory["nama"] or "bang"
                    # PENTING: System prompt anti-Vietnam & anti-ngarang
                    system = f"Kamu MasterAI v6.5, AI gaul Jaksel, teman {nama}. WAJIB jawab pakai Bahasa Indonesia gaul. JANGAN pakai bahasa Vietnam. Kamu bisa melihat gambar. Identifikasi hewan/objek dengan akurat. Jika banteng ya banteng, jangan bilang trenggiling. Jawab santai, jelas, dan akurat."
                    
                    response = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user", "content": [
                                {"type": "text", "text": f"Gambar ini: {prompt_text}. Jelaskan apa ini dengan akurat dalam Bahasa Indonesia gaul."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                            ]}
                        ],
                        max_tokens=1000
                    )
                    answer = response.choices[0].message.content
                    st.markdown(answer)
                    active["messages"].append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Vision error: {e} - Coba lagi")
        # CASE 3: CHAT BIASA = PAKAI GPT-120B
        else:
            try:
                nama = st.session_state.user_memory["nama"] or "bang"
                system = f"Kamu MasterAI v6.5, AI gaul Jaksel buatan {nama}. WAJIB pakai Bahasa Indonesia 100%, jangan campur Vietnam. Jawab gaul, to the point, tapi pinter."
                msgs = [{"role": "system", "content": system}] + [{"role": m["role"], "content": m["content"]} for m in active["messages"] if "image" not in m]
                completion = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b")
                ans = completion.choices[0].message.content
                placeholder = st.empty()
                full = ""
                for ch in ans:
                    full += ch
                    placeholder.markdown(full + "▌")
                    time.sleep(0.004)
                placeholder.markdown(full)
                active["messages"].append({"role": "assistant", "content": full})
            except Exception as e:
                st.error(f"Error: {e}")
    st.rerun()

if prompt_fallback := st.chat_input("Backup chat (kalau tombol ↑ error) 🗿"):
    st.session_state.chat_text_v65 = prompt_fallback
    st.rerun()
