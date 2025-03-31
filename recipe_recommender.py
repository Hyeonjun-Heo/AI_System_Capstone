import os
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = openai_api_key)

# 파일 읽기 함수
def load_ingredients(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError('File format not supported')
    return df

# 유통기한 임박 식재료 필터링 (3일 이내)
def filter_expiring_ingredients(df, days=3):
    today = datetime.today()
    df['유통기한'] = pd.to_datetime(df['유통기한'])
    soon_expiring = df[df['유통기한'] <= today + timedelta(days=days)]
    return soon_expiring["종류"].tolist()  # 현재 엑셀파일엔 "종류"로 되어있으나, "식재료"로 바꿀 수 있음.

# ChatGPT를 통한 레시피 추천 함수
def get_recipe(ingredients):
    prompt = f"""
    다음 식재료들을 사용한 맛있는 레시피를 추천해주세요. :
    {', '.join(ingredients)}
    
    너가 만들어낸 이상한 소고기 바나나 칠리소스 볶음 이딴거 말고 실제 사람들이 먹는 음식으로 추천해주세요.
    요리는 두 가지 이상이 나와도 됩니다. 그러니까 너무 관련 없는 재료들끼리 묶어서 레시피로 제공 하려 하지 않아도 됩니다.
    레시피는 [재료], [조리법]을 포함하여 한국어로 제공해주세요.
    """
    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',    # 정밀한 답변 원하면 'gpt-4-turbo'
        messages=[{"role" : "user", "content" : prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# 메인 로직
def main():
    file_path = "/Users/heohyeonjun/Desktop/2025 AI_Capstone_Project/AI_System_Capstone/식재료_랜덤목록.xlsx"  # csv인경우 .csv
    df = load_ingredients(file_path)
    
    expiring_ingredients = filter_expiring_ingredients(df)
    
    if expiring_ingredients:
        print(f"유통기한 임박 재료 : {', '.join(expiring_ingredients)}\n")
        recipe = get_recipe(expiring_ingredients)
        print("추천 레시피:\n")
        print(recipe)
    else:
        print("유통기한이 임박한 재료가 없습니다.")
        
if __name__ == "__main__":
    main()

