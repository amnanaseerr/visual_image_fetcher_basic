import streamlit as st
import requests
import os
import zipfile
from io import BytesIO

# --- 🔹 Your Google API details ---
API_KEY = "AIzaSyANyHulmjndM4nZlF06i8OoyzeKChWfYOA"
CX = "c3b04135aa8bf432d"

# --- Streamlit page config ---
st.set_page_config(page_title="Smart Image Fetcher", layout="wide")
st.title("🔍 Smart Image Fetcher")
st.markdown("Fetch real images using your own API.")

# --- Inputs ---
query = st.text_input("Enter search keyword:")
num_images = st.slider("Number of images to fetch", 5, 50, 10)
download = st.checkbox("Do you want to download these images?")

# --- Search Button ---
if st.button("Search Images"):
    if not query:
        st.warning("Please enter a keyword first.")
    else:
        st.info("Fetching images... please wait ⏳")

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "cx": CX,
            "key": API_KEY,
            "searchType": "image",
            "num": num_images
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])

            if items:
                st.success(f"✅ {len(items)} images fetched for '{query}'!")
                cols = st.columns(3)
                image_urls = []

                for idx, item in enumerate(items):
                    img_url = item["link"]
                    image_urls.append(img_url)
                    with cols[idx % 3]:
                        st.image(img_url, caption=f"Image {idx+1}", use_container_width=True)

                # --- Optional Download Section ---
                if download:
                    os.makedirs("google_downloads", exist_ok=True)
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w") as zipf:
                        for i, url in enumerate(image_urls):
                            try:
                                img_data = requests.get(url).content
                                zipf.writestr(f"{query}_{i+1}.jpg", img_data)
                            except:
                                pass
                    zip_buffer.seek(0)
                    st.download_button(
                        label="⬇️ Download all images as ZIP",
                        data=zip_buffer,
                        file_name=f"{query}_images.zip",
                        mime="application/zip"
                    )
                    st.success("All images saved successfully!")
            else:
                st.error("No images found! Try another keyword.")
        else:
            st.error(f"⚠️ Error fetching images: {response.status_code}")
            st.write(response.text)
