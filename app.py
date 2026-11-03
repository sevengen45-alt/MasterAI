import streamlit as st
from groq import Groq
import uuid, time, requests, urllib.parse

st.set_page_config(page_title="MasterAI", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! 15 tahun, SMAK St. Maria Monte Carmelo Maumere, panggilan Juan."
DEVELOPER_BIO = {
    "nama": "Jonathan Kristian Sergio Marut", "panggilan": "Juan", "umur": "15 Tahun",
    "sekolah": "SMAK St. Maria Monte Carmelo Maumere", "lokasi": "Maumere, NTT 🇮🇩",
    "motto": "Umur 15 tahun bukan halangan buat bikin AI keren! 🔥",
}

# ===== AUTO IMAGE ENGINE - DALL-E x MIDJOURNEY JADI 1 TANPA OPSI =====
def auto_enhance_prompt(user_prompt):
    # Auto jadi Midjourney v6 + DALL-E 3 hybrid - tanpa pilih-pilih
    return f"{user_prompt}, ultra detailed, cinematic lighting, photorealistic, masterpiece, 8k, highly detailed, DALL-E 3 and Midjourney v6 style, vibrant colors, sharp focus, trending on ArtStation"

def generate_image_auto(prompt):
    enhanced = auto_enhance_prompt(prompt)
    encoded = urllib.parse.quote(enhanced)
    seed = uuid.uuid4().int % 999999
    # Auto model terbaik - FLUX = Midjourney v6 killer
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux&seed={seed}&nologo=true&enhance=true&safe=false"
    try:
        r = requests.get(url, timeout=90)
        if r.status_code == 200:
            return r.content, enhanced
        return None, enhanced
    except:
        return None, enhanced

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}
.stApp { background: #030308 !important; }
.stApp::before {
    content: ""; position: fixed; width: 200%; height: 200%; top: -50%; left: -50%;
    background: radial-gradient(circle at 20% 30%, rgba(255,0,128,0.55) 0%, transparent 35%),
                radial-gradient(circle at 80% 20%, rgba(0,245,255,0.55) 0%, transparent 40%),
                radial-gradient(circle at 50% 80%, rgba(255,230,0,0.45) 0%, transparent 40%);
    animation: orbDance 20s ease-in-out infinite alternate; filter: blur(18px); z-index: 0; pointer-events: none;
}
@keyframes orbDance { 0%{transform:translate(0,0)} 100%{transform:translate(8%,5%)} }
[data-testid="stAppViewContainer"] { position: relative; z-index: 2; }
h1 {
    background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040) !important;
    background-size: 400% 100% !important; -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important; text-align: center !important; font-weight: 900 !important; font-size: 4.5rem !important;
    animation: rainbowFlow 3s linear infinite !important;
}
@keyframes rainbowFlow { 0%{background-position:0%} 100%{background-position:400%} }

/* ===== SIDEBAR KHUSUS HP - MINIMIZE ===== */
section[data-testid="stSidebar"] {
    background: rgba(12,10,28,0.92) !important; backdrop-filter: blur(30px) !important;
    border-right: 3px solid #FF00E6 !important; width: 300px !important;
}

