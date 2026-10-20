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
              try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b", # model baru yang tadi
        messages=[
            {"role": "user", "content": pertanyaan}
        ]
    )
    hasil = response.choices[0].message.content
    st.success(hasil)

except Exception as e:
    st.error(f"Error: {e}")
                
    else:
        str.warning("Ketik pertanyaan dulu!")
