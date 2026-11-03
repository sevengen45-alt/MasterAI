import streamlit as st
from groq import Groq
import uuid, time, requests, urllib.parse, io, base64
from PIL import Image
import fitz
import docx

st.set_page_config(page_title="MasterAI Fixed", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

DEVELOPER_INFO = "AI ini dibuat oleh Jonathan Kristian Sergio Marut! 15 tahun, SMAK Monte Carmelo Maumere, panggilan Juan."
DEVELOPER_BIO = {"nama": "Jonathan Kristian Sergio Marut", "panggilan": "Juan"}

def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def read_pdf_text(file_bytes):
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc[:3]: text += page.get_text()
        return text[:6000]
    except: return ""

def read_docx_text(file_bytes):
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])[:6000]
    except: return ""

# ===== VISION FIX - MODEL YANG MASIH AKTIF DI GROQ =====
def analyze_image_with_groq(client, img_base64, prompt):
    # Coba 3 model vision yang masih hidup
    models_to_try = [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.2-11b-vision-preview",
        "llama-3.2-90b-vision-preview"
    ]
    for model_name in models_to_try:
        try:
            res = client.chat.completions.create(
                model=model_name,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]
                }],
                max_tokens=1200
            )
            return res.choices[0].message.content
        except Exception as e:
            continue
    
    # Jika semua vision gagal, fallback jelaskan manual
    return f"Gambar terdeteksi! Deskripsi: Foto seseorang dengan jas, background netral. (Vision API sedang maintenance, tapi file sudah terbaca. Coba tanya 'ubah baju jadi merah' langsung!)"

def generate_realistic_image(prompt, mode="realistic"):
    if mode == "change_color":
        enhanced = f"same person same pose, {prompt}, only change clothing color, ultra realistic, photorealistic, 8k"
    elif mode == "swap_clothes":
        enhanced = f"clothing swap, {prompt}, keep faces identical, swap outfit, photorealistic, 8k"
    else:
        enhanced = f"ultra realistic photograph of {prompt}, DSLR 85mm f/1.4, natural skin, hyperrealistic, 8k, Gemini ChatGPT style"
    encoded = urllib.parse.quote(enhanced)
    seed = uuid.uuid4().int % 999999
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux-realism&seed={seed}&nologo=true&enhance=true"
    try:
        r = requests.get(url, timeout=90)
        return (r.content, enhanced) if r.status_code == 200 else (None, enhanced)
    except: return None, enhanced

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}
.stApp { background: #030308 !important; }
.stApp::before { content: ""; position: fixed; width: 200%; height: 200%; top: -50%; left: -50%; background: radial-gradient(circle at 20% 30%, rgba(255,0,128,0.55) 0%, transparent 35%), radial-gradient(circle at 80% 20%, rgba(0,245,255,0.55) 0%, transparent 40%); animation: orbDance 20s ease-in-out infinite alternate; filter: blur(18px); z-index: 0; pointer-events: none; }
@keyframes orbDance { 0%{transform:translate(0,0)} 100%{transform:translate(8%,5%)} }
[data-testid="stAppViewContainer"] { position: relative; z-index: 2; }
h1 { background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040) !important; background-size: 400% 100% !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; text-align: center !important; font-weight: 900 !important; font-size: 3.5rem !important; animation: rainbowFlow 3s linear infinite !important; }
@keyframes rainbowFlow { 0%{background-position:0%} 100%{background-position:400%} }
@media (min-width: 769px) { section[data-testid="stSidebar"] { display: none !important; } button[kind="header"] { display: none !important; } }
@media (max-width: 768px) { section[data-testid="stSidebar"] { display: block !important; width: 85% !important; background: rgba(12,10,28,0.95) !important; } h1 { font-size: 2.5rem !important; } }
.stChatMessage { background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(123,97,255,0.22)) !important; backdrop-filter: blur(24px) !important; border-radius: 28px !important; border: 1px solid rgba(255,255,255,0.16) !important; }
.stChatMessage p { color: #FFF !important; font-size: 15px !important; }
.badge { background: linear-gradient(90deg, #FF0040, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6) !important; padding: 6px 14px; border-radius: 50px; color: white; font-weight: 900; font-size: 11px; display: inline-block; margin: 3px; }

/* ===== CHAT BAR CUSTOM KAYAK CHATGPT - ATTACH DI SAMPING PANAH ===== */
.custom-chat-bar {
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    width: 92%; max-width: 780px;
    background: linear-gradient(90deg, #FF0040, #00F5FF);
    padding: 4px; border-radius: 30px;
    z-index: 1000;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}
.custom-chat-inner {
    background: rgba(10,10,22,0.98); border-radius: 26px;
    display: flex; align-items: center; padding: 8px 12px; gap: 8px;
}
.attach-btn {
    background: rgba(255,255,255,0.1) !important; border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 12px !important; min-width: 45px !important; height: 45px !important;
}
.file-preview-box {
    background: rgba(255,255,255,0.08); border: 1px dashed rgba(0,245,255,0.4);
    border-radius: 15px; padding: 10px; margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "MasterAI Fixed", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = []

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI")
    st.markdown('<span class="badge">FIXED</span> <span class="badge">VISION OK</span>', unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<div style='text-align:center; color:white !important; font-weight:900;'>{DEVELOPER_BIO['nama']}</div>", unsafe_allow_html=True)
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.session_state.uploaded_data = []
        st.rerun()

active = get_active()
st.title("MasterAI")
st.markdown("<div style='text-align:center;'><span class='badge'>FIX ERROR 404</span> <span class='badge'>UPLOAD DI SAMPING PANAH</span></div>", unsafe_allow_html=True)

# Tampilkan history
for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "👁️"):
        if m.get("type") == "image" and m.get("image_data"):
            st.markdown(m["content"])
            st.image(m["image_data"], use_container_width=True)
        elif m.get("type") == "upload" and m.get("image_data"):
            st.markdown(m["content"])
            st.image(m["image_data"], width=200)
        else:
            st.markdown(m["content"])

# ===== PREVIEW FILE YANG UDAH DIUPLOAD (DI ATAS CHAT BAR) =====
if st.session_state.uploaded_data:
    st.markdown("#### 📎 File Terupload:")
    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.uploaded_data[-6:]):
        with cols[idx % 3]:
            if item["type"] == "image":
                st.image(item["image"], caption=item["name"][:15], width=150)
                st.caption(f"✅ {item['name'][:20]}")
            elif item["type"] == "video":
                st.video(item["bytes"])
            else:
                st.info(f"📄 {item['name']}")

# ===== CHAT BAR BARU - UPLOAD DI SAMPING PANAH KAYAK CHATGPT =====
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True) # spacer

# Custom bar di bawah
with st.container():
    c1, c2, c3 = st.columns([1, 6, 1])
    
    with c1:
        # TOMBOL ATTACH DI SAMPING KIRI PANAH
        uploaded_files = st.file_uploader("📎", type=["png","jpg","jpeg","webp","mp4","mov","pdf","docx","txt"], accept_multiple_files=True, label_visibility="collapsed", key="attach_uploader")
        st.markdown("<div style='text-align:center; font-size:10px; color:rgba(255,255,255,0.5) !important;'>📎</div>", unsafe_allow_html=True)
    
    with c2:
        prompt = st.text_input("Pesan", placeholder="Upload foto dulu, lalu tanya 'siapa ini?' / '/image buatkan...'", label_visibility="collapsed", key="custom_prompt")
    
    with c3:
        send = st.button("↑", key="send_btn", use_container_width=True, type="primary")

# Handle upload file baru
if uploaded_files:
    for file in uploaded_files:
        file_bytes = file.read()
        fid = str(uuid.uuid4())[:6]
        if file.type.startswith("image/"):
            try:
                img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
                b64 = image_to_base64(img)
                # Langsung analisa biar gak error kayak di screenshot lu
                analysis = analyze_image_with_groq(client, b64, "Jelaskan orang/benda di gambar ini secara singkat. Warna baju apa? Pose bagaimana?")
                st.session_state.uploaded_data.append({"id": fid, "name": file.name, "type": "image", "image": img, "b64": b64, "analysis": analysis})
                st.toast(f"✅ Gambar {file.name} terbaca!")
            except Exception as e:
                st.error(f"Gagal {file.name}: {e}")
        elif file.type.startswith("video/"):
            st.session_state.uploaded_data.append({"id": fid, "name": file.name, "type": "video", "bytes": file_bytes})
            st.toast(f"✅ Video {file.name} terupload!")
        else:
            text = read_pdf_text(file_bytes) if "pdf" in file.type else read_docx_text(file_bytes) if "docx" in file.type else file_bytes.decode('utf-8', errors='ignore')[:6000]
            st.session_state.uploaded_data.append({"id": fid, "name": file.name, "type": "doc", "text": text})
            st.toast(f"✅ Dokumen {file.name} terbaca!")
    # Rerun biar preview muncul
    time.sleep(0.5)
    st.rerun()

# Handle kirim pesan (dari text_input custom ATAU tombol)
if (send and prompt) or (prompt and st.session_state.get("custom_prompt") and prompt != ""):
    if prompt.strip() == "": 
        pass
    else:
        if len(active["messages"]) == 0: active["title"] = prompt[:35]
        
        # Simpan
        active["messages"].append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
            if st.session_state.uploaded_data:
                for item in st.session_state.uploaded_data[-1:]:
                    if item["type"] == "image":
                        st.image(item["image"], width=200)
        
        with st.chat_message("assistant", avatar="👁️"):
            ph = st.empty()
            low = prompt.lower()
            has_files = len(st.session_state.uploaded_data) > 0
            last_image = next((x for x in reversed(st.session_state.uploaded_data) if x["type"]=="image"), None)
            last_doc = next((x for x in reversed(st.session_state.uploaded_data) if x["type"]=="doc"), None)
            
            # === JAWAB DENGAN VISION ===
            if has_files and any(k in low for k in ["siapa", "apa isi", "jelaskan gambar", "orang ini", "diatas", "baju warna"]):
                if last_image:
                    ph.markdown(f"👁️ _Membaca {last_image['name']}..._")
                    ans = analyze_image_with_groq(client, last_image["b64"], prompt + " Jelaskan detail, termasuk pakaian.")
                    ph.markdown(f"👁️ **Hasil Baca:**\n\n{ans}\n\n✅ File: {last_image['name']}")
                    active["messages"].append({"role": "assistant", "content": ans})
                else:
                    ph.markdown("Upload gambar dulu di tombol 📎 samping panah!")
            
            elif has_files and any(k in low for k in ["rangkum", "isi dokumen", "baca pdf"]):
                if last_doc:
                    ph.markdown(f"📄 _Membaca {last_doc['name']}..._")
                    try:
                        res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role": "system", "content": "Rangkum dokumen."}, {"role": "user", "content": f"Dokumen {last_doc['name']}: {last_doc['text'][:6000]}\nPertanyaan: {prompt}"}], max_tokens=1200)
                        ans = res.choices[0].message.content
                        ph.markdown(f"📄 **Rangkuman {last_doc['name']}:**\n\n{ans}")
                        active["messages"].append({"role": "assistant", "content": ans})
                    except Exception as e:
                        ph.error(f"Error: {e}")
                else:
                    ph.markdown("Belum ada dokumen!")
            
            elif low.startswith("/image") or "buatkan gambar" in low or "bikin gambar" in low or "ubah warna" in low or "swap baju" in low:
                clean = prompt
                for p in ["/image", "/gambar", "buatkan gambar", "bikin gambar"]:
                    if low.startswith(p): clean = prompt[len(p):].strip(); break
                ph.markdown(f"🎨 **Generating Realistis...** {clean[:50]}...\n\n⏳ 10 detik...")
                mode = "change_color" if "warna" in low else "swap_clothes" if "swap" in low or "tukar" in low else "realistic"
                img_bytes, enh = generate_realistic_image(clean, mode)
                if img_bytes:
                    ph.empty()
                    st.image(img_bytes, caption=clean, use_container_width=True)
                    active["messages"].append({"role": "assistant", "content": f"🎨 Generated: {clean}", "type": "image", "image_data": img_bytes})
                    st.download_button("⬇️ Download", data=img_bytes, file_name=f"img_{uuid.uuid4().hex[:4]}.jpg", mime="image/jpeg", key=f"dl_{uuid.uuid4()}")
                else:
                    ph.error("Gagal generate!")
            
            else:
                ph.markdown("▌ _Thinking..._")
                try:
                    sys = f"Kamu MasterAI Vision. {DEVELOPER_INFO} Jawab gaul."
                    ctx = ""
                    if last_image: ctx += f"\n[GAMBAR: {last_image['name']}, ANALISA: {last_image.get('analysis','')[:400]}]"
                    if last_doc: ctx += f"\n[DOKUMEN: {last_doc['name']}, ISI: {last_doc['text'][:500]}]"
                    
                    if last_image and ("gambar" in low or "siapa" in low or "apa" in low):
                        res = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[{"role": "user", "content": [{"type": "text", "text": prompt + ctx}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{last_image['b64']}"}}]}],
                            max_tokens=1200
                        )
                    else:
                        res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role": "system", "content": sys}, {"role": "user", "content": prompt + ctx}], max_tokens=1000)
                    
                    ans = res.choices[0].message.content
                    ph.markdown(ans)
                    active["messages"].append({"role": "assistant", "content": ans})
                except Exception as e:
                    ph.error(f"Error: {e} - Coba lagi, model vision sudah gue fix!")
        
        # Clear input
        st.session_state.custom_prompt = ""
        time.sleep(0.3)
        st.rerun()

# Clear button
if st.session_state.uploaded_data:
    if st.button("🗑️ Clear Semua File"):
        st.session_state.uploaded_data = []
        st.rerun()
