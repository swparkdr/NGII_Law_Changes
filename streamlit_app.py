import streamlit as st
import requests
import json
import difflib

# 기본 설정
st.set_page_config(page_title="법령 변경 비교 시스템", layout="wide")
st.title("📚 국토지리정보원 법령 변경 비교 시스템")

# --- 법령 목록 API 불러오기 ---
def fetch_law_list(oc_code: str, keyword: str, num_rows: int = 100):
    """API를 통해 법령 목록을 받아온다."""
    try:
        url = "https://www.law.go.kr/DRF/lawSearch.do"
        params = {
            "OC": oc_code,
            "target": "law",
            "query": keyword,
            "type": "JSON",
            "numOfRows": num_rows,
        }
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        return data["LawSearch"]["law"]
    except Exception as e:
        st.error(f"API 호출 실패: {e}")
        return []

# --- 차이 비교 함수 ---
def compare_texts(old_text: str, new_text: str):
    diff = difflib.ndiff(old_text.splitlines(), new_text.splitlines())
    return list(diff)

def render_diff_as_text(diff):
    result = ""
    for line in diff:
        if line.startswith("- "):
            result += f"❌ 삭제: {line[2:]}\n"
        elif line.startswith("+ "):
            result += f"✅ 추가: {line[2:]}\n"
        else:
            result += f"    {line[2:]}\n"
    return result

# --- 기능 선택 ---
tab1, tab2, tab3 = st.tabs(["1️⃣ 법령 검색", "2️⃣ 법령 변경 비교", "3️⃣ 요약 출력"])

with tab1:
    st.subheader("🔍 법령 검색")
    oc_code = st.text_input("기관 코드 (OC)", value="lhs0623")
    keyword = st.text_input("검색어 (예: 공간정보)", value="공간정보")
    if st.button("📥 법령 목록 불러오기"):
        results = fetch_law_list(oc_code, keyword)
        if results:
            for law in results:
                st.markdown(f"**{law['법령명한글']}**")
                st.caption(f"- 시행일자: {law['시행일자']}, 공포일자: {law['공포일자']}")
                st.markdown(
                    f"[법령 상세 보기](https://www.law.go.kr{law['법령상세링크']})", unsafe_allow_html=True
                )

with tab2:
    st.subheader("📄 법령 비교")
    uploaded_old = st.file_uploader("이전 법령 TXT 업로드", type=["txt"], key="old")
    uploaded_new = st.file_uploader("변경된 법령 TXT 업로드", type=["txt"], key="new")

    if uploaded_old and uploaded_new:
        old_text = uploaded_old.read().decode("utf-8")
        new_text = uploaded_new.read().decode("utf-8")
        diff = compare_texts(old_text, new_text)
        st.code(render_diff_as_text(diff), language="text")

with tab3:
    st.subheader("🧠 요약 보기")
    st.info("이 기능은 향후 자연어 요약 기능이 추가될 예정입니다.")
