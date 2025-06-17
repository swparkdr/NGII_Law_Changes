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

        # Debugging
        print("✅ 응답 타입:", type(data))
        print("📄 응답 예시:", str(data)[:300])

        # Check and return law list if structure matches
        if isinstance(data, dict) and "LawSearch" in data:
            return data["LawSearch"].get("law", [])
        else:
            print("⚠️ 알 수 없는 응답 형식입니다.")
            return []

    except requests.exceptions.RequestException as req_err:
        print("❌ 요청 오류:", req_err)
        return []
    except ValueError as val_err:
        print("❌ JSON 파싱 오류:", val_err)
        print("🔍 응답 원문:", response.text[:300])
        return []
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
