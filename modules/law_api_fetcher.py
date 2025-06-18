import requests
import streamlit as st

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

def fetch_law_detail(oc_code: str, mst: str, output_type: str = "HTML"):
    """법령 상세 내용을 API로 가져온다."""
    try:
        url = f"https://www.law.go.kr/DRF/lawService.do"
        params = {
            "OC": oc_code,
            "target": "law",
            "MST": mst,
            "type": output_type
        }
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.text
    except Exception as e:
        st.error(f"법령 상세 불러오기 실패: {e}")
        return ""
