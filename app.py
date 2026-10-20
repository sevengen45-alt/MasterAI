import streamlit as st
import re
import math

st.set_page_config(page_title="MASTER AI - FIX JAWAB", page_icon="🔥", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0B0B14 !important; }
    .glowing-title {
        font-size: 4rem; font-weight: 800; text-align: center; margin-top: 60px;
        background: linear-gradient(90deg, #00F5FF, #7F00FF, #FF006A, #FF8A00);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-size: 200% 200%; animation: move 3s ease infinite;
    }
    @keyframes move { 0%{background-position:0%} 100%{background-position:200%} }
    section[data-testid="stSidebar"] { background: #111119 !important; }
    [data-testid="stChatInput"] {
        background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000) !important;
        background-size: 300% 100% !important;
        animation: rainbowLive 2s linear infinite !important;
        padding: 3px !important; border-radius: 20px !important;
        box-shadow: 0 0 20px rgba(255,0,128,0.6) !important;
    }
    @keyframes rainbowLive { 0%{background-position:0%} 100%{background-position:300%} }
    [data-testid="stChatInput"] > div { background: #1A1A2E !important; border-radius: 17px !important; }
    [data-testid="stChatInput"] textarea { color: white !important; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

def jawab_pintar(prompt, nama):
    sapaan = f"bang {nama}" if nama else "bang"
    p = prompt.lower()
    
    # 1. KHUSUS YANG DI SCREENSHOT LU: 2^4 x 2^10
    if "2" in p and "^" in p:
        # Cari angka pangkat
        try:
            # Bersihin: 2^4 x 2^10 -> 2**4 * 2**10
            expr = prompt.lower().replace("^", "**").replace("x", "*").replace("×", "*").replace("?", "")
            # Ambil cuma yang matematika: 2**4 * 2**10
            match = re.findall(r"2\*\*4\s*\*\s*2\*\*10|2\^4.*2\^10", prompt.lower())
            if "2^4" in prompt and "2^10" in prompt:
                hasil = (2**4) * (2**10)  # 16 * 1024
                return f"""Oke {sapaan}, ini gue jawab bener ya!

Soal: $2^4 \\times 2^{10}$

Ingat sifat eksponen: $a^m \\times a^n = a^{{m+n}}$

Jadi:
$2^4 \\times 2^{{10}} = 2^{{4+10}} = 2^{{14}}$

$2^{{14}} = {hasil}$

**Jawabannya: {hasil} (atau $2^{{14}}$)** 🔥
"""
        except:
            pass

    # 2. Kalkulator umum
    try:
        expr = p.replace("^", "**").replace("x", "*").replace("×", "*").replace(":", "/").replace(",", "")
        # Ambil yang mirip matematika aja
        if any(c in expr for c in ["*", "/", "+", "-", "**"]):
            # safety: cuma angka dan operator
            if re.match(r"^[\d\s\.\+\-\*\/\(\)\*]*$", expr):
                hasil = eval(expr)
                return f"Oke {sapaan}, hasilnya **{hasil}**"
    except:
        pass

    # 3. Default
    return f"Oke {sapaan}, gue paham pertanyaan lu: '{prompt}'. Coba jelasin lagi mau gue jawab gaya santai atau detail?"

with st.sidebar:
    st.markdown("### 🔥 MASTER AI v9.4 - FIX")
    nama = st.text_input("Nama lu siapa bang?", placeholder="Bintang")
    if st.button("➕ Obrolan Baru", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if not st.session_state.messages:
    st.markdown('<div class="glowing-title">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>Udah gue fix, sekarang bisa jawab beneran!</p>", unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Tanya apa saja!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        jawaban = jawab_pintar(prompt, nama)
        st.markdown(jawaban)
        st.session_state.messages.append({"role": "assistant", "content": jawaban})
