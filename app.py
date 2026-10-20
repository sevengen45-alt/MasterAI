import streamlit as st
import wikipedia
from duckduckgo_search import DDGS

st.set_page_config(page_title="MASTER AI - Hidup & Riset", page_icon="✨", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: #0A0A0F;
        background-image: 
            radial-gradient(at 0% 0%, rgba(120, 119, 198, 0.3) 0px, transparent 50%),
            radial-gradient(at 50% 0%, rgba(255, 119, 198, 0.2) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(120, 219, 255, 0.2) 0px, transparent 50%);
    }
    .main-title {
        font-size: 3rem; font-weight: 800; text-align: center;
        background: linear-gradient(100deg, #A5B4FC, #F0ABFC, #93C5FD, #6EE7B7);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-size: 200% 200%; animation: move 6s ease infinite;
        margin-top: 40px;
    }
    @keyframes move { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 20px !important; backdrop-filter: blur(12px);
    }
    section[data-testid="stSidebar"] { background: #111119 !important; }
    .research-badge {
        display: inline-block; background: linear-gradient(90deg, #00F5FF, #7F00FF);
        color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {"Obrolan Baru": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Obrolan Baru"
if "messages" not in st.session_state:
    st.session_state.messages = []

def realtime_research(query):
    try:
        wikipedia.set_lang("id")
        try:
            summary = wikipedia.summary(query, sentences=3)
            return summary, f"Wikipedia: {query}"
        except: pass
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                combined = "\n".join([r['body'] for r in results[:2]])
                return combined[:600] + "...", "DuckDuckGo Search"
    except: return None, None
    return None, None

def is_important_question(prompt):
    keywords = ["apa itu","siapa","sejarah","matematika","mtk","ipa","rumus","penemu","jelaskan"]
    return any(k in prompt.lower() for k in keywords)

def get_smart_answer(prompt, nama):
    sapaan = f"bang {nama}" if nama else "bang"
    research_data, source = None, None
    if is_important_question(prompt):
        research_data, source = realtime_research(prompt)

    if "informatika" in prompt.lower():
        base = f"""Oke {sapaan}, gue jawab dengan santai ya!

**Informatika itu ilmu tentang komputer & informasi.**
1. **Ngoding** - Bikin app kayak gini
2. **Data & AI** - Bikin komputer bisa mikir
3. **Jaringan** - Gimana internet nyambung
4. **Keamanan** - Jagain data

Lu udah praktekin langsung!
"""
        if research_data: base += f"\n\n**📚 Riset ({source}):**\n{research_data}"
        return base, bool(research_data)

    if research_data:
        return f"""Oke {sapaan}, gue jawab dengan santai ya, udah gue riset real-time!

**{prompt}:**

{research_data}

*Sumber: {source}*""", True

    return f"""Yo {sapaan}, soal **'{prompt}'** paham gue. Kuncinya ada di logikanya. Mau gue breakdown pake analogi atau langsung contoh code? (Kalo Sejarah/MTK/IPA otomatis gue research!)""", False

with st.sidebar:
    st.markdown("## ✨ MASTER AI v10.0")
    if st.button("➕ Obrolan Baru", use_container_width=True):
        new_title = f"Obrolan {len(st.session_state.all_chats)+1}"
        st.session_state.all_chats[new_title] = []
        st.session_state.current_chat = new_title
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("**🕓 Riwayat Obrolan**")
    for title in list(st.session_state.all_chats.keys())[::-1]:
        if st.button(f"💬 {title}", key=title, use_container_width=True):
            st.session_state.current_chat = title
            st.session_state.messages = st.session_state.all_chats[title]
            st.rerun()
    nama = st.text_input("Nama lu?", placeholder="Juan")

st.markdown('<div class="main-title">Siap Memulai Obrolan!</div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("is_research"):
            st.markdown('<span class="research-badge">🔍 REAL-TIME RESEARCH</span>', unsafe_allow_html=True)
        st.markdown(msg["content"])

if prompt := st.chat_input("Tanya apa saja..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.session_state.all_chats[st.session_state.current_chat] = st.session_state.messages
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        jawaban, is_research = get_smart_answer(prompt, nama)
        if is_research: st.markdown('<span class="research-badge">🔍 REAL-TIME RESEARCH</span>', unsafe_allow_html=True)
        st.markdown(jawaban)
    st.session_state.messages.append({"role":"assistant","content":jawaban, "is_research": is_research})
    st.session_state.all_chats[st.session_state.current_chat] = st.session_state.messages
    if "Obrolan" in st.session_state.current_chat:
        new_name = prompt[:25]
        st.session_state.all_chats[new_name] = st.session_state.all_chats.pop(st.session_state.current_chat)
        st.session_state.current_chat = new_name
        st.rerun()
