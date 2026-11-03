import streamlit as st
from groq import Groq
import uuid, time, requests, urllib.parse

st.set_page_config(page_title="MasterAI DALL-E x Midjourney", page_icon="🎨", layout="wide")

DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! 15 tahun, SMAK St. Maria Monte Carmelo Maumere, panggilan Juan."
DEVELOPER_BIO = {
    "nama": "Jonathan Kristian Sergio Marut", "panggilan": "Juan", "umur": "15 Tahun",
    "sekolah": "SMAK St. Maria Monte Carmelo Maumere", "lokasi": "Maumere, NTT 🇮🇩",
    "motto": "Umur 15 tahun bukan halangan buat bikin AI keren! 🔥",
}

# ===== DALL-E & MIDJOURNEY STYLE PROMPT ENGINE =====
def enhance_prompt(user_prompt, style):
    """Ubah prompt cupu jadi prompt DALL-E / Midjourney dewa"""
    if style == "Midjourney v6 🔥 (Paling Artistik)":
        return f"{user_prompt}, ultra detailed, cinematic lighting, highly detailed, 8k, photorealistic, masterpiece, trending on ArtStation, volumetric lighting, sharp focus, intricate details, --ar 16:9 --style raw --v 6.0"
    elif style == "DALL-E 3 🎨 (Paling Kreatif)":
        return f"A highly detailed digital art illustration of {user_prompt}, vibrant colors, ultra realistic, 4k, masterpiece, digital painting, soft lighting, highly detailed, award winning, DALL-E 3 style"
    elif style == "Anime Midjourney 🌸":
        return f"anime style {user_prompt}, studio ghibli, makoto shinkai, ultra detailed anime, beautiful lighting, 8k, key visual, anime masterpiece"
    elif style == "Realistic Photo 📸 (Foto Real)":
        return f"photograph of {user_prompt}, DSLR, 85mm lens, f/1.8, ultra realistic, natural lighting, 8k, photorealistic, highly detailed skin, real photo"
    else: # Flux Pro
        return f"{user_prompt}, masterpiece, best quality, ultra detailed"

