import streamlit as st
from law_crawler import load_law_changes
from matcher import load_internal_docs, match_law_to_docs

# Load data
law_changes = load_law_changes()
internal_docs = load_internal_docs()

st.set_page_config(page_title="법령 변경 반영 시스템", layout="wide")
st.title("📜 국토지리정보원 법령 변경 매핑 시스템 (데모)")

for change in law_changes:
    with st.expander(f"🔸 [{change['법령명']}] {change['조문번호']} - {change['제목']}"):
        st.markdown(f"- **개정일**: {change['개정일']}")
        st.markdown(f"- **변경사항**: {change['변경사항']}")

        matches = match_law_to_docs(change, internal_docs)

        if matches:
            st.success("🗂 관련 내부 문서가 매핑되었습니다:")
            for m in matches:
                st.markdown(f"- `{m['문서명']}` → **{m['항목명']}** *(키워드: {m['매칭키워드']})*")
        else:
            st.warning("⚠️ 매핑되는 내부 문서가 없습니다.")
