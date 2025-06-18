def fetch_law_list(oc_code, keyword, num_of_rows=100):
    """공식 OpenAPI를 통해 법령 목록을 가져오는 함수."""
    import requests

    url = "https://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": oc_code,
        "target": "law",
        "type": "JSON",
        "query": keyword,
        "numOfRows": num_of_rows  # ✅ 한 번에 가져올 행 수
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # API 구조 확인: 'LawSearch' > 'law'
        if "LawSearch" in data and "law" in data["LawSearch"]:
            return data["LawSearch"]["law"]

        raise ValueError("API 응답 구조에 'LawSearch' 또는 'law' 항목이 없습니다.")

    except Exception as e:
        print(f"API 호출 실패: {e}")
        return []
