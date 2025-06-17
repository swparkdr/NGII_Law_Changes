import requests

def fetch_law_list(oc_code, keyword):
    """
    Fetch a list of laws from the law.go.kr Open API based on keyword.

    Parameters:
    - oc_code (str): API key (기관코드)
    - keyword (str): 검색 키워드

    Returns:
    - list of laws (list of dict) or empty list if error occurs
    """
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": oc_code,
        "target": "law",
        "type": "JSON",
        "query": keyword
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 예외 처리: 전체 구조 확인
        if isinstance(data, dict) and "LawSearch" in data:
            law_search = data["LawSearch"]
            if isinstance(law_search, dict):
                return law_search.get("law", [])
            else:
                print("⚠️ 'LawSearch'는 dict가 아님. 타입:", type(law_search))
        else:
            print("⚠️ 예상된 'LawSearch' 키 없음. 전체 응답 구조:", type(data))

    except requests.exceptions.RequestException as req_err:
        print("❌ 요청 오류:", req_err)
    except ValueError as val_err:
        print("❌ JSON 파싱 오류:", val_err)
        print("🔍 응답 원문:", response.text[:300])
    except Exception as e:
        print("❌ 기타 오류:", e)

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
