import requests
import xml.etree.ElementTree as ET

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
        print(f"API 호출 실패: {e}")
        return []

def fetch_law_detail(oc_code: str, mst: str):
    """법령 조문을 XML 형태로 받아오기"""
    try:
        url = "https://www.law.go.kr/DRF/lawService.do"
        params = {
            "OC": oc_code,
            "target": "law",
            "MST": mst,
            "type": "XML",
        }
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return ""

def extract_plaintext_from_xml(xml_string):
    """법령 XML에서 조문 본문 텍스트 추출"""
    try:
        root = ET.fromstring(xml_string)
        texts = []
        for article in root.iter("조문내용"):
            if article.text:
                texts.append(article.text.strip())
        return "\n".join(texts)
    except Exception as e:
        return f"XML 파싱 실패: {e}"
