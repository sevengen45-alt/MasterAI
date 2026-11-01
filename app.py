import streamlit as st
from groq import Groq
import uuid
import time
import requests
from datetime import datetime

st.set_page_config(page_title="MasterAI v10 - Google Search", page_icon="🌐", layout="wide")

# ===== CONFIG DEVELOPER =====
DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."

DEVELOPER_BIO = {
    "nama": "Jonathan Kristian Sergio Marut",
    "panggilan": "Juan",
    "umur": "15 Tahun",
    "sekolah": "SMAK St. Maria Monte Carmelo Maumere",
    "role": "AI Developer & Pelajar",
    "lokasi": "Maumere, NTT, Indonesia 🇮🇩",
    "motto": "Umur 15 tahun bukan halangan buat bikin AI keren! 🔥",
    "skill": ["Python", "Streamlit", "Groq AI", "Google Search API"]
}

# ====== TEKNOLOGI SEARCHING REAL-TIME GOOGLE ======
def google_search_real_time(query, num_results=5):
    """
    Searching langsung ke internet pakai DuckDuckGo (gratis, no API key)
    Mirip Google, real-time! 
    """
    try:
        # Pakai DuckDuckGo Search - gratis & real-time kayak Google
        from duckduckgo_search import DDGS
        
        results_text = ""
        with DDGS() as ddgs:
            # Cari berita / web
            results = list(ddgs.text(query, max_results=num_results))
            
            for i, r in enumerate(results, 1):
                title = r.get('title', '')
                body = r.get('body', '')
                href = r.get('href', '')
                results_text += f"{i}. {title}\n{body}\nSource: {href}\n\n"
        
        return results_text if results_text else "Tidak ada hasil."
    
    except Exception as e:
        # Fallback kalau library belum install - pakai API alternatif
        try:
            # Fallback ke Wikipedia + simple search
            url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
            resp = requests.get(url, timeout=5)
            data = resp.json()
            if data.get('AbstractText'):
