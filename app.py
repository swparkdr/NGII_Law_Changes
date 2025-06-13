import streamlit as st
from law_crawler import load_law_changes
from matcher import load_internal_docs, match_law_to_docs
import pandas as pd

# Load data
law_changes = load_law_changes()
internal_docs = load_internal_docs()

# Get list of departments from CSV
departments = internal_docs['소속과'].dropna().unique().tolist()

st.set_page_config(page_title="법령 변경 반영 시스템", layout="wide")
st.title("📜 국토지리정보원 법령 변경 매핑 시스템")

# 부서 선택
selected_dept = st.selectbox("📂 부서를 선택하세요", departments)

st.markdown("---")

# 필터된 내부 문서
filtered_docs = internal_docs[internal_docs['소속과'] == selected_dept]

# 각 법령 변경사항에 대해 해당 부서 관련 문서만 매핑
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
