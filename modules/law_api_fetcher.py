def fetch_law_list(oc_code, keyword, num_of_rows=100):
    """
    공식 OpenAPI를 통해 법령 목록을 가져오는 함수.
    API 호출 실패 시 빈 리스트를 반환합니다.
    """
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
        response = requests.get(url, params=params, timeout=10) # ✅ 타임아웃 추가
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생

        data = response.json()

        # API 응답 구조 확인: 'LawSearch' > 'law'
        if "LawSearch" in data and "law" in data["LawSearch"]:
            return data["LawSearch"]["law"]
        else:
            # 예상치 못한 API 응답 구조일 경우
            print(f"API 응답 구조 오류: 'LawSearch' 또는 'law' 항목이 없습니다. 전체 응답: {data}")
            return []

    except requests.exceptions.HTTPError as http_err:
        # HTTP 오류 (예: 404 Not Found, 500 Internal Server Error)
        print(f"HTTP 오류 발생: {http_err} (상태 코드: {http_err.response.status_code})")
        return []
    except requests.exceptions.ConnectionError as conn_err:
        # 연결 오류 (예: 네트워크 문제, 잘못된 URL)
        print(f"연결 오류 발생: {conn_err}. URL 또는 네트워크 연결을 확인하세요.")
        return []
    except requests.exceptions.Timeout as timeout_err:
        # 요청 시간 초과 오류
        print(f"요청 시간 초과 오류 발생: {timeout_err}")
        return []
    except requests.exceptions.RequestException as req_err:
        # requests 라이브러리 관련 기타 오류
        print(f"API 요청 중 알 수 없는 오류 발생: {req_err}")
        return []
    except ValueError as json_err:
        # JSON 디코딩 오류
        print(f"JSON 디코딩 오류 발생: {json_err}. 유효하지 않은 JSON 응답입니다.")
        return []
    except Exception as e:
        # 그 외 모든 예상치 못한 오류
        print(f"예상치 못한 오류 발생: {e}")
        return []
