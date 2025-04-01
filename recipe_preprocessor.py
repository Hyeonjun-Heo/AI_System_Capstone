import pandas as pd
import re


# ✅ 전처리 함수 정의
def clean_ingredient_text(text):
    if pd.isna(text):
        return []

    # ✅ 1. ● ~ : 패턴 제거
    text = re.sub(r"[●•※★\-]{1,2}[^:\n]+[:：]", "", text)

    # ✅ 2. 줄바꿈을 쉼표로 변환
    text = text.replace('\n', ',')

    # ✅ 3. 라인 필터링
    lines = text.split(',')
    lines = [
        line for line in lines
        if not line.strip().endswith(":")
        and not any(kw in line for kw in ["양념장", "소스", "조리법", "드레싱", "장식", "고명", "약간"])
    ]

    cleaned = []

    for item in lines:
        item = item.strip()
        item = re.sub(r"\[[^]]*\]", "", item)             # 대괄호 제거
        item = re.sub(r"\([^)]*\)", "", item)             # 괄호 제거
        item = re.sub(r"[●※★•:\n\t]", "", item)          # 특수문자 제거
        item = re.sub(r"[^가-힣]", "", item)         # 한글/영문 외 제거
        
        # 정규식 분리
        split_items = re.findall(r'[가-힣]{2,}', item)
        
        for word in split_items:
            word = word.strip()
            if not word:  # ✅ 빈 문자열 제거
                continue
            # if len(word) <= 1 and word not in ALLOW_SHORT:
            #     continue
            cleaned.append(word)


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

