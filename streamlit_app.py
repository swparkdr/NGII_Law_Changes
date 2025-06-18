import streamlit as st
import os
import sys

# ✅ 강제 경로 설정 (Streamlit에서 모듈 인식 문제 방지)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ✅ modules에서 가져오기
from modules.law_api_fetcher import fetch_law_list, fetch_law_detail
from modules.comparator import compare_laws

st.set_page_config(page_title="국토지리정보원 법령 변경 비교 시스템", layout="wide")
st.title("📘 국토지리정보원 법령 변경 비교 시스템")

# 🔹 Step 1: 법령 목록 불러오기
st.header("1️⃣ 법령 검색 및 불러오기")
keyword = st.text_input("키워드를 입력하세요 (예: 공간정보)", value="공간정보")

if st.button("법령 목록 가져오기"):
    with st.spinner("법령 정보를 불러오는 중입니다..."):
        law_list = fetch_law_list(keyword)
        if law_list:
            st.session_state.laws = law_list
            st.success(f"총 {len(law_list)}건의 법령이 검색되었습니다.")
        else:
            st.error("❌ 법령을 불러오는 데 실패했습니다.")

# 🔹 Step 2: 법령 상세 비교
if "laws" in st.session_state:
    st.header("2️⃣ 법령 상세 비교")

    law_titles = [f"{law['법령명한글']} ({law['시행일자']})" for law in st.session_state.laws]
    selected_indices = st.multiselect("비교할 법령 2개를 선택하세요:", options=list(range(len(law_titles))),
                                      format_func=lambda i: law_titles[i])

    if len(selected_indices) == 2:
        law1 = st.session_state.laws[selected_indices[0]]
        law2 = st.session_state.laws[selected_indices[1]]

        with st.spinner("법령 전문을 불러오는 중입니다..."):
            content1 = fetch_law_detail(law1)
            content2 = fetch_law_detail(law2)

        if content1 and content2:
            st.subheader("비교 결과 (문단 단위 분석)")
            differences = compare_laws(content1, content2)
            for block in differences:
                st.markdown(block, unsafe_allow_html=True)
        else:
            st.error("❌ 두 법령 전문을 모두 불러오는 데 실패했습니다.")

# 🔹 Footer
st.markdown("---")
st.caption("Made by NGII. Powered by 국가법령정보센터 OpenAPI.")