/* DI DESKTOP: SEMBUNYIKAN TOMBOL SIDEBAR, SIDEBAR SELALU KETUTUP */
@media (min-width: 769px) {
    section[data-testid="stSidebar"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
}

/* DI HP: SIDEBAR BISA DIGESER */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] { display: block !important; width: 85% !important; }
    button[kind="header"] { display: block !important; background: linear-gradient(90deg, #FF0040, #00F5FF) !important; color: white !important; border-radius: 12px !important; }
    h1 { font-size: 2.8rem !important; }
}

.stChatMessage { background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(123,97,255,0.22)) !important; backdrop-filter: blur(24px) !important; border-radius: 28px !important; border: 1px solid rgba(255,255,255,0.16) !important; }
.stChatMessage p { color: #FFF !important; font-size: 16px !important; }
.badge { background: linear-gradient(90deg, #FF0040, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6) !important; padding: 6px 14px; border-radius: 50px; color: white; font-weight: 900; font-size: 11px; display: inline-block; margin: 3px; }
[data-testid="stChatInput"] { background: linear-gradient(90deg, #FF0040, #00F5FF) !important; padding: 4px !important; border-radius: 30px !important; max-width: 780px !important; margin: 0 auto !important; }
[data-testid="stChatInput"] > div { background: rgba(10,10,22,0.95) !important; border-radius: 26px !important; }
[data-testid="stChatInput"] textarea { color: #FFF !important; font-weight: 700 !important; }
.bio-card { background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(123,97,255,0.15)) !important; border-radius: 20px !important; padding: 14px !important; }
.bio-avatar { width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #FF0040, #00F5FF, #FFE600); display: flex; align-items: center; justify-content: center; font-size: 30px; font-weight: 900; color: white; margin: 0 auto 10px auto; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "MasterAI DALL-E x Midjourney", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI")
    st.markdown('<span class="badge">DALL-E 3</span> <span class="badge">MIDJOURNEY v6</span> <span class="badge">AUTO</span>', unsafe_allow_html=True)
    st.divider()
    
    # BIO AJA, TANPA OPSI GAMBAR LAGI!
    st.markdown(f"<div class='bio-card'><div class='bio-avatar'>J</div><div style='text-align:center; color:white !important; font-weight:900;'>{DEVELOPER_BIO['nama']}</div><div style='text-align:center; color:#00F5FF !important; font-size:11px;'>{DEVELOPER_BIO['panggilan']} • {DEVELOPER_BIO['umur']}</div><div style='text-align:center; color:rgba(255,255,255,0.6) !important; font-size:10px; margin-top:5px;'>{DEVELOPER_BIO['sekolah']}</div></div>", unsafe_allow_html=True)
    
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    
    st.markdown("#### 💬 Riwayat")
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True)[:20]:
        if st.button(f"💬 {chat['title'][:24]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()
    
    st.divider()
    st.markdown("<div style='font-size:11px; color:rgba(255,255,255,0.5) !important; text-align:center;'>📱 Sidebar cuma muncul di HP<br/>Di laptop auto hide biar clean</div>", unsafe_allow_html=True)

active = get_active()
st.title("MasterAI")
st.markdown(f"<div style='text-align:center;'><span class='badge'>BUATAN {DEVELOPER_BIO['nama'].upper()}</span> <span class='badge'>DALL-E 3 + MIDJOURNEY AUTO</span></div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; color:rgba(255,255,255,0.7) !important; font-size:13px; margin:10px 0;">
Ketik aja: <b style="color:#00F5FF !important;">/image pemandangan Maumere</b> atau <b style="color:#FF00E6 !important;">buatkan gambar anime</b> - otomatis jadi karya seni! 🎨
</div>
""", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "🎨"):
        if m.get("type") == "image":
            st.markdown(m["content"])
            if m.get("image_data"):
                st.image(m["image_data"], caption=m.get("caption",""), use_container_width=True)
        else:
            st.markdown(m["content"])

if prompt := st.chat_input("Ketik /image anime boy Maumere... atau chat biasa..."):
    # AUTO DETEKSI GAMBAR - TANPA OPSI!
    is_image = False
    clean = prompt
    low = prompt.lower()
    if low.startswith("/image"): 
        is_image = True
        clean = prompt[6:].strip()
    elif low.startswith("/gambar") or low.startswith("/buat gambar") or any(k in low for k in ["buatkan gambar", "bikin gambar", "buatin gambar", "gambar anime", "buatkan foto", "generate image", "create image"]):
        is_image = True
        for pref in ["/gambar", "/buat gambar", "buatkan gambar", "bikin gambar", "buatin gambar"]:
            if low.startswith(pref):
                clean = prompt[len(pref):].strip()
                break
        if clean == prompt: # kalo pake kalimat natural
            clean = prompt
    
    if len(active["messages"]) == 0: active["title"] = clean[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🎨"):
        if is_image and clean:
            ph = st.empty()
            ph.markdown(f"🎨 **Auto DALL-E x Midjourney Mode**\n\n📝 Prompt: `{clean}`\n\n⚡ _Sedang melukis masterpiece... 10-15 detik..._")
            
            img_bytes, enhanced = generate_image_auto(clean)
            
            if img_bytes:
                ph.empty()
                st.image(img_bytes, caption=f"Auto DALL-E x Midjourney | {clean}", use_container_width=True)
                active["messages"].append({
                    "role": "assistant", 
                    "content": f"🎨 **Berhasil!** Prompt: {clean}", 
                    "type": "image", "image_data": img_bytes, "caption": clean
                })
                st.download_button("⬇️ Download HD", data=img_bytes, file_name=f"masterai_{uuid.uuid4().hex[:5]}.jpg", mime="image/jpeg", key=f"dl_{uuid.uuid4()}")
            else:
                ph.error("❌ Gagal, coba prompt lain!")
        else:
            ph = st.empty()
            ph.markdown("▌ _Thinking..._ ⚡")
            try:
                if "siapa pembuat" in low:
                    ans = f"{DEVELOPER_INFO} - {DEVELOPER_BIO['nama']} 🔥"
                else:
                    sys = f"Kamu MasterAI DALL-E x Midjourney Auto. {DEVELOPER_INFO} Jawab gaul. Kalo user minta gambar, bilang: ketik /image [deskripsi]"
                    res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role":"system","content":sys},{"role":"user","content":prompt}], max_tokens=1000)
                    ans = res.choices[0].message.content
                ph.markdown(ans)
                active["messages"].append({"role":"assistant","content":ans})
            except Exception as e:
                ph.error(f"Error: {e}")
