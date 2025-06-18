import streamlit as st
from modules.law_api_fetcher import fetch_law_list, fetch_law_detail
from modules.law_diff_utils import compare_laws
from modules.law_renderer import render_law_text_as_paragraphs

st.set_page_config(page_title="국토지리정보원 법령 변경 비교 시스템", layout="wide")

st.title("📚 NGII 법령 변경 비교 시스템")

oc_code = st.text_input("기관코드(OC)", value="lhs0623")
keyword = st.text_input("검색 키워드", value="공간정보")

if st.button("🔍 법령 검색"):
    law_list = fetch_law_list(oc_code, keyword)
    if law_list:
        selected = st.selectbox("법령 선택", options=law_list, format_func=lambda x: x["법령명한글"])
        mst = selected["법령일련번호"]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("기존 법령")
            old_text = fetch_law_detail(oc_code, mst)
            render_law_text_as_paragraphs(old_text)
        with col2:
            st.subheader("변경된 법령")
            new_text = fetch_law_detail(oc_code, mst)
            render_law_text_as_paragraphs(new_text)

        st.subheader("🔁 변경 비교 결과")
        html_diff = compare_laws(old_text, new_text)
        st.components.v1.html(html_diff, height=600, scrolling=True)
