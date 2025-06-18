import streamlit as st
import requests
from difflib import SequenceMatcher

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

# --- 법령 상세 HTML 받아오기 ---
def fetch_law_detail(oc_code: str, mst: str):
    """API를 통해 법령의 HTML 원문을 받아온다."""
    try:
        url = "https://www.law.go.kr/DRF/lawService.do"
        params = {
            "OC": oc_code,
            "target": "law",
            "MST": mst,
            "type": "HTML",
        }
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.text
    except Exception as e:
        st.error(f"API 호출 실패: {e}")
        return ""

# --- 자연어 기반 변경 비교 함수 ---
def highlight_differences_readable(old_text, new_text):
    """Show differences between two texts in a human-readable, color-coded way."""
    s = SequenceMatcher(None, old_text.splitlines(), new_text.splitlines())
    result = []

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            result.extend([f"<div>{line}</div>" for line in old_text.splitlines()[i1:i2]])
        elif tag == 'replace':
            result.extend([f"<div style='color:red'>- {line}</div>" for line in old_text.splitlines()[i1:i2]])
            result.extend([f"<div style='color:green'>+ {line}</div>" for line in new_text.splitlines()[j1:j2]])
        elif tag == 'delete':
            result.extend([f"<div style='color:red'>- {line}</div>" for line in old_text.splitlines()[i1:i2]])
        elif tag == 'insert':
            result.extend([f"<div style='color:green'>+ {line}</div>" for line in new_text.splitlines()[j1:j2]])

    return "\n".join(result)

# --- Streamlit 앱 시작 ---
st.title("📚 국토지리정보원 법령 변경 비교 시스템")

oc_code = st.text_input("🔑 API 기관 코드 (OC)", value="lhs0623")
keyword = st.text_input("🔍 검색어 입력", value="공간정보")

if st.button("📥 법령 검색"):
    law_list = fetch_law_list(oc_code, keyword)
    if not law_list:
        st.warning("검색 결과가 없습니다.")
    else:
        st.session_state.laws = law_list
        st.success(f"{len(law_list)}건의 법령을 불러왔습니다.")

if "laws" in st.session_state:
    selected = st.selectbox("📑 비교할 법령 선택 (최신 순)", st.session_state.laws, format_func=lambda x: x["법령명한글"])

    if selected:
        mst = selected["법령일련번호"]

        st.subheader("🆚 변경 비교 결과")

        old_text = fetch_law_detail(oc_code, mst)  # 현재는 같은 걸 두 번 부르지만, 향후 이전 버전 받아오도록 확장 가능
        new_text = fetch_law_detail(oc_code, mst)

        diff_html = highlight_differences_readable(old_text, new_text)
        st.markdown(diff_html, unsafe_allow_html=True)
