import tkinter as tk
from tkinter import ttk, messagebox
import socket
class QuizClientGUI:
    def __init__(self, host="127.0.0.1", port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.window = tk.Tk()
        self.window.title("Quiz Game")
        self.window.geometry("800x600")
        self.window.configure(bg="#1e1e1e")

        self.frames = {}
        self.score = 0
        self.current_question = None
        self.total_questions = 10
        self.current_question_index = 0

        self.build_name_screen()  # Name screen first
        self.build_category_screen()  # Category screen initialized but not shown
        self.build_question_screen()  # Question screen initialized but not shown
        self.build_result_screen()  # Result screen initialized but not shown

        self.show_frame("name")  # Show the name screen first


    def show_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()

    def build_name_screen(self):
        frame = tk.Frame(self.window, bg="#1e1e1e")
        frame.place(relwidth=1, relheight=1)
        self.frames["name"] = frame

        title = tk.Label(
            frame,
            text="Enter Your Name",
            font=("Arial", 30, "bold"),
            bg="#1e1e1e",
            fg="#ffcc00",
        )
        title.pack(pady=50)

        self.name_entry = tk.Entry(frame, font=("Arial", 16))
        self.name_entry.pack(pady=10)

        start_btn = ttk.Button(
            frame,
            text="Start Quiz",
            command=self.submit_name,
            style="start.TButton",
        )
        start_btn.pack(pady=10)

    def submit_name(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showerror("Error", "Please enter a name.")
            return
        self.client_socket.send(self.player_name.encode())  # Send name to server
        self.show_frame("main")  # Show the main menu after name is entered
        self.build_main_screen()  # Now build the main screen after setting the name
        self.fetch_categories()
    def build_main_screen(self):
        frame = tk.Frame(self.window, bg="#1e1e1e")
        frame.place(relwidth=1, relheight=1)
        self.frames["main"] = frame

        welcome_msg = f"Welcome {self.player_name} to the Quiz Game!"
        title = tk.Label(
            frame,
            text=welcome_msg,  # Display dynamic welcome message
            font=("Arial", 30, "bold"),
            bg="#1e1e1e",
            fg="#ffcc00",
        )
        title.pack(pady=50)

        start_btn = ttk.Button(
            frame,
            text="Start Quiz",
            command=lambda: self.show_frame("categories"),
            style="start.TButton",
        )
        start_btn.pack(pady=10)

        quit_btn = ttk.Button(
            frame, text="Quit Game", command=self.window.quit, style="quit.TButton"
        )
        quit_btn.pack(pady=10)


    def build_category_screen(self):
            frame = tk.Frame(self.window, bg="#1e1e1e")
            frame.place(relwidth=1, relheight=1)
            self.frames["categories"] = frame

            # Label for category selection, now in a separate frame
            label_frame = tk.Frame(frame, bg="#1e1e1e")
            label_frame.pack(pady=20)

            label = tk.Label(
                label_frame,
                text="Select a Category",
                font=("Arial", 24, "bold"),
                bg="#1e1e1e",
                fg="#ffffff",
            )
            label.pack()

            # Container for category buttons
            self.category_container = tk.Frame(frame, bg="#1e1e1e")
            self.category_container.pack(pady=10)

            # Back and Quit buttons (no changes needed)
            back_btn = ttk.Button(
                frame,
                text="Back",
                command=lambda: self.show_frame("main"),
                style="back.TButton",
            )
            back_btn.pack(side="left", padx=10, pady=20)

            quit_btn = ttk.Button(
                frame, text="Quit Game", command=self.window.quit, style="quit.TButton"
            )
            quit_btn.pack(side="right", padx=10, pady=20)

    def build_question_screen(self):
        frame = tk.Frame(self.window, bg="#2e3d49")
        frame.place(relwidth=1, relheight=1)
        self.frames["questions"] = frame

        self.progress_label = tk.Label(
            frame,
            text="Question 1/10",
            font=("Helvetica", 16, "bold"),
            bg="#2e3d49",
            fg="#ffcc00",
        )
        self.progress_label.pack(pady=10)

        # self.timer_label = tk.Label(
        #     frame,
        #     # text="Time Left: 15s",
        #     font=("Helvetica", 16, "bold"),
        #     bg="#2e3d49",
        #     fg="#ff4d4d",
        # )
        # self.timer_label.pack(pady=10)

        self.score_label = tk.Label(
            frame,
            text=f"Score: {self.score}",
            font=("Helvetica", 16, "bold"),
            bg="#2e3d49",
            fg="#ffffff",
        )
        self.score_label.pack(pady=10)

        self.question_label = tk.Label(
            frame,
            text="Question will appear here",
            font=("Helvetica", 18, "bold"),
            wraplength=600,
            justify="center",
            bg="#2e3d49",
            fg="#ffffff",
        )
        self.question_label.pack(pady=20)

        self.options_container = tk.Frame(frame, bg="#2e3d49")
        self.options_container.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.options_container,
                text=f"Option {i+1}",
                font=("Helvetica", 16),
                bg="#333333",
                fg="#ffffff",
                activebackground="#5e5e5e",
                activeforeground="#ffffff",
                relief="flat",
                command=lambda i=i: self.submit_answer(i),
            )
            btn.pack(pady=10, ipadx=10, ipady=5)
            self.option_buttons.append(btn)

        back_btn = tk.Button(
            frame,
            text="Back to Categories",
            font=("Helvetica", 14),
            bg="#4d8c4f",
            fg="#ffffff",
            command=lambda: self.show_frame("categories"),
        )
        back_btn.pack(side="left", padx=10, pady=20)

        quit_btn = tk.Button(
            frame,
            text="Quit Game",
            font=("Helvetica", 14),
            bg="#ff6666",
            fg="#ffffff",
            command=self.window.quit,
        )
        quit_btn.pack(side="right", padx=10, pady=20)

    def build_result_screen(self):
        frame = tk.Frame(self.window, bg="#212121")
        frame.place(relwidth=1, relheight=1)
        self.frames["results"] = frame

        self.result_label = tk.Label(
            frame,
            text="Your Final Score: 0/10",
            font=("Arial", 24, "bold"),
            bg="#212121",
            fg="#ffffff",
        )
        self.result_label.pack(pady=50)

        restart_btn = ttk.Button(
            frame,
            text="Play Again",
            command=lambda: self.show_frame("categories"),
            style="restart.TButton",
        )
        restart_btn.pack(pady=10)

        quit_btn = ttk.Button(
            frame, text="Quit Game", command=self.window.quit, style="quit.TButton"
        )
        quit_btn.pack(pady=10)

    def fetch_categories(self):
        data = self.client_socket.recv(1024).decode()
        categories = data.replace("Available Categories:\n", "").split("\n")
        self.display_categories(categories)

    def display_categories(self, categories):
            # Clear any existing buttons before displaying new ones
            for widget in self.category_container.winfo_children():
                widget.destroy()

            for category in categories:
                btn = ttk.Button(
                    self.category_container,
                    text=category.strip(),
                    command=lambda c=category: self.select_category(c.strip()),
                    style="category.TButton",
                )
                btn.pack(pady=5)


    def select_category(self, category):
        self.score = 0
        self.current_question_index = 0
        self.client_socket.send(category.encode())
        self.show_frame("questions")
        self.fetch_question()

    def fetch_question(self):
        data = self.client_socket.recv(1024).decode()

        if "Quiz completed!" in data:
            self.show_frame("results")
            self.result_label.config(
                text=f"Your Final Score: {self.score}/{self.total_questions}"
            )
            return

        parts = data.split("\n")
        self.current_question = parts[0]
        options = parts[1:]

        self.current_question_index += 1
        self.progress_label.config(
            text=f"Question {self.current_question_index}/{self.total_questions}"
        )
        self.display_question(self.current_question, options)

    def display_question(self, question, options):
        self.question_label.config(text=question)
        for i, option in enumerate(options):
            self.option_buttons[i].config(text=option)

    def submit_answer(self, option_index):
        self.client_socket.send(str(option_index + 1).encode())
        feedback = self.client_socket.recv(1024).decode()
        if "Correct!" in feedback:
            self.score += 1
        self.score_label.config(text=f"Score: {self.score}")
        messagebox.showinfo("Feedback", feedback)
        self.fetch_question()

if __name__ == "__main__":
    style = ttk.Style()
    style.configure("start.TButton", background="#007acc", foreground="white")
    style.configure("quit.TButton", background="#ff6666", foreground="white")
    style.configure("back.TButton", background="#2e8b57", foreground="white")
    style.configure("restart.TButton", background="#4d8c4f", foreground="white")

    style.configure(
        "category.TButton",
        background="#333333",
        foreground="white",
        font=("Helvetica", 16, "bold"),
        padding=10,
        relief="flat",
        width=20,
    )

    style.map(
        "category.TButton",
        background=[("active", "#444444"), ("pressed", "#555555")],
    )

    app = QuizClientGUI()
    app.window.mainloop()