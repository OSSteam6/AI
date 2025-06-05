import pandas as pd
from sklearn.datasets import fetch_20newsgroups
import nltk
import os
import re

nltk.download('punkt')

def is_valid_english_sentence(text):
    # 영어 알파벳, 숫자, 기본 문장 부호만 포함된 문장인지 확인
    # 허용되는 문자: 영문자, 숫자, 공백, 기본 문장 부호(.,!?;:'"()-)
    pattern = r'^[a-zA-Z0-9\s.,!?;:\'"()-]+$'
    return bool(re.match(pattern, text))

def process_news_sentences():
    print("20 Newsgroups 데이터셋을 가져오는 중...")
    newsgroups = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
    texts = newsgroups.data

    # 모든 기사에서 문장 단위로 분리
    all_sentences = []
    for doc in texts:
        sentences = nltk.sent_tokenize(doc)
        # 각 문장에서 줄바꿈 문자 제거
        sentences = [s.replace('\n', ' ').replace('\r', ' ') for s in sentences]
        # 영어 알파벳과 기본 문장 부호만 포함된 문장만 선택
        valid_sentences = [s for s in sentences if is_valid_english_sentence(s)]
        all_sentences.extend(valid_sentences)

    # DataFrame 생성
    result_df = pd.DataFrame({
        'sentence_id': range(len(all_sentences)),
        'text': all_sentences
    })

    if not os.path.exists('data'):
        os.makedirs('data')
    output_path = 'data/news_sentences.csv'
    result_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"총 {len(all_sentences)}개의 문장이 저장되었습니다.")
    print(f"결과가 '{output_path}'에 저장되었습니다.")

if __name__ == "__main__":
    process_news_sentences() 