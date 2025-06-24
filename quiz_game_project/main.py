import tkinter as tk
from tkinter import messagebox
import json
import random

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("600x400")
        self.load_questions()

        self.score = 0
        self.q_no = 0
        self.timer_count = 15
        self.selected_category = None
        self.current_question_set = []

        self.init_start_screen()

    def load_questions(self):
        with open("questions.json") as file:
            self.questions = json.load(file)

    def init_start_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to the Quiz Game", font=("Helvetica", 20)).pack(pady=40)
        tk.Button(self.root, text="Start Quiz", command=self.show_category_selection, width=20).pack(pady=10)
        tk.Button(self.root, text="Instructions", command=self.show_instructions, width=20).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20).pack(pady=10)

    def show_instructions(self):
        self.clear_screen()
        instructions = "1. Select a category.\n2. Answer each question before the timer ends.\n3. One point per correct answer.\n4. Final score shown at the end."
        tk.Label(self.root, text="Instructions", font=("Helvetica", 18)).pack(pady=10)
        tk.Label(self.root, text=instructions, font=("Helvetica", 12), justify="left").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.init_start_screen).pack(pady=20)

    def show_category_selection(self):
        self.clear_screen()
        tk.Label(self.root, text="Choose Category", font=("Helvetica", 16)).pack(pady=20)
        for category in self.questions.keys():
            tk.Button(self.root, text=category, width=20, command=lambda c=category: self.start_quiz(c)).pack(pady=5)

    def start_quiz(self, category):
        self.selected_category = category
        self.current_question_set = self.questions[category]
        random.shuffle(self.current_question_set)
        self.score = 0
        self.q_no = 0
        self.display_question()

    def display_question(self):
        self.clear_screen()
        self.timer_count = 15

        if self.q_no >= len(self.current_question_set):
            self.show_result()
            return

        question = self.current_question_set[self.q_no]
        self.var = tk.StringVar()
        self.timer_label = tk.Label(self.root, text="Time Left: 15s", font=("Helvetica", 12))
        self.timer_label.pack(pady=5)
        self.root.after(1000, self.update_timer)

        tk.Label(self.root, text=f"Q{self.q_no + 1}: {question['question']}", font=("Helvetica", 14), wraplength=500).pack(pady=20)

        for opt in question["options"]:
            tk.Radiobutton(self.root, text=opt, variable=self.var, value=opt, font=("Helvetica", 12)).pack(anchor="w", padx=100)

        tk.Button(self.root, text="Next", command=self.next_question).pack(pady=20)

    def update_timer(self):
        if self.timer_count > 0:
            self.timer_count -= 1
            self.timer_label.config(text=f"Time Left: {self.timer_count}s")
            self.root.after(1000, self.update_timer)
        else:
            self.next_question()

    def next_question(self):
        selected = self.var.get()
        if selected == self.current_question_set[self.q_no]["answer"]:
            self.score += 1
        self.q_no += 1
        self.display_question()

    def show_result(self):
        self.clear_screen()
        tk.Label(self.root, text="Quiz Completed!", font=("Helvetica", 18)).pack(pady=20)
        result_text = f"Category: {self.selected_category}\nScore: {self.score} / {len(self.current_question_set)}"
        tk.Label(self.root, text=result_text, font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Play Again", command=self.init_start_screen).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop()
