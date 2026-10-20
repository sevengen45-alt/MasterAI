import streamlit as str
from groq import Groq

# 1. Konfigurasi Tampilan Web Simpel (Persis Versi Aslimu)
str.title("MasterAI")
str.write("Silahkan tanya apa saja pada AI ini")

# 2. Masukkan API Key Groq kamu di bawah ini
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# 3. Wadah Input User
user_input = str.text_input("Pertanyaan :")

# 4. Eksekusi Saat Tombol Diklik
if str.button("Tanya"):
    if user_input:
        with str.spinner("Tunggu..."):
            try:
                # Panggil mesin Groq super cepat
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": user_input}]
                )
                jawaban = response.choices.message.content
                
                # Tampilkan hasil jawaban
                str.write(jawaban)
                
            except Exception as e:
                str.error(f"Error: {e}")
    else:
        str.warning("Ketik pertanyaan dulu!")
