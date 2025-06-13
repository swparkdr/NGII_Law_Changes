import streamlit as st
from law_crawler import load_law_changes
from matcher import load_internal_docs, match_law_to_docs
import pandas as pd

# 고정된 부서 목록
departments = [
    "기획정책과", "운영지원과", "위치기준과", "지리정보과",
    "스마트공간정보과", "국토조사과", "위성센터"
]

# 초기 상태 설정
if "selected_dept" not in st.session_state:
    st.session_state.selected_dept = None

st.set_page_config(page_title="법령 변경 반영 시스템", layout="wide")
st.title("📜 국토지리정보원 법령 변경 매핑 시스템")

# STEP 1: 부서 선택
if st.session_state.selected_dept is None:
    st.subheader("1️⃣ 과(부서)를 선택하세요")

    cols = st.columns(3)
    for idx, dept in enumerate(departments):
        with cols[idx % 3]:
            if st.button(f"📁 {dept}"):
                st.session_state.selected_dept = dept
    st.stop()

# STEP 2: 선택된 부서의 매핑 결과
selected_dept = st.session_state.selected_dept
st.subheader(f"📂 {selected_dept} - 관련 법령 매핑 결과")

# 돌아가기 버튼
if st.button("⬅️ 부서 선택으로 돌아가기"):
    st.session_state.selected_dept = None
    st.experimental_rerun()

# 데이터 로딩
law_changes = load_law_changes()
internal_docs = load_internal_docs()
filtered_docs = internal_docs[internal_docs['소속과'] == selected_dept]

# 법령 변경사항 → 해당 부서 관련 문서만 매핑
for change in law_changes:
    matches = match_law_to_docs(change, filtered_docs)

    with st.expander(f"🔸 [{change['법령명']}] {change['조문번호']} - {change['제목']}"):
        st.markdown(f"- **개정일**: {change['개정일']}")
        st.markdown(f"- **변경사항**: {change['변경사항']}")

        if matches:
            st.success("🗂 관련 내부 문서가 매핑되었습니다:")
            for m in matches:
                st.markdown(f"- `{m['문서명']}` → **{m['항목명']}** *(키워드: {m['매칭키워드']})*")
        else:
            st.info("이 부서의 관련 문서에는 매핑된 항목이 없습니다.")
