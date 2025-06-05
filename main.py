import os
from src.process_news import process_news_sentences
from src.typing_program import run_typing_program
from src.find_weak_keys import analyze_typing_results
from src.generate_sentence import generate_sentences
from src.weak_key_typing_program import run_weak_key_typing

def main():
    # 1. 뉴스 데이터에서 문장 추출
    print("\n=== 1. 뉴스 데이터에서 문장 추출 ===")
    process_news_sentences()
    
    # 2. 타이핑 연습 실행
    print("\n=== 2. 타이핑 연습 실행 ===")
    run_typing_program()
    
    # 3. 타이핑 결과 분석
    print("\n=== 3. 타이핑 결과 분석 ===")
    analyze_typing_results()
    
    # 4. 취약 키를 바탕으로 문장 생성
    print("\n=== 4. 취약 키를 바탕으로 문장 생성 ===")
    generate_sentences()
    
    # 5. 약한 키를 사용한 타이핑 연습 실행
    print("\n=== 5. 약한 키를 사용한 타이핑 연습 실행 ===")
    run_weak_key_typing()

if __name__ == "__main__":
    # data 폴더가 없으면 생성
    if not os.path.exists('data'):
        os.makedirs('data')
    
    main() 