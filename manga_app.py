
import streamlit as st
import requests

st.set_page_config(page_title="MangaFin", layout="wide", initial_sidebar_state="expanded")

if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ---------- Sidebar ----------
st.sidebar.title("🔍 Filter Manga")
query = st.sidebar.text_input("Judul Manga")
lang = st.sidebar.selectbox("Bahasa Chapter", ["id", "en", "jp", "es", "fr", "vi"], index=0)
genre_list = [
    "Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror",
    "Mystery", "Romance", "Sci-Fi", "Slice of Life", "Sports", "Supernatural"
]
genre = st.sidebar.selectbox("Genre", ["Semua"] + genre_list)

# ---------- Tabs ----------
tab1, tab2 = st.tabs(["📚 Hasil Pencarian", "⭐ Favorit Saya"])

def get_genres():
    genre_map = {
        "Action": "391b0423-d847-456f-aff0-8b0cfc03066b",
        "Adventure": "87cc87cd-a395-47af-b27a-93258283bbc6",
        "Comedy": "4d32cc48-9f00-4cca-9b5a-a839f0764984",
        "Drama": "f8f62932-27da-4fe4-8ee1-6779a8c5edba",
        "Fantasy": "cdc58593-87dd-415e-bbc0-2ec27bf404cc",
        "Horror": "cdad7e68-1419-41dd-bdce-27753074a640",
        "Mystery": "ee968100-4191-4968-93d3-f82d72be7e46",
        "Romance": "423e2eae-a7a2-4a8b-ac03-a8351462d71d",
        "Sci-Fi": "256c8bd9-4904-4360-bf4f-508a76d67183",
        "Slice of Life": "ba0dc0b1-06c8-4a2a-b6e4-5cba4ced3c09",
        "Sports": "799c202e-7daa-44eb-9cf7-8a3c0441531e",
        "Supernatural": "0bc90acb-ccc1-4c6e-b9a2-5c3a8c9e6c1e"
    }
    return genre_map

def fetch_manga(title, language, genre_tag=None):
    params = {
        "title": title,
        "limit": 20,
        "availableTranslatedLanguage[]": language,
        "includes[]": ["cover_art"]
    }
    if genre_tag:
        params["includedTags[]"] = genre_tag
    res = requests.get("https://api.mangadex.org/manga", params=params)
    return res.json().get("data", [])

def get_cover_url(manga_id, file_name):
    return f"https://uploads.mangadex.org/covers/{manga_id}/{file_name}.256.jpg"

# ---------- Tab 1: Search Results ----------
with tab1:
    if query:
        with st.spinner("🔎 Mencari manga..."):
            genre_tag = get_genres().get(genre) if genre != "Semua" else None
            results = fetch_manga(query, lang, genre_tag)
            if results:
                for manga in results:
                    attr = manga["attributes"]
                    title = attr["title"].get("en") or list(attr["title"].values())[0]
                    manga_id = manga["id"]
                    link = f"https://mangadex.org/title/{manga_id}"

                    cover_rel = manga["relationships"]
                    cover_file = None
                    for rel in cover_rel:
                        if rel["type"] == "cover_art":
                            cover_file = rel["attributes"]["fileName"]
                    cover_url = get_cover_url(manga_id, cover_file) if cover_file else ""

                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if cover_url:
                            st.image(cover_url, use_column_width=True)
                    with col2:
                        st.markdown(f"### [{title}]({link})")
                        st.markdown(f"**ID:** {manga_id}")
                        if st.button(f"⭐ Simpan ke Favorit", key=manga_id):
                            if manga_id not in st.session_state.favorites:
                                st.session_state.favorites.append({
                                    "id": manga_id,
                                    "title": title,
                                    "cover": cover_url,
                                    "link": link
                                })
                                st.success(f"✅ Disimpan: {title}")
                    st.markdown("---")
            else:
                st.warning("Tidak ditemukan manga dengan kriteria tersebut.")
    else:
        st.info("Masukkan judul manga di sidebar untuk mulai pencarian.")

# ---------- Tab 2: Favorit ----------
with tab2:
    st.subheader("⭐ Daftar Manga Favorit")
    if not st.session_state.favorites:
        st.info("Belum ada favorit yang disimpan.")
    else:
        for fav in st.session_state.favorites:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(fav["cover"], use_column_width=True)
            with col2:
                st.markdown(f"### [{fav['title']}]({fav['link']})")
                if st.button("🗑️ Hapus dari Favorit", key="del_" + fav["id"]):
                    st.session_state.favorites = [f for f in st.session_state.favorites if f["id"] != fav["id"]]
                    st.experimental_rerun()
