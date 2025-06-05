import pandas as pd
import numpy as np

#manhattan_distance 함수
def manhattan_distance(vec1, vec2):
    return np.sum(np.abs(vec1 - vec2))

#softmax 함수
def softmax(x):
    e_x = np.exp(x - np.max(x))  # 수치 안정성 고려
    return e_x / e_x.sum()

def find_weak_keys(results_path, summary_path, top_n_sentence=3, top_n_keys=5):
    # CSV 파일 로드
    results_df = pd.read_csv(results_path)
    summary_df = pd.read_csv(summary_path)  # 사용되지 않지만 포함

    # 문장 단위 평균 통계 계산
    sentence_stats = results_df.groupby("sentence_id").agg({
        "Key-hold": "mean",
        "Press-Press": "mean",
        "오답 여부": "mean"
    }).rename(columns={
        "Key-hold": "avg_khd",
        "Press-Press": "avg_ppl",
        "오답 여부": "error_rate"
    }).reset_index()

    # 기준 벡터: 전체 평균
    baseline_vector = sentence_stats[["avg_khd", "avg_ppl", "error_rate"]].mean().values

    # 문장별 거리 계산
    sentence_stats["distance"] = sentence_stats[["avg_khd", "avg_ppl", "error_rate"]].apply(
        lambda row: manhattan_distance(row.values, baseline_vector), axis=1
    )

    # 이상 문장 상위 N개 선택
    top_outliers = sentence_stats.sort_values("distance", ascending=False).head(top_n_sentence)
    outlier_ids = top_outliers["sentence_id"].tolist()

    # 이상 문장의 문자 데이터 추출
    outlier_data = results_df[results_df["sentence_id"].isin(outlier_ids)]

    # 이상 문장에 포함된 키별 평균 통계
    key_stats = outlier_data.groupby("입력값").agg({
        "Key-hold": "mean",
        "Press-Press": "mean",
        "오답 여부": "mean"
    }).rename(columns={
        "Key-hold": "avg_khd",
        "Press-Press": "avg_ppl",
        "오답 여부": "error_rate"
    }).reset_index()

    # 이상 키를 찾을때 사용하는 기준 벡터 계산(전체 키에 대한 평균)
    key_stats_all = results_df.groupby("입력값").agg({
    "Key-hold": "mean",
    "Press-Press": "mean",
    "오답 여부": "mean"
    }).rename(columns={
    "Key-hold": "avg_khd",
    "Press-Press": "avg_ppl",
    "오답 여부": "error_rate"
    }).reset_index()

    key_baseline = key_stats_all[["avg_khd", "avg_ppl", "error_rate"]].mean().values

    # 키별 거리 계산
    key_stats["distance"] = key_stats[["avg_khd", "avg_ppl", "error_rate"]].apply(
        lambda row: manhattan_distance(row.values, key_baseline), axis=1
    )

    # 취약키 추출 및 softmax 점수 계산
    weak_keys = key_stats.sort_values("distance", ascending=False).head(top_n_keys).copy()
    weak_keys["softmax_score"] = softmax(weak_keys["distance"].values)

    return weak_keys[["입력값", "avg_khd", "avg_ppl", "error_rate", "distance", "softmax_score"]]


if __name__ == "__main__":
    results_path = "data/typing_results.csv"
    summary_path = "data/typing_summary.csv"

    weak_keys = find_weak_keys(results_path, summary_path)

    # 결과 CSV로 저장
    output_path = "data/weak_keys.csv"
    weak_keys.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"취약키 분석 결과가 '{output_path}' 파일로 저장되었습니다.")
