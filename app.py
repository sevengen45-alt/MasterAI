import streamlit as st

st.set_page_config(page_title="MasterAI Form Validator", page_icon="🤖")

st.title("🤖 MasterAI")
st.subheader("Form Validator AI")

st.write("Halo! Selamat datang di MasterAI")

nama = st.text_input("Nama Lengkap")
email = st.text_input("Email")
pesan = st.text_area("Pesan / Form yang mau di cek")

if st.button("Validasi Form 🔥"):
    if not nama or not email:
        st.error("Nama dan Email wajib diisi bang! 🗿")
    elif "@" not in email:
        st.error("Email nya salah format! 😭")
    else:
        st.success(f"MANTEP! Form dari {nama} VALID! ✅")
        st.balloons()
        st.write(f"Email: {email}")
        st.write(f"Pesan: {pesan}")

st.caption("Created by Naya - Hosted with Streamlit")
