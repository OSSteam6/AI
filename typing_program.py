import tkinter as tk
import time
import csv
import random

# 연습 문장 목록
sentences = [
    "exceptional circumstances require immediate and thoughtful responses",
    "typing speed improves dramatically with consistent and deliberate practice",
    "grabbing a big box gently requires excellent motor control",
    "the extravagant gift box glittered in the sunlight",
    "backspace habit grows worse over time with inaccurate typing",
    "sudden changes in weather patterns demand adaptive strategies",
    "carefully chosen words can shift the tone of an entire conversation",
    "a curious fox leapt over the quiet stream and disappeared",
    "time management is the cornerstone of consistent productivity",
    "she juggled tasks with graceful precision despite constant pressure",
    "in the distance the lighthouse flickered through the thick fog",
    "typing with rhythm improves accuracy and cognitive flow",
    "beneath the surface tensions simmered like an unspoken truth",
    "an unexpected delay changed the trajectory of the entire plan",
    "moments of silence often speak louder than lengthy explanations"
]

#초기 설정
key_logs = []
current_sentence = random.choice(sentences)
sentence_id = sentences.index(current_sentence)
last_press_time = None
start_time = None

#키 누를 때 실행
def on_key_press(event):
    global last_press_time, start_time

    now = time.time()
    if start_time is None:
        start_time = now

    relative_press = round(now - start_time, 3) # 시작 후 경과 시간
    key = event.keysym # 누른 키 이름

    prev_press_time = last_press_time
    last_press_time = relative_press 

    latency = round(relative_press - prev_press_time, 3) if prev_press_time is not None else ""

    # 키 입력 정보 저장
    log = {
        "sentence_id": sentence_id,
        "key": key,
        "press_time": relative_press,
        "release_time": None,
        "key_hold_duration": None,
        "press_press_latency": latency,
    }
    key_logs.append(log)

# 키 땔 때 실행
def on_key_release(event):
    now = time.time()
    relative_release = round(now - start_time, 3)
    key = event.keysym

    for log in reversed(key_logs):
        if log["key"] == key and log["release_time"] is None:
            log["release_time"] = relative_release
            log["key_hold_duration"] = round(relative_release - log["press_time"], 3)
            break

#결과 저장
def save_results():
    final_rows = []
    hold_durations = []
    press_latencies = []
    error_count = 0
    target = current_sentence  
    current_index = 0         

    # 각 키 입력에 대해 처리
    for row in key_logs:
        raw_input = row["key"]

        # 백스페이스 처리
        if raw_input == "BackSpace":
            input_char = "bksp"
            raw_input = ""

            target_char_raw = target[current_index] if 0 <= current_index < len(target) else ""
            if current_index > 0:
                current_index -= 1

            correctness = ""  # bksp는 정오답 없음

        else:
            # 스페이스 처리
            if raw_input == "space":
                input_char = "space"
                raw_input = " "
            else:
                input_char = raw_input

            target_char_raw = target[current_index] if 0 <= current_index < len(target) else ""

            #정답 비교
            if raw_input == target_char_raw:
                correctness = 0
            else:
                correctness = 1
                error_count += 1

            current_index += 1

        target_char = "space" if target_char_raw == " " else target_char_raw

        khd = round(row["key_hold_duration"], 3) if row["key_hold_duration"] else ""
        ppl = round(row["press_press_latency"], 3) if row["press_press_latency"] else ""

        if isinstance(khd, float): hold_durations.append(khd)
        if isinstance(ppl, float): press_latencies.append(ppl)

        final_rows.append({
            "sentence_id": sentence_id,
            "정답": target_char,
            "입력값": input_char,
            "Key-hold": khd,
            "Press-Press": ppl,
            "오답 여부": correctness
        })
    # 키 입력 결과 csv 저장
    with open("typing_results.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=final_rows[0].keys())
        writer.writeheader()
        writer.writerows(final_rows)
    # 평균 통계 저장
    avg_khd = round(sum(hold_durations) / len(hold_durations), 3) if hold_durations else 0
    avg_ppl = round(sum(press_latencies) / len(press_latencies), 3) if press_latencies else 0

    summary_data = [{
        "sentence_id": sentence_id,
        "avg_key_hold_duration": avg_khd,
        "avg_press_press_latency": avg_ppl,
        "error_count": error_count
    }]
    with open("typing_summary.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=summary_data[0].keys())
        writer.writeheader()
        writer.writerows(summary_data)

    print("typing_results.csv 저장 완료")
    print("typing_summary.csv 저장 완료")

    root.destroy()

# tkinter UI
root = tk.Tk()
root.title("타자 연습 프로그램")

label = tk.Label(root, text="문장을 입력하세요:", font=("Arial", 16))
label.pack()

sentence_display = tk.Label(root, text=current_sentence, wraplength=600, font=("Arial", 14), fg="blue")
sentence_display.pack(pady=10)

# 실시간 피드백: 정답이면 초록, 오답이면 빨강
def check_realtime_feedback(event=None):
    typed = entry.get()
    correct_part = current_sentence[:len(typed)]

    if typed == correct_part:
        entry.config(fg="green")
    else:
        entry.config(fg="red")

entry = tk.Entry(root, width=100)
entry.pack(pady=10)
entry.focus_set()
entry.bind("<KeyPress>", on_key_press)
entry.bind("<KeyRelease>", lambda event: [on_key_release(event), check_realtime_feedback(event)])


done_button = tk.Button(root, text="입력 완료 및 저장", command=save_results)
done_button.pack(pady=10)

root.mainloop()
