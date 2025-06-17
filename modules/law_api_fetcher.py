import streamlit as st
import json
import os
from modules.utils import load_json_file, highlight_differences
from modules.law_compare import compare_laws

def fetch_law_list_from_api(api_key: str, keyword: str, rows: int = 10):
    import requests
    from urllib.parse import urlencode

    base_url = "https://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": api_key,
        "target": "law",
        "type": "JSON",
        "section": "lawNm",
        "query": keyword,
        "numOfRows": rows
    }
    response = requests.get(f"{base_url}?{urlencode(params)}")

    if response.status_code == 200:
        data = response.json()
        return data.get("LawSearch", {}).get("law", [])
    else:
        return []

st.set_page_config(page_title="NGII 법령 비교 시스템", layout="wide")

st.title("📚 국토지리정보원 법령 비교 시스템")
st.markdown("국토지리정보원에서 관리하는 공간정보 관련 법령을 쉽게 검색하고 비교할 수 있습니다.")

st.sidebar.header("📂 데이터 업로드 / 불러오기")

# 파일 업로드
uploaded_old = st.sidebar.file_uploader("📌 기존 법령 JSON", type="json", key="old")
uploaded_new = st.sidebar.file_uploader("📌 변경된 법령 JSON", type="json", key="new")

# 법령 목록 API로 가져오기 (테스트용)
if st.sidebar.button("🔄 법령 목록 API 불러오기"):
    laws = fetch_law_list_from_api("lhs0623", "공간정보")  # OC, 키워드
    st.sidebar.success(f"{len(laws)}개의 법령 불러옴")
    for law in laws:
        st.sidebar.markdown(f"- {law['법령명한글']}")

# 전체 비교 실행
if uploaded_old and uploaded_new:
    old_data = json.load(uploaded_old)
    new_data = json.load(uploaded_new)

    st.subheader("🔍 1. 키워드 검색")
    keyword = st.text_input("궁금한 키워드를 입력하세요:", "")

    if keyword:
        st.markdown("#### 📌 검색 결과")
        for o in old_data["조문"]:
            if keyword in o:
                st.markdown(f"🔴 `{o.strip()}`")
        for n in new_data["조문"]:
            if keyword in n:
                st.markdown(f"🟢 `{n.strip()}`")

    st.divider()

    st.subheader("📝 2. 전체 조문 비교")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔴 기존 법령")
        for i, clause in enumerate(old_data["조문"], 1):
            st.markdown(f"**제{i}조**")
            st.markdown(clause.strip())

    with col2:
        st.markdown("### 🟢 변경된 법령")
        for i, clause in enumerate(new_data["조문"], 1):
            st.markdown(f"**제{i}조**")
            st.markdown(clause.strip())

    st.divider()

    st.subheader("🧐 3. 변경 요약")
    added, removed, modified = compare_laws(old_data["조문"], new_data["조문"])

    st.markdown(f"- ➕ 추가된 조문: {len(added)}개")
    for line in added:
        st.markdown(f"<span style='color:green'>+ {line}</span>", unsafe_allow_html=True)

    st.markdown(f"- ❌ 삭제된 조문: {len(removed)}개")
    for line in removed:
        st.markdown(f"<span style='color:red'>- {line}</span>", unsafe_allow_html=True)

    st.markdown(f"- ✏️ 수정된 조문: {len(modified)}개")
    for old, new in modified:
        st.markdown("🔸 수정 전:")
        st.markdown(f"<span style='color:red'>{old}</span>", unsafe_allow_html=True)
        st.markdown("🔸 수정 후:")
        st.markdown(f"<span style='color:green'>{new}</span>", unsafe_allow_html=True)

else:
    st.info("좌측 사이드바에서 기존/변경 JSON 법령 파일을 업로드해 주세요.")
