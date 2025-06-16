
import requests
import json

def fetch_laws_from_api(api_key, save_path):
    """Call 국가법령정보센터 API and save result as JSON."""
    try:
        url = f"https://www.law.go.kr/DRF/lawService.do?OC={api_key}&target=law&type=JSON"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # 구조에 따라 정제 필요. 일단 저장
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        return False
    except Exception as e:
        print(f"API fetch error: {e}")
        return False
