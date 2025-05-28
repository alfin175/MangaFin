
import streamlit as st
import requests

st.set_page_config(page_title="MangaDex Streamlit", layout="wide")
st.title("📚 Cari Manga dari MangaDex")

query = st.text_input("Masukkan judul manga:")
lang = st.selectbox("Pilih bahasa chapter:", ["id", "en"], index=0)

if query:
    with st.spinner("Mencari manga..."):
        res = requests.get(
            "https://api.mangadex.org/manga",
            params={"title": query, "limit": 10}
        )
        data = res.json()
        results = data.get("data", [])

        if results:
            for manga in results:
                title = manga["attributes"]["title"].get("en", "Tanpa Judul")
                manga_id = manga["id"]
                st.subheader(title)

                # Cover
                cover_res = requests.get(f"https://api.mangadex.org/cover?manga[]=" + manga_id)
                cover_data = cover_res.json().get("data", [])
                if cover_data:
                    file_name = cover_data[0]["attributes"]["fileName"]
                    cover_url = f"https://uploads.mangadex.org/covers/{manga_id}/{file_name}.256.jpg"
                    st.image(cover_url, width=150)

                # Link MangaDex
                st.markdown(f"[🔗 Buka di MangaDex](https://mangadex.org/title/{manga_id})", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.warning("Manga tidak ditemukan.")
