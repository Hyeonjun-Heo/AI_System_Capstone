import requests
import pandas as pd
import time

API_KEY = "27a49415edf9496fb394"
BASE_URL = f"https://openapi.foodsafetykorea.go.kr/api/27a49415edf9496fb394/COOKRCP01/json"

# ✅ 전체 개수 가져오기
def get_total_count():
    url = f"{BASE_URL}/1/1"
    response = requests.get(url)
    data = response.json()
    total = int(data['COOKRCP01']['total_count'])
    print(f"📦 전체 레시피 개수: {total}")
    return total

# ✅ 단일 요청 함수
def fetch_recipes(start=1, end=100):
    url = f"{BASE_URL}/{start}/{end}"
    response = requests.get(url)
    data = response.json()

    if 'COOKRCP01' not in data:
        print("⚠️ API 오류 발생:", data)
        return []

    rows = data['COOKRCP01']['row']
    return [
        {"레시피명": r["RCP_NM"], "재료": r["RCP_PARTS_DTLS"]}
        for r in rows if r.get("RCP_PARTS_DTLS")
    ]

# ✅ 전체 반복 수집 함수
def fetch_all_recipes(step=100, delay=0.5):
    max_count = get_total_count()
    all_recipes = []
    for start in range(1, max_count + 1, step):
        end = min(start + step - 1, max_count)
        print(f"🔄 수집 중: {start} ~ {end}")
        batch = fetch_recipes(start, end)

        if not batch:
            print(f"⚠️ 수집 실패 또는 빈 결과: {start} ~ {end}")

        all_recipes.extend(batch)
        time.sleep(delay)

    return all_recipes

# ✅ 메인 실행
if __name__ == "__main__":
    data = fetch_all_recipes()
    df = pd.DataFrame(data)
    df.to_csv("recipes_raw.csv", index=False)
    print(f"\n✅ 총 {len(df)}개의 레시피 수집 완료 → recipes_raw.csv 저장됨")
