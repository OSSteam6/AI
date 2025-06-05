from dotenv import load_dotenv
import pandas as pd
import os
from openai import OpenAI

print("시작 테스트")

# .env파일에서 API키 불러오기
load_dotenv()
api = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api)

print("API 키 값 : ", api)

# 취약 키 top3 불러오기
df = pd.read_csv("weak_keys.csv")
df = df.sort_values("softmax_score", ascending=False)
df_top3 = df[:3]

# 키 3개 꺼내기기
key1 = df_top3.iloc[0]["입력값"]
key2 = df_top3.iloc[1]["입력값"]
key3 = df_top3.iloc[2]["입력값"]

# 프롬프트
prompt = f"Create a sentence using '{key1}', '{key2}', and '{key3}' multiple times."

try:
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = [{"role":"user", "content":prompt}]
)
    print("GPT 문장 생성 :")
    print(response.choices[0].message.content)
except Exception as e:
    print("오류 발생 :", e)



# 생성된 문장 텍스트 파일로 저장
with open("generated_sentence.txt", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)



