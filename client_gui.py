import socket
import tkinter as tk
from tkinter import ttk
import threading

# ---------- CONNECTION ----------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12345))


# ---------- NETWORK ----------
def send_request(msg):
    try:
        client.sendall((msg + "\n").encode())

        data = ""
        while True:
            part = client.recv(1024).decode()
            data += part
            if "\n" in part:
                break

        res = data.strip()
        print("SERVER RESPONSE:", res)
        return res

    except Exception as e:
        return f"Error: {e}"


def send_request_thread(msg):
    def task():
        res = send_request(msg)
        root.after(0, lambda: show_output(res))

    threading.Thread(target=task, daemon=True).start()


def show_output(res):
    output_label.config(text=res)

    if "success" in res.lower():
        output_label.config(fg="green")
    else:
        output_label.config(fg="red")


# ---------- AUTH ----------
def register():
    msg = f"REGISTER {entry_user.get()} {entry_pass.get()}"
    show_output("Processing...")
    send_request_thread(msg)


def login():
    msg = f"LOGIN {entry_user.get()} {entry_pass.get()}"
    show_output("Processing...")
    send_request_thread(msg)


# ---------- LEADERBOARD ----------
def get_leaderboard():
    def task():
        res = send_request("GET")

        def update():
            for row in tree.get_children():
                tree.delete(row)

            for line in res.split("\n"):
                if line:
                    tree.insert("", "end", values=(line,))

        root.after(0, update)

    threading.Thread(target=task, daemon=True).start()


# ---------- QUIZ ----------
quiz_questions = [
    {"question": "Capital of India?", "options": ["Mumbai", "Delhi", "Chennai", "Kolkata"], "answer": "Delhi"},
    {"question": "2 + 2 = ?", "options": ["3", "4", "5", "6"], "answer": "4"},
    {"question": "Language used?", "options": ["Java", "C++", "Python", "Go"], "answer": "Python"}
]

current_q = 0
score = 0
time_left = 10


def start_quiz():
    global current_q, score
    current_q = 0
    score = 0
    show_question()


def show_question():
    global current_q, time_left

    if current_q < len(quiz_questions):
        q = quiz_questions[current_q]
        question_label.config(text=q["question"])

        for i, opt in enumerate(q["options"]):
            buttons[i].config(text=opt)

        time_left = 10
        countdown()
    else:
        finish_quiz()


def check_answer(selected):
    global current_q, score

    if selected == quiz_questions[current_q]["answer"]:
        score += 10

    current_q += 1
    show_question()


def countdown():
    global time_left

    if time_left > 0:
        timer_label.config(text=f"Time left: {time_left}s")
        time_left -= 1
        root.after(1000, countdown)
    else:
        next_question()


def next_question():
    global current_q
    current_q += 1
    show_question()


def finish_quiz():
    question_label.config(text=f"Quiz Finished! Score: {score}")
    show_output("Updating score...")
    send_request_thread(f"UPDATE {score}")


# ---------- GUI ----------
root = tk.Tk()
root.title("Leaderboard System")
root.geometry("500x650")

tk.Label(root, text="Username").pack()
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password").pack()
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Register", command=register).pack(pady=5)
tk.Button(root, text="Login", command=login).pack(pady=5)


# ---------- Leaderboard (Scrollable) ----------
frame = tk.Frame(root)
frame.pack(pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(
    frame,
    columns=("Leaderboard",),
    show="headings",
    yscrollcommand=scrollbar.set
)

tree.heading("Leaderboard", text="Leaderboard Rankings")
tree.pack(fill="both", expand=True)

scrollbar.config(command=tree.yview)

tk.Button(root, text="Get Leaderboard", command=get_leaderboard).pack(pady=5)


# ---------- Quiz ----------
question_label = tk.Label(root, text="", font=("Arial", 12))
question_label.pack(pady=10)

timer_label = tk.Label(root, text="", fg="red")
timer_label.pack()

buttons = []
for i in range(4):
    btn = tk.Button(
        root,
        text="",
        width=20,
        command=lambda i=i: check_answer(buttons[i].cget("text"))
    )
    btn.pack(pady=2)
    buttons.append(btn)

tk.Button(root, text="Start Quiz", command=start_quiz).pack(pady=10)


# ---------- Output ----------
output_label = tk.Label(
    root,
    text="Messages will appear here",
    fg="blue",
    bg="white",
    font=("Arial", 14),
    width=40,
    height=2
)
output_label.pack(pady=10)


root.mainloop()