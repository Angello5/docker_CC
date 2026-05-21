import streamlit as st
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

st.title("Subida de archivos")

uploaded_file = st.file_uploader("Selecciona un archivo")

if uploaded_file is not None:
    file_path = UPLOAD_DIR / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Archivo guardado en: {file_path}")