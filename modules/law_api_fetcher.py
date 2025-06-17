import requests
import json

def fetch_law_list(keyword: str, oc: str, rows: int = 100, page: int = 1) -> dict:
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": oc,
        "target": "law",
        "type": "JSON",
        "query": keyword,
        "display": rows,
        "page": page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API 요청 실패: 상태 코드 {response.status_code}")

def fetch_law_detail(mst: str, oc: str, format: str = "JSON") -> dict:
    url = "http://www.law.go.kr/DRF/lawService.do"
    params = {
        "OC": oc,
        "target": "law",
        "MST": mst,
        "type": format
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        if format == "JSON":
            return response.json()
        else:
            return response.text
    else:
        raise Exception(f"법령 상세 조회 실패: 상태 코드 {response.status_code}")
