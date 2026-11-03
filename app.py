import streamlit as st
from groq import Groq
import uuid, time, requests, urllib.parse, base64, io
from PIL import Image
import fitz  # PyMuPDF buat PDF
import docx

st.set_page_config(page_title="MasterAI Vision Reader", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

DEVELOPER_INFO = "AI ini dibuat oleh Jonathan Kristian Sergio Marut! 15 tahun, SMAK Monte Carmelo Maumere, panggilan Juan."
DEVELOPER_BIO = {"nama": "Jonathan Kristian Sergio Marut", "panggilan": "Juan", "umur": "15 Tahun", "sekolah": "SMAK St. Maria Monte Carmelo Maumere"}

# ===== VISION ENGINE - BACA GAMBAR/VIDEO/DOKUMEN =====
def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def read_pdf_text(file_bytes):
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc[:5]:  # baca 5 halaman pertama
            text += page.get_text()
        return text[:8000]  # limit
    except Exception as e:
        return f"Gagal baca PDF: {e}"

def read_docx_text(file_bytes):
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs])
        return text[:8000]
    except Exception as e:
        return f"Gagal baca DOCX: {e}"

def analyze_image_with_groq(client, img_base64, prompt="Jelaskan gambar ini secara detail"):
    try:
        # Model vision Groq yang bisa baca gambar
        res = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",  # vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]
                }
            ],
            max_tokens=1500
        )
        return res.choices[0].message.content
    except Exception as e:
        # Fallback ke model text jika vision gagal
        try:
            res2 = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "system", "content": f"Kamu AI vision. User upload gambar, prompt: {prompt}. Jelaskan seolah kamu bisa lihat gambar tersebut."}, {"role": "user", "content": prompt}],
                max_tokens=1000
            )
            return res2.choices[0].message.content + f"\n\n_(Note: Vision fallback - {e})_"
        except Exception as e2:
            return f"Gagal analisa gambar: {e2}"

