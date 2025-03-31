import pandas as pd
import re


# ✅ 전처리 함수 정의
def clean_ingredient_text(text):
    if pd.isna(text):
        return []

    items = text.split(',')
    cleaned = []

    for item in items:
        item = item.strip()
        item = re.sub(r"\[[^]]*\]", "", item)             # 대괄호 제거
        item = re.sub(r"\([^)]*\)", "", item)             # 괄호 제거
        item = re.sub(r"[●※★•:\n\t]", "", item)          # 특수문자 제거
        item = re.sub(r"[^가-힣]", "", item)         # 한글/영문 외 제거
        
        cleaned.append(item)

    return list(set(cleaned))  # ✅ return 꼭 필요함

# ✅ CSV 불러오기
df = pd.read_csv("recipes_raw.csv")

# ✅ 전처리 적용
df["재료목록"] = df["재료"].apply(clean_ingredient_text)

# ✅ 확인
print(df[["레시피명", "재료", "재료목록"]].head())

# ✅ 저장
df.to_csv("recipes_cleaned.csv", index=False)
print("✅ 최종 전처리 완료 → recipes_cleaned.csv 저장됨")
