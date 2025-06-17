import requests

def fetch_law_list(oc_code: str, keyword: str = "", num_of_rows: int = 100):
    """Fetch a list of laws using the public API."""
    url = "https://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": oc_code,
        "target": "law",
        "type": "JSON",
        "numOfRows": num_of_rows,
        "query": keyword
    }
    response = requests.get(url, params=params)

    try:
        data = response.json()
        return data["LawSearch"]["law"] if "LawSearch" in data else []
    except Exception as e:
        print("❌ API 호출 실패:", e)
        print("🔍 응답 내용:", response.text[:300])  # 처음 300자만 확인
        return []

def fetch_law_detail(oc_code: str, mst: str, law_type: str = "HTML"):
    """Fetch full law detail content using the public API."""
    url = "https://www.law.go.kr/DRF/lawService.do"
    params = {
        "OC": oc_code,
        "target": "law",
        "MST": mst,
        "type": law_type
    }
    response = requests.get(url, params=params)
    return response.text if law_type == "HTML" else response.json()
