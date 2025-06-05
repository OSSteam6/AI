import tkinter as tk

with open("data/generated_sentence.txt", "r", encoding="utf-8") as f:
    target_sentence = f.read().strip()

root = tk.Tk()
root.title("취약 키 연습 프로그램 ")

label = tk.Label(root, text="다음 문장을 연습하세요:", font=("Arial", 16))
label.pack(pady=5)

sentence_display = tk.Label(root, text=target_sentence, wraplength=600, font=("Arial", 14), fg="blue")
sentence_display.pack(pady=10)

entry_var = tk.StringVar()

def on_type(event=None):
    typed = entry_var.get()
    correct_part = target_sentence[:len(typed)]

    # 실시간 피드백: 정답이면 초록, 오답이면 빨강
    if typed == correct_part:
        entry.config(fg="green")
    else:
        entry.config(fg="red")

entry = tk.Entry(root, width=100, textvariable=entry_var, font=("Arial", 12))
entry.pack(pady=10)
entry.focus_set()
entry.bind("<KeyRelease>", on_type)

def reset_input():
    entry_var.set("")
    entry.config(fg="black")

reset_btn = tk.Button(root, text="다시 연습", command=reset_input)
reset_btn.pack(pady=10)

root.mainloop()
