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
    print(f"총 {len(texts)}개의 뉴스 기사를 불러왔습니다.")

    # 모든 기사에서 문장 단위로 분리
    all_sentences = []
    total_sentences = 0
    valid_sentences = 0
    
    for i, doc in enumerate(texts):
        sentences = nltk.sent_tokenize(doc)
        total_sentences += len(sentences)
        
        # 각 문장에서 줄바꿈 문자 제거
        sentences = [s.replace('\n', ' ').replace('\r', ' ') for s in sentences]
        
        # 영어 알파벳과 기본 문장 부호만 포함된 문장만 선택
        valid_sentences_list = [s for s in sentences if is_valid_english_sentence(s)]
        valid_sentences += len(valid_sentences_list)
        
        if i < 3:  # 처음 3개 기사의 문장만 출력
            print(f"\n기사 {i+1}의 문장들:")
            for j, s in enumerate(valid_sentences_list[:3], 1):
                print(f"  {j}. {s[:100]}...")
        
        all_sentences.extend(valid_sentences_list)

    print(f"\n처리 결과:")
    print(f"- 총 문장 수: {total_sentences}")
    print(f"- 유효한 문장 수: {valid_sentences}")
    print(f"- 제외된 문장 수: {total_sentences - valid_sentences}")

    # DataFrame 생성
    result_df = pd.DataFrame({
        'sentence_id': range(len(all_sentences)),
        'text': all_sentences
    })

    if not os.path.exists('data'):
        os.makedirs('data')
    output_path = 'data/news_sentences.csv'
    result_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n결과가 '{output_path}'에 저장되었습니다.")

if __name__ == "__main__":
    process_news_sentences() 