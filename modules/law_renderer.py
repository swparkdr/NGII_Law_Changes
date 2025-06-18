import streamlit as st
from bs4 import BeautifulSoup

def render_law_text_as_paragraphs(html_text: str):
    """HTML 법령 텍스트를 문단별로 나눠 보기 쉽게 출력"""
    soup = BeautifulSoup(html_text, "html.parser")
    paragraphs = soup.get_text(separator="\n").split("\n")
    for p in paragraphs:
        if p.strip():
            st.markdown(f"📝 {p.strip()}")
