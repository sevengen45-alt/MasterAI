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
    background: linear-gradient(90deg, #FF0040,
