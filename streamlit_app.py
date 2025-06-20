import streamlit as st
from modules.law_api_fetcher import fetch_law_versions, fetch_law_detail, extract_plaintext_from_xml
from modules.utils import highlight_differences

st.title("국가법령 변경 비교 시스템")

oc_code = st.text_input("기관코드 (OC)", value="lhs0623")
law_id = st.text_input("법령 ID 입력", value="010914")  # 예: 공간정보산업 진흥법

if st.button("법령 버전 불러오기"):
    versions = fetch_law_versions(oc_code, law_id)
    if not versions or len(versions) < 2:
        st.warning("최신과 이전 버전을 비교할 수 없습니다.")
    else:
        latest = versions[0]
        previous = versions[1]

        st.subheader("📜 비교 대상")
        st.write(f"📅 최신 버전 시행일자: {latest['시행일자']}")
        st.write(f"📅 이전 버전 시행일자: {previous['시행일자']}")

        xml_latest = fetch_law_detail(oc_code, latest["법령일련번호"])
        xml_previous = fetch_law_detail(oc_code, previous["법령일련번호"])

        text_latest = extract_plaintext_from_xml(xml_latest)
        text_previous = extract_plaintext_from_xml(xml_previous)

        if text_latest.strip() == text_previous.strip():
            st.success("✅ 변경 사항 없음")
        else:
            st.subheader("🔍 변경 비교 결과")
            diff = highlight_differences(text_previous, text_latest)
            st.markdown(diff, unsafe_allow_html=True)
