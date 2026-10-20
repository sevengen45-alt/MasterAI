import streamlit as st
from groq import Groq
import time

st.set_page_config(page_title="MasterAI", page_icon="👨🏼‍💻", layout="wide")

# ===== CSS MODERN SUPER CANGGIH =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    .stApp {
        background: radial-gradient(circle at 20% 30%, #1a1a2e 0%, #0f0f1e 40%, #000000 100%);
        font-family: 'Inter', sans-serif;
    }
    h1 {
        font-weight: 800 !important;
        background: linear-gradient(90deg, #00F5FF, #7B61FF, #FF00E5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem !important;
        letter-spacing: -2px;
    }
    .stChatMessage {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        padding: 15px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    div[data-testid="stChatInput"] {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        backdrop-filter: blur(20px);
    }
    .stCaption { text-align: center; color: #888 !important; }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR CANGGIH =====
with st.sidebar:
    st.markdown("## ⚙️ MasterAI Control")
    st.markdown("---")
    model_choice = st.selectbox("🧠 Pilih Otak AI:", 
        ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3-32b", "llama-3.3-70b-versatile"])
    st.markdown("---")
    st.markdown("### 👨🏼‍💻 Status")
    st.success("✅ Groq API: Connected")
    st.info(f"💬 Total Chat: {len(st.session_state.get('messages', []))}")
    if st.button("🗑️ Hapus Semua Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Made with 💀 by You - MasterAI v3.0")

# ===== LOGIC =====
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ API Key belum ada di Secrets!")
    st.stop()

st.title("MasterAI")
st.caption("MasterAI v3.0 • Hacker Edition • Lebih cepat, lebih canggih, lebih gelap 🖤")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Yo bang! 😎 MasterAI v3.0 udah aktif. Mau tanya apa hari ini? 👨🏼‍💻"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"]=="user" else "🤖"):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ketik pertanyaan kamu di sini, bebas!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👤"):
        with st.spinner("MasterAI lagi memproses pertanyaan  mu😉👌🏼..."):
            try:
                completion = client.chat.completions.create(
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    model=model_choice,
                )
                response = completion.choices[0].message.content
                placeholder = st.empty()
                full = ""
                for c in response:
                    full += c
                    placeholder.markdown(full + "▌")
                    time.sleep(0.005)
                placeholder.markdown(full)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Coba ganti otak AI di sidebar kiri ke gpt-oss-20b")
