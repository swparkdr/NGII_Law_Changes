import requests
import xml.etree.ElementTree as ET

def fetch_law_versions(oc_code, law_id):
    try:
        url = "https://www.law.go.kr/DRF/lawSearchList.do"
        params = {
            "OC": oc_code,
            "target": "law",
            "id": law_id,
            "type": "JSON",
        }
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        return data["LawSearchList"]["law"]
    except Exception as e:
        print(f"API 버전 목록 호출 실패: {e}")
        return []

def fetch_law_detail(oc_code: str, mst: str):
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
    try:
        root = ET.fromstring(xml_string)
        texts = []
        for article in root.iter("조문내용"):
            if article.text:
                texts.append(article.text.strip())
        return "\n".join(texts)
    except Exception as e:
        return f"XML 파싱 실패: {e}"
