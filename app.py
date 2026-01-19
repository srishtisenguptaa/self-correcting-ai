import streamlit as st
import requests

st.title("Self-Correcting Data Validation Agent")

text = st.text_area("Paste messy data")

if st.button("Process"):
    res = requests.post(
        "http://localhost:8000/process",
        json={"text": text}
    )
    st.json(res.json())
