import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

import streamlit as st
import json
import os
from law_api_fetcher import fetch_law_list, fetch_law_detail
from law_compare import compare_laws
from utils import load_json_file, highlight_differences

st.set_page_config(page_title="법령 변경 비교 시스템", layout="wide")
st.title("📘 법령 자동 조회 및 변경 비교 시스템")

st.sidebar.header("🔍 법령 검색 및 비교")
oc = st.sidebar.text_input("OC 코드 입력", value="lhs0623")
keyword = st.sidebar.text_input("검색 키워드", value="공간정보")

if st.sidebar.button("🔎 검색 실행"):
    with st.spinner("법령 목록을 불러오는 중..."):
        try:
            law_data = fetch_law_list(keyword, oc)
            laws = law_data["LawSearch"]["law"]
            st.session_state["law_list"] = laws
            st.success(f"{len(laws)}건의 결과가 검색되었습니다.")
        except Exception as e:
            st.error(f"API 호출 실패: {e}")

if "law_list" in st.session_state:
    laws = st.session_state["law_list"]
    options = {f"[{law['시행일자']}] {law['법령명한글']}": law for law in laws}
    law_select_1 = st.selectbox("📄 기존 법령 선택", list(options.keys()), key="law1")
    law_select_2 = st.selectbox("🆕 변경된 법령 선택", list(options.keys()), key="law2")

    law1 = options[law_select_1]
    law2 = options[law_select_2]

    if st.button("⚖️ 변경 비교 실행"):
        with st.spinner("법령 전문 불러오는 중..."):
            try:
                law_text_1 = fetch_law_detail(law1["법령일련번호"], oc, format="HTML")
                law_text_2 = fetch_law_detail(law2["법령일련번호"], oc, format="HTML")

                added, removed, summary = compare_laws(law_text_1, law_text_2)

                st.subheader("📌 변경 요약")
                st.info(summary)

                st.subheader("🟥 삭제된 조문")
                st.code("\n".join(removed), language="html")

                st.subheader("🟩 추가된 조문")
                st.code("\n".join(added), language="html")

                st.subheader("📊 전체 비교 (기존 vs 변경)")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 기존 법령")
                    st.code(law_text_1, language="html")
                with col2:
                    st.markdown("#### 변경된 법령")
                    st.code(law_text_2, language="html")

            except Exception as e:
                st.error(f"법령 비교 중 오류 발생: {e}")