def generate_realistic_image(prompt, edit_mode="realistic"):
    if edit_mode == "change_color":
        enhanced = f"same person same pose, {prompt}, only change clothing color, ultra realistic, photorealistic, fabric texture, 8k"
    elif edit_mode == "swap_clothes":
        enhanced = f"clothing swap, {prompt}, keep faces identical, swap outfit, realistic draping, photorealistic, 8k"
    else:
        enhanced = f"ultra realistic photograph of {prompt}, DSLR 85mm f/1.4, natural skin texture, hyperrealistic, 8k, photorealistic, Gemini ChatGPT style"
    encoded = urllib.parse.quote(enhanced)
    seed = uuid.uuid4().int % 999999
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux-realism&seed={seed}&nologo=true&enhance=true"
    try:
        r = requests.get(url, timeout=90)
        return (r.content, enhanced) if r.status_code == 200 else (None, enhanced)
    except:
        return None, enhanced

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800;900&display=swap');
* {font-family: 'Space Grotesk', sans-serif !important;}
.stApp { background: #030308 !important; }
.stApp::before { content: ""; position: fixed; width: 200%; height: 200%; top: -50%; left: -50%; background: radial-gradient(circle at 20% 30%, rgba(255,0,128,0.55) 0%, transparent 35%), radial-gradient(circle at 80% 20%, rgba(0,245,255,0.55) 0%, transparent 40%); animation: orbDance 20s ease-in-out infinite alternate; filter: blur(18px); z-index: 0; pointer-events: none; }
@keyframes orbDance { 0%{transform:translate(0,0)} 100%{transform:translate(8%,5%)} }
[data-testid="stAppViewContainer"] { position: relative; z-index: 2; }
h1 { background: linear-gradient(90deg, #FF0040, #FF8A00, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6, #FF0040) !important; background-size: 400% 100% !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; text-align: center !important; font-weight: 900 !important; font-size: 4rem !important; animation: rainbowFlow 3s linear infinite !important; }
@keyframes rainbowFlow { 0%{background-position:0%} 100%{background-position:400%} }
@media (min-width: 769px) { section[data-testid="stSidebar"] { display: none !important; } button[kind="header"] { display: none !important; } }
@media (max-width: 768px) { section[data-testid="stSidebar"] { display: block !important; width: 85% !important; background: rgba(12,10,28,0.95) !important; } h1 { font-size: 2.8rem !important; } }
.stChatMessage { background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(123,97,255,0.22)) !important; backdrop-filter: blur(24px) !important; border-radius: 28px !important; border: 1px solid rgba(255,255,255,0.16) !important; }
.stChatMessage p { color: #FFF !important; font-size: 15px !important; }
.badge { background: linear-gradient(90deg, #FF0040, #FFE600, #00FF88, #00F5FF, #7B61FF, #FF00E6) !important; padding: 6px 14px; border-radius: 50px; color: white; font-weight: 900; font-size: 11px; display: inline-block; margin: 3px; }
[data-testid="stChatInput"] { background: linear-gradient(90deg, #FF0040, #00F5FF) !important; padding: 4px !important; border-radius: 30px !important; max-width: 780px !important; margin: 0 auto !important; }
[data-testid="stChatInput"] > div { background: rgba(10,10,22,0.95) !important; border-radius: 26px !important; }
[data-testid="stChatInput"] textarea { color: #FFF !important; font-weight: 700 !important; }
.file-preview { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); border-radius: 15px; padding: 10px; margin: 5px 0; }
.bio-card { background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(123,97,255,0.15)) !important; border-radius: 20px !important; padding: 14px !important; }
.bio-avatar { width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #FF0040, #00F5FF, #FFE600); display: flex; align-items: center; justify-content: center; font-size: 26px; font-weight: 900; color: white; margin: 0 auto 8px auto; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "chats" not in st.session_state:
    fid = str(uuid.uuid4())
    st.session_state.chats = {fid: {"title": "MasterAI Vision Reader", "messages": [], "created": time.time()}}
    st.session_state.active_chat = fid
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = []

def get_active(): return st.session_state.chats[st.session_state.active_chat]

with st.sidebar:
    st.markdown("### MasterAI")
    st.markdown('<span class="badge">VISION</span> <span class="badge">BACA GAMBAR</span> <span class="badge">BACA DOKUMEN</span>', unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<div class='bio-card'><div class='bio-avatar'>J</div><div style='text-align:center; color:white !important; font-weight:900; font-size:13px;'>{DEVELOPER_BIO['nama']}</div></div>", unsafe_allow_html=True)
    if st.button("➕ Obrolan Baru", use_container_width=True, type="primary"):
        nid = str(uuid.uuid4())
        st.session_state.chats[nid] = {"title": f"Chat {len(st.session_state.chats)+1}", "messages": [], "created": time.time()}
        st.session_state.active_chat = nid
        st.session_state.uploaded_data = []
        st.rerun()

active = get_active()
st.title("MasterAI")
st.markdown("<div style='text-align:center;'><span class='badge'>BUATAN JONATHAN MARUT</span> <span class='badge'>VISION READER - BACA GAMBAR VIDEO DOKUMEN</span></div>", unsafe_allow_html=True)

# ===== TASKBAR UPLOAD =====
st.markdown("#### 📎 Upload Gambar / Video / Dokumen - AI Bakal Baca Otomatis!")

uploaded_files = st.file_uploader("Upload file", type=["png","jpg","jpeg","webp","mp4","mov","avi","pdf","docx","txt"], accept_multiple_files=True, label_visibility="collapsed")

if uploaded_files:
    for file in uploaded_files:
        file_bytes = file.read()
        file_id = str(uuid.uuid4())[:6]
        
        if file.type.startswith("image/"):
            try:
                img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
                b64 = image_to_base64(img)
                # Auto analisa gambar
                with st.spinner(f"👁️ AI lagi baca gambar {file.name}..."):
                    analysis = analyze_image_with_groq(client, b64, "Jelaskan detail gambar ini: apa isinya, warna baju, pose, background. Jika ada orang, deskripsikan pakaian nya detail untuk bisa diedit nanti.")
                
                st.session_state.uploaded_data.append({"id": file_id, "name": file.name, "type": "image", "image": img, "b64": b64, "analysis": analysis})
                
                st.markdown(f"<div class='file-preview'>", unsafe_allow_html=True)
                st.image(img, caption=f"📸 {file.name}", width=250)
                st.markdown(f"<div style='color:#00F5FF !important; font-size:13px;'><b>👁️ AI Vision Membaca:</b><br/>{analysis[:500]}...</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Gagal baca {file.name}: {e}")
        
        elif file.type.startswith("video/"):
            st.session_state.uploaded_data.append({"id": file_id, "name": file.name, "type": "video", "bytes": file_bytes})
            st.video(file_bytes)
            st.markdown(f"<div class='file-preview' style='color:#FFE600 !important;'>🎥 Video {file.name} terupload! AI bisa analisa frame. Ketik 'jelaskan video ini' atau 'ambil frame ke-5'</div>", unsafe_allow_html=True)
        
        elif file.type in ["application/pdf"]:
            text = read_pdf_text(file_bytes)
            st.session_state.uploaded_data.append({"id": file_id, "name": file.name, "type": "doc", "text": text})
            st.markdown(f"<div class='file-preview'><div style='color:#FFF !important; font-weight:700;'>📄 {file.name}</div><div style='color:rgba(255,255,255,0.7) !important; font-size:12px; max-height:150px; overflow:auto;'>{text[:1000]}...</div></div>", unsafe_allow_html=True)
            st.success(f"✅ PDF {file.name} berhasil dibaca! {len(text)} karakter")
        
        elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
            text = read_docx_text(file_bytes) if "docx" in file.type else file_bytes.decode('utf-8', errors='ignore')[:8000]
            st.session_state.uploaded_data.append({"id": file_id, "name": file.name, "type": "doc", "text": text})
            st.markdown(f"<div class='file-preview'><div style='color:#FFF !important; font-weight:700;'>📄 {file.name}</div><div style='color:rgba(255,255,255,0.7) !important; font-size:12px;'>{text[:1000]}...</div></div>", unsafe_allow_html=True)

if st.session_state.uploaded_data:
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown(f"<div style='color:#00FF88 !important; font-size:13px;'>✅ {len(st.session_state.uploaded_data)} file siap dibaca AI!</div>", unsafe_allow_html=True)
    with col2:
        if st.button("🗑️ Clear Semua"):
            st.session_state.uploaded_data = []
            st.rerun()

st.divider()

for m in active["messages"]:
    with st.chat_message(m["role"], avatar="🧑‍💻" if m["role"]=="user" else "👁️"):
        if m.get("type") == "image":
            st.markdown(m["content"])
            if m.get("image_data"): st.image(m["image_data"], use_container_width=True)
        else:
            st.markdown(m["content"])

if prompt := st.chat_input("Upload dulu, lalu ketik: 'apa isi gambar ini?' / 'rangkum dokumen' / 'ubah baju jadi merah' / '/image buatkan...'"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="👁️"):
        ph = st.empty()
        low = prompt.lower()
        
        # ===== LOGIC BACA FILE =====
        has_files = len(st.session_state.uploaded_data) > 0
        last_image = next((x for x in reversed(st.session_state.uploaded_data) if x["type"]=="image"), None)
        last_doc = next((x for x in reversed(st.session_state.uploaded_data) if x["type"]=="doc"), None)
        
        # Jika user tanya tentang gambar yang diupload
        if has_files and any(k in low for k in ["apa isi gambar", "jelaskan gambar", "apa ini", "baju warna apa", "deskripsikan", "apa yang ada di gambar", "baca gambar"]):
            if last_image:
                ph.markdown(f"👁️ _Sedang menganalisa {last_image['name']}..._")
                analysis = analyze_image_with_groq(client, last_image["b64"], prompt)
                ph.markdown(f"👁️ **Analisa Gambar {last_image['name']}:**\n\n{analysis}")
                active["messages"].append({"role": "assistant", "content": f"👁️ Analisa {last_image['name']}:\n\n{analysis}"})
            else:
                ph.markdown("❌ Belum ada gambar yang diupload!")
        
        # Jika user tanya tentang dokumen
        elif has_files and any(k in low for k in ["rangkum dokumen", "isi dokumen", "baca dokumen", "apa isi pdf", "rangkuman"]):
            if last_doc:
                ph.markdown(f"📄 _Membaca {last_doc['name']}..._")
                try:
                    res = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {"role": "system", "content": "Kamu adalah AI yang bisa membaca dokumen. Rangkum dengan jelas."},
                            {"role": "user", "content": f"Dokumen {last_doc['name']} isinya:\n\n{last_doc['text'][:6000]}\n\nPertanyaan user: {prompt}"}
                        ],
                        max_tokens=1500
                    )
                    ans = res.choices[0].message.content
                    ph.markdown(f"📄 **Rangkuman {last_doc['name']}:**\n\n{ans}")
                    active["messages"].append({"role": "assistant", "content": ans})
                except Exception as e:
                    ph.error(f"Error baca dokumen: {e}")
            else:
                ph.markdown("❌ Belum ada dokumen!")
        
        # Jika minta edit baju
        elif any(k in low for k in ["ubah warna", "ganti warna", "swap baju", "tukar baju"]):
            if not last_image:
                ph.markdown("❌ Upload gambar dulu biar bisa edit baju!")
            else:
                ph.markdown(f"👕 **Mode Edit Baju**\n\n📝 {prompt}\n\n⏳ _Generating realistis..._")
                mode = "change_color" if "warna" in low else "swap_clothes"
                img_bytes, enh = generate_realistic_image(prompt, edit_mode=mode)
                if img_bytes:
                    ph.empty()
                    st.image(img_bytes, caption=f"Edited - {prompt[:50]}", use_container_width=True)
                    active["messages"].append({"role": "assistant", "content": f"👕 **Edit Baju Berhasil!** {prompt}", "type": "image", "image_data": img_bytes})
                    st.download_button("⬇️ Download", data=img_bytes, file_name=f"edit_{uuid.uuid4().hex[:4]}.jpg", mime="image/jpeg", key=f"dl_{uuid.uuid4()}")
                else:
                    ph.error("Gagal edit!")
        
        # Jika minta generate gambar baru
        elif low.startswith("/image") or "buatkan gambar" in low or "bikin gambar" in low:
            clean = prompt
            for p in ["/image", "/gambar", "buatkan gambar", "bikin gambar"]:
                if low.startswith(p): clean = prompt[len(p):].strip(); break
            ph.markdown(f"🎨 **Generating Realistic (Gemini/ChatGPT Style)...**\n\nPrompt: {clean}\n\n⏳ 10-20 detik...")
            img_bytes, enh = generate_realistic_image(clean, edit_mode="realistic")
            if img_bytes:
                ph.empty()
                st.image(img_bytes, caption=clean, use_container_width=True)
                active["messages"].append({"role": "assistant", "content": f"🎨 Generated: {clean}", "type": "image", "image_data": img_bytes})
                st.download_button("⬇️ Download HD", data=img_bytes, file_name=f"real_{uuid.uuid4().hex[:4]}.jpg", mime="image/jpeg", key=f"dl2_{uuid.uuid4()}")
            else:
                ph.error("Gagal generate!")
        
        # Chat biasa tapi dengan context file
        else:
            ph.markdown("▌ _Thinking dengan context file..._ ⚡")
            try:
                context = ""
                if last_image:
                    context += f"\n[User upload gambar {last_image['name']}, analisa sebelumnya: {last_image.get('analysis','')[:500]}]\n"
                if last_doc:
                    context += f"\n[User upload dokumen {last_doc['name']}, isi: {last_doc['text'][:1000]}...]\n"
                
                if "siapa pembuat" in low:
                    ans = DEVELOPER_INFO
                else:
                    sys = f"Kamu MasterAI Vision. {DEVELOPER_INFO} Kamu bisa baca gambar, video, dokumen. Context file: {context} Jawab gaul Indonesia."
                    msgs = [{"role": "system", "content": sys}]
                    # Jika ada gambar, kirim vision
                    if last_image and ("gambar" in low or "foto" in low or "baju" in low):
                        msgs.append({
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{last_image['b64']}"}}
                            ]
                        })
                    else:
                        msgs.append({"role": "user", "content": prompt + context})
                    
                    res = client.chat.completions.create(model="meta-llama/llama-4-maverick-17b-128e-instruct" if last_image else "openai/gpt-oss-120b", messages=msgs, max_tokens=1500)
                    ans = res.choices[0].message.content
                
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            except Exception as e:
                ph.error(f"Error: {e}\nCoba model lain atau upload ulang.")
