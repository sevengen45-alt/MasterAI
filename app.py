import streamlit as st
from groq import Groq
import uuid
import time

st.set_page_config(page_title="MasterAI v10 - Pure Dark & RGB", page_icon="⚡", layout="wide")

# ===== CONFIG DEVELOPER - ANTI BAJAK + BIO =====
DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."

DEVELOPER_BIO = {
    "nama": "Jonathan Kristian Sergio Marut",
    "panggilan": "Juan",
    "umur": "15 Tahun",
    "sekolah": "SMAK St. Maria Monte Carmelo Maumere",
    "role": "AI Developer & Pelajar",
    "lokasi": "Maumere, NTT, Indonesia 🇮🇩",
    "motto": "Umur 15 tahun bukan halangan buat bikin AI keren! 🔥",
    "skill": ["Python", "Streamlit", "Groq AI", "UI/UX Design", "Prompt Engineering"]
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&family=Inter:wght@400;500;600;700&display=swap');

* {font-family: 'Inter', sans-serif !important;}
h1, h2, h3, h4, h5, h6 {font-family: 'Space Grotesk', sans-serif !important;}

/* THEME PURE DARK: Background Hitam Pekat, Teks Putih */
.stApp {
    background: #000000 !important;
    color: #FFFFFF !important;
}

/* JUDUL - RGB Menyala Terang */
h1 {
    background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040) !important;
    background-size: 400% 100% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-weight: 900 !important;
    font-size: 4.5rem !important;
    letter-spacing: -0.05em !important;
    animation: rainbowFlow 3s linear infinite, floatTitle 3s ease-in-out infinite alternate !important;
    filter: drop-shadow(0 0 25px rgba(255,255,255,0.25));
}
@keyframes rainbowFlow { 0%{background-position:0%} 100%{background-position:400%} }
@keyframes floatTitle { 0%{transform: translateY(0px)} 100%{transform: translateY(-6px)} }
@media (max-width:600px){ h1{font-size:3rem !important;} }

/* SIDEBAR - Hitam dengan Garis RGB Bergerak di Kanan */
section[data-testid="stSidebar"] {
    background: #0A0A0E !important;
    border-right: 3px solid transparent !important;
    position: relative;
}
section[data-testid="stSidebar"]::before {
    content: ""; position: absolute; inset: 0; right: -3px; left: auto; width: 3px;
    background: linear-gradient(180deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040);
    background-size: 100% 400%; animation: borderRun 3s linear infinite;
}
@keyframes borderRun { 0%{background-position:0% 0%} 100%{background-position:0% 400%} }

/* CHAT MESSAGE - Kartu Hitam Elegan dengan Border Putih Tipis */
.stChatMessage {
    background: #0E0E12 !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.8) !important;
    padding: 16px !important;
    transition: all 0.3s ease !important;
}
.stChatMessage:hover {
    border-color: rgba(0,245,255,0.6) !important;
    box-shadow: 0 12px 40px rgba(0,245,255,0.15) !important;
}
.stChatMessage p { color: #FFFFFF !important; font-size: 16px !important; line-height: 1.6 !important; }
.stChatMessage strong { color: #00F5FF !important; }

/* BADGE RGB */
.badge {
    background: linear-gradient(90deg, #FF0040, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6) !important;
    background-size: 300% 100% !important;
    animation: rainbowFlow 2s linear infinite !important;
    padding: 5px 14px; border-radius: 50px; color: white; font-weight: 900; font-size: 11px;
    display: inline-block; margin: 4px; letter-spacing: 0.08em;
    box-shadow: 0 0 15px rgba(0,245,255,0.3);
}

/* CHAT INPUT - Bingkai RGB Tipis & Elegan */
[data-testid="stChatInput"] {
    background: linear-gradient(90deg, #FF0040, #00F5FF, #FFE600, #FF0040) !important;
    background-size: 300% 100% !important;
    animation: rainbowFlow 4s linear infinite !important;
    border-radius: 26px !important;
    max-width: 780px !important; margin: 0 auto !important;
    padding: 2px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6) !important;
}
[data-testid="stChatInput"] > div {
    background: #0A0A0E !important;
    border-radius: 24px !important;
    border: none !important;
}
[data-testid="stChatInput"] textarea { color: #FFFFFF !important; font-weight: 500 !important; font-size: 16px !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #00F5FF, #7B61FF) !important;
    color: white !important;
    border-radius: 1
