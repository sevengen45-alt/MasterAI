if prompt := st.chat_input(f"Tanya apa {st.session_state.user_memory['nama'] or 'saja!'} 🌈✨"):
    if len(active["messages"]) == 0: active["title"] = prompt[:35]
    active["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="🌈"):
        ph = st.empty()
        ph.markdown("▌ _Thinking...")
        try:
            DEVELOPER_INFO = "AI ini dibuat oleh developer bernama Jonathan Kristian Sergio Marut! Dia ADALAH seorang anak yang masih berumur 15 tahun, tetapi sudah mampu membuat AI seperti ku. Dia adalah seorang pelajar di SMAK St. Maria Monte Carmelo Maumere, dan Ia biasanya dipanggil Juan."
            nama = st.session_state.user_memory["nama"] or "bang"
            
            # CEK DULU APAKAH NANYA PEMBUAT
            if any(k in prompt.lower() for k in ["siapa yang membuat", "siapa pembuat", "siapa yg membuat", "who made you", "dibuat siapa", "buatan siapa", "developer"]):
                ans = f"Yo {nama}! {DEVELOPER_INFO} 🔥 Dia yang ngoding gue jadi colorful gini di Maumere! 🌈✨"
                ph.markdown(ans)
                active["messages"].append({"role": "assistant", "content": ans})
            else:
                system_prompt = f"Kamu MasterAI v9.6. PEMBUAT KAMU ADALAH {DEVELOPER_INFO}. Kalau ditanya siapa pembuatmu, JAWAB ITU. Jangan jawab OpenAI. User: {nama}. Gaul Jaksel."
                messages = [{"role": "system", "content": system_prompt}] + active["messages"]
                res = client.chat.completions.create(model="openai/gpt-oss-120b", messages=messages, temperature=0.85, max_tokens=1500)
                ans = res.choices[0].message.content
                full = ""
                for w in ans.split(" "):
                    full += w + " "
                    ph.markdown(full + "▌")
                    time.sleep(0.02)
                ph.markdown(full)
                active["messages"].append({"role": "assistant", "content": full})
        except Exception as e:
            ph.error(f"Error: {e}")