def generate_image(prompt, style_name="Midjourney v6 🔥 (Paling Artistik)", w=1024, h=1024):
    # Enhance dulu prompt nya
    enhanced = enhance_prompt(prompt, style_name)
    encoded = urllib.parse.quote(enhanced)
    seed = uuid.uuid4().int % 999999
    # Model flux = pesaing Midjourney v6 & DALL-E 3
    model = "flux" if "Midjourney" in style_name or "DALL-E" in style_name else "flux-realism" if "Realistic" in style_name else "turbo"
    if "Anime" in style_name: model = "flux-anime"
    
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={w}&height={h}&model={model}&seed={seed}&nologo=true&enhance=true&safe=false"
    try:
        r = requests.get(url, timeout=90)
        if r.status_code == 200:
            return r.content, enhanced, url
        return None, enhanced, None
    except:
        return None, enhanced, None

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
section[data-testid="stSidebar"] { background: rgba(12,10,28,0.85) !important; backdrop-filter: blur(30px) !important; border-right: 3px solid #FF00E6 !important; }
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
    st.markdown('<span class="badge">DALL-E 3</span> <span class="badge">MIDJOURNEY v6</span> <span class="badge">FLUX PRO</span>', unsafe_allow_html=True)
    st.divider()
    st.markdown("#### 🎨 Pilih Style Gambar")
    style = st.selectbox("Style", [
        "Midjourney v6 🔥 (Paling Artistik) - REKOMENDASI",
        "DALL-E 3 🎨 (Paling Kreatif)",
        "Realistic Photo 📸 (Foto Real)",
        "Anime Midjourney 🌸",
        "Flux Pro ⚡ (Super Cepat)"
    ], label_visibility="collapsed")
    st.session_state.img_style = style
    
    col1, col2 = st.columns(2)
    with col1:
        w = st.selectbox("Lebar", [1024, 1280, 720], index=0)
    with col2:
        h = st.selectbox("Tinggi", [1024, 720, 1280], index=0)
    st.session_state.img_size = (w, h)
    
    st.markdown(f"<div style='background:rgba(255,255,255,0.08); padding:10px; border-radius:10px; font-size:11px; color:#FFE600 !important;'>💡 Style {style} aktif!<br/>Midjourney = artistik cinematic<br/>DALL-E 3 = kreatif warna-warni<br/>Realistic = kayak foto beneran</div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown(f"<div class='bio-card'><div class='bio-avatar'>J</div><div style='text-align:center; color:white !important; font-weight:900;'>{DEVELOPER_BIO['nama']}</div><div style='text-align:center; color:#00F5FF !important; font-size:11px;'>{DEVELOPER_BIO['panggilan']} • {DEVELOPER_BIO['umur']}</div></div>", unsafe_allow_html=True)
    
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.rerun()
    st.divider()
    for cid, chat in sorted(st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True)[:15]:
        if st.button(f"{chat['title'][:28]}", key=f"chat_{cid}", use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

active = get_active()
st.title("MasterAI")
st.markdown(f"<div style='text-align:center;'><span class='badge'>BUATAN {DEVELOPER_BIO['nama'].upper()}</span> <span class='badge'>DALL-E 3 + MIDJOURNEY v6</span></div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; background: linear-gradient(90deg, #FF0040, #00F5FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight:900; font-size:18px; margin:10px 0;">
🎨 KETIK AJA /image [deskripsi] - OTOMATIS JADI DALL-E / MIDJOURNEY!
</div>
""", unsafe_allow_html=True)

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "🎨"):
        if m.get("type") == "image":
            st.markdown(m["content"])
            if m.get("image_data"):
                st.image(m["image_data"], caption=m.get("caption",""), use_container_width=True)
                st.download_button("⬇️ Download HD", data=m["image_data"], file_name=f"masterai_{uuid.uuid4().hex[:5]}.jpg", mime="image/jpeg", key=f"dl_{uuid.uuid4()}")
        else:
            st.markdown(m["content"])

if prompt := st.chat_input("Tulis /image anime boy di Maumere sunset ultra detailed... atau chat biasa..."):
    is_image = prompt.lower().startswith("/image") or prompt.lower().startswith("/gambar") or prompt.lower().startswith("/buat gambar")
    clean = prompt
    if prompt.lower().startswith("/image"): clean = prompt[6:].strip()
    elif prompt.lower().startswith("/gambar"): clean = prompt[7:].strip()
    elif prompt.lower().startswith("/buat gambar"): clean = prompt[11:].strip()
    elif any(k in prompt.lower() for k in ["buatkan gambar", "bikin gambar", "gambar anime", "buatkan foto"]):
        is_image = True
    
    if len(active["messages"]) == 0: active["title"] = clean[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🎨"):
        if is_image and clean:
            ph = st.empty()
            style = st.session_state.get("img_style", "Midjourney v6 🔥 (Paling Artistik)")
            w,h = st.session_state.get("img_size", (1024,1024))
            ph.markdown(f"🎨 **Mode:** {style}\n\n📝 **Prompt asli:** {clean}\n\n⚡ _Enhancing prompt jadi DALL-E/Midjourney style..._")
            time.sleep(1)
            ph.markdown(f"🎨 **Generating dengan {style}...**\n\n⏳ _Melukis... 10-20 detik, sabar ya Juan..._ 🔥")
            
            img_bytes, enhanced_prompt, url = generate_image(clean, style_name=style, w=w, h=h)
            
            if img_bytes:
                ph.empty()
                st.success(f"✅ Jadi! Style: {style}")
                st.markdown(f"<div style='color:#AAA !important; font-size:11px;'>Enhanced prompt: {enhanced_prompt[:120]}...</div>", unsafe_allow_html=True)
                st.image(img_bytes, caption=f"{style} | {clean}", use_container_width=True)
                
                active["messages"].append({
                    "role": "assistant", 
                    "content": f"🎨 **Berhasil!**\n\n**Style:** {style}\n**Prompt:** {clean}\n**Enhanced:** {enhanced_prompt[:150]}...", 
                    "type": "image", "image_data": img_bytes, "caption": clean
                })
                st.download_button("⬇️ Download HD Quality", data=img_bytes, file_name=f"masterai_{style[:4]}_{uuid.uuid4().hex[:4]}.jpg", mime="image/jpeg")
            else:
                ph.error("❌ Gagal, coba prompt lain atau ganti style!")
        else:
            ph = st.empty()
            ph.markdown("▌ _Thinking..._ ⚡")
            try:
                if "siapa pembuat" in prompt.lower():
                    ans = f"{DEVELOPER_INFO} - {DEVELOPER_BIO['nama']} 🔥"
                else:
                    sys = f"Kamu MasterAI DALL-E x Midjourney. {DEVELOPER_INFO} Jawab gaul Indonesia."
                    res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role":"system","content":sys},{"role":"user","content":prompt}], max_tokens=1000)
                    ans = res.choices[0].message.content
                ph.markdown(ans)
                active["messages"].append({"role":"assistant","content":ans})
            except Exception as e:
                ph.error(f"Error: {e}")
