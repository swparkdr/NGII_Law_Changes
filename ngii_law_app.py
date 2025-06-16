
# ngii_law_app.py

import streamlit as st
import json
import os
from datetime import datetime
from modules.api import fetch_laws_from_api
from modules.compare import compare_laws
from modules.search import search_laws

# --- 기본 설정 ---
st.set_page_config(page_title="NGII 법령 도우미", layout="wide")

# --- 경로 설정 ---
LAWS_PATH = "laws.json"
OLD_LAWS_PATH = "laws_old.json"

# --- API Key 입력 ---
st.sidebar.header("🔐 API 키 입력")
api_key = st.sidebar.text_input("국가법령정보센터 API 키", type="password")

# --- 마지막 갱신일 추정 ---
def get_last_updated():
    if os.path.exists(LAWS_PATH):
        ts = os.path.getmtime(LAWS_PATH)
        return datetime.fromtimestamp(ts)
    return None

# --- 0단계: 최신 법령 갱신 ---
st.title("📘 국토지리정보원 법령 도우미")
st.markdown("""
**이 앱은 NGII 관련 법령을 검색하고, 변경사항을 비교하고, 자동 갱신할 수 있는 도구입니다.**
""")

with st.expander("🌀 법령 갱신 (API 연동)"):
    last_updated = get_last_updated()
    if last_updated:
        st.markdown(f"- 마지막 갱신일: `{last_updated.strftime('%Y-%m-%d %H:%M:%S')}`")
    else:
        st.markdown("- 아직 데이터가 없습니다.")

    if st.button("🔁 법령 갱신하기"):
        if not api_key:
            st.warning("API 키를 입력해주세요.")
        else:
            if os.path.exists(LAWS_PATH):
                os.replace(LAWS_PATH, OLD_LAWS_PATH)
            result = fetch_laws_from_api(api_key, LAWS_PATH)
            if result:
                st.success("법령이 성공적으로 갱신되었습니다!")
            else:
                st.error("API 호출 실패 또는 형식 오류.")

# --- 1단계: 키워드 검색 ---
st.header("🔍 법령 검색")
if os.path.exists(LAWS_PATH):
    laws_data = json.load(open(LAWS_PATH, encoding="utf-8"))
    keyword = st.text_input("궁금한 키워드를 입력하세요:")
    if keyword:
        results = search_laws(laws_data, keyword)
        if results:
            for clause in results:
                st.markdown(f"**📌 {clause['조문명']}**")
                st.write(clause['조문내용'])
        else:
            st.info("일치하는 조문이 없습니다.")
else:
    st.warning("법령 데이터를 먼저 갱신하거나 업로드해주세요.")

# --- 2단계: 법령 변경 비교 ---
st.header("📎 변경된 법령 비교")
if os.path.exists(LAWS_PATH) and os.path.exists(OLD_LAWS_PATH):
    diff = compare_laws(OLD_LAWS_PATH, LAWS_PATH)
    if diff:
        for d in diff:
            st.markdown(f"### 🔧 {d['조문명']}")
            st.markdown(
                f"<pre><span style='color:red'>- {d['이전']}</span>\n<span style='color:green'>+ {d['현재']}</span></pre>",
                unsafe_allow_html=True
            )
    else:
        st.success("변경된 조항이 없습니다.")
else:
    st.info("변경 비교를 위해선 과거/현재 법령 파일이 모두 필요합니다.")
