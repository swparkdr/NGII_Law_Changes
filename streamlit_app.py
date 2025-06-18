import streamlit as st
from modules.law_api_fetcher import fetch_law_list, fetch_law_detail, extract_plaintext_from_xml
from modules.utils import highlight_differences

st.title("국가법령 변경 비교 시스템")

oc_code = st.text_input("기관코드 (OC)", value="lhs0623")
keyword = st.text_input("법령 검색어", value="공간정보")

if st.button("법령 검색"):
    laws = fetch_law_list(oc_code, keyword)
    if laws:
        st.session_state["laws"] = laws
    else:
        st.warning("법령 정보를 가져오지 못했습니다.")

if "laws" in st.session_state:
    law_titles = [law["법령명한글"] for law in st.session_state["laws"]]
    selected = st.selectbox("비교할 법령 선택", law_titles)
    selected_law = st.session_state["laws"][law_titles.index(selected)]

    st.write(f"선택된 법령: **{selected_law['법령명한글']}**")
    mst = selected_law["법령일련번호"]

    if st.button("법령 내용 비교"):
        try:
            xml_text = fetch_law_detail(oc_code, mst)
            law_text = extract_plaintext_from_xml(xml_text)
            st.text_area("법령 본문 (요약)", value=law_text[:3000], height=400)
        except Exception as e:
            st.error(f"비교 실패: {e}")