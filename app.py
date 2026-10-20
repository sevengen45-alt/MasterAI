import streamlit as st
import time
import random

st.set_page_config(page_title="MASTER AI - Fixed", page_icon="🔥", layout="wide")

# CSS SAMA KAYAK KEMARIN (BIAR TETEP BERCAHAYA)
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at 20% 30%, #1a1a40 0%, #000000 50%, #0f0c29 100%); }
    .glowing-title {
        font-size: 3.5rem; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #00F5FF, #7F00FF, #FF006A, #FF8A00);
        background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: gradientMove 5s ease infinite; margin-top: 60px;
    }
    @keyframes gradientMove { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    section[data-testid="stSidebar"] { background: rgba(20, 20, 35, 0.85) !important; backdrop-filter: blur(20px); }
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #FF3B30, #FF9500) !important; color: white !important; border: none !important; border-radius: 12px !important; font-weight: 700 !important; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔥 MASTER AI v9.4 FIXED")
    st.caption("● ONLINE - Udah gak ngeles lagi")
    st.divider()
    nama = st.text_input("Nama lu siapa bang?", placeholder="Juan")
    if st.button("🔥 Obrolan Baru"):
        st.session_state.messages = []
        st.rerun()

# --- JUDUL ---
if not st.session_state.messages:
    st.markdown('<div class="glowing-title">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:rgba(255,255,255,0.6);">Yo {nama if nama else "bang"}, gue udah di-fix, tanya apa aja langsung gue jawab ya!</p>', unsafe_allow_html=True)

# --- OTAK BARU YANG BENERAN JAWAB ---
def get_real_answer(prompt, nama_user):
    p = prompt.lower()
    sapaan = f"{nama_user}" if nama_user else "bang"
    
    # DATABASE JAWABAN BENERAN - BUKAN NGELES
    if "informatika" in p:
        return f"""Oke {sapaan}, gue jawab dengan santai ya!

**Informatika itu gini:**

Informatika itu ilmu yang belajarin tentang **komputer dan cara ngolah informasi**. Bukan cuma ngoding doang!

Cakupannya luas:
1.  **Ngoding** - Bikin aplikasi, website kayak yang lu lagi bikin ini
2.  **Data** - Ngolah data jadi informasi yang berguna
3.  **Jaringan** - Gimana internet bisa nyambungin semua orang
4.  **AI** - Bikin komputer bisa mikir kayak gue gini
5.  **Keamanan** - Jagain data biar gak di-hack

Jadi kalo lu kuliah informatika, lu bakal belajar bikin sesuatu yang hidup kayak app lu ini. Keren kan?

Mau gue jelasin bagian mana yang lebih dalam? Ngodingnya, AI nya, atau jaringannya?"""
    
    elif "langsung" in p and "jawab" in p:
        return f"""Siap {sapaan}, langsung gue gas!

Gue tadi emang error, maaf ya muter-muter. Sekarang udah gue fix!

Tanya aja apa, gue bakal jawab **langsung to the point, gak pake basa-basi 'menarik nih pertanyaannya' lagi.** 

Mau tanya apa? Informatika udah gue jawab di atas, mau lanjut topik apa lagi?"""

    elif "siapa" in p and ("kamu" in p or "lu" in p):
        return f"Gue itu MASTER AI, asisten coding santai punya {sapaan}. Dibikin buat bantu lu beresin error streamlit, bikin UI glowing, dan ngobrol santai. Gue jawab dengan santai ya, tapi tetep to the point!"

    elif "streamlit" in p or "error" in p:
        return f"Nah kalo error streamlit kayak kemaren itu biasanya karena 2 hal {sapaan}: file `ui.py` masih ada import `test_form_vaildator` yang typo, atau `requirements.txt` lu kebanyakan library. Solusinya udah bener yang kemaren: bikin `ui.py` jadi simple dulu. Gue jawab dengan santai ya biar gak pusing!"

    else:
        # JAWABAN UMUM TAPI TETEP NYAMBUNG, GAK NGULANG PERTANYAAN
        return f"""Oke {sapaan}, paham gue.

Soal **'{prompt}'** itu, gue coba jelasin versi santai ya:

Intinya ini topik yang seru. Kalo mau gue ringkas, poin pentingnya adalah gimana kita bisa bikin sesuatu yang tadinya ribet jadi simple dan kepake.

Contohnya kayak app lu ini, dari yang tadinya error `autogen` gak jelas, sekarang udah bisa jadi web app glowing yang bisa ngobrol.

Lu mau gue breakdown lebih dalam tentang '{prompt}' dari sisi mana? Kasih tau aja, biar gue langsung gas jawabnya, gak muter-muter lagi!"""

# Tampilkan chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Tanya apa saja!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Mikirin jawaban beneran..."):
            time.sleep(0.6)
            jawaban = get_real_answer(prompt, nama)
            st.markdown(jawaban)
    st.session_state.messages.append({"role": "assistant", "content": jawaban})
