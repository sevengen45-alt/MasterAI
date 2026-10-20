import streamlit as st
from groq import Groq

st.title("MasterAI")
st.write("Silahkan tanya apa saja pada AI ini")

pertanyaan = st.text_input("Pertanyaan :")

if st.button("Tanya"):
    if pertanyaan:
        try:
            # Ambil API Key dari Secrets Streamlit (bukan dari file .env lagi pas deploy)
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "user", "content": pertanyaan}
                ]
            )
            
            jawaban = response.choices[0].message.content
            st.success(jawaban)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Tulis pertanyaan dulu bang")
