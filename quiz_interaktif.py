import tkinter as tk
from tkinter import messagebox, ttk


class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Tugas Akhir")
        self.window.geometry("700x500")
        self.window.configure(bg="white")

        # Data quiz (10 soal)
        self.questions = [
            {
                "question": "Apa itu event-driven programming?",
                "options": ["Program yang berjalan berurutan", "Program yang merespons kejadian", "Program tanpa GUI", "Program berbasis web"],
                "correct": 1
            },
            {
                "question": "Widget Tkinter yang digunakan untuk menampilkan teks adalah...",
                "options": ["Button", "Label", "Entry", "Frame"],
                "correct": 1
            },
            {
                "question": "Method yang dipanggil untuk menjalankan aplikasi Tkinter adalah...",
                "options": ["run()", "mainloop()", "start()", "execute()"],
                "correct": 1
            },
            {
                "question": "Fungsi yang digunakan untuk mengikat event keyboard pada widget adalah...",
                "options": ["bind()", "click()", "key()", "event()"],
                "correct": 0
            },
            {
                "question": "Apa fungsi dari self.window.after(1000, fungsi)?",
                "options": ["Menjalankan fungsi segera", "Menjadwalkan fungsi setelah 1000 milidetik", "Menghentikan program", "Menghapus window"],
                "correct": 1
            },
            {
                "question": "Widget yang tepat untuk memilih satu jawaban dari beberapa opsi adalah...",
                "options": ["Checkbutton", "Radiobutton", "Listbox", "Entry"],
                "correct": 1
            },
            {
                "question": "Modul Tkinter yang menyediakan widget bertema modern seperti Progressbar adalah...",
                "options": ["tkinter", "tkinter.ttk", "tkinter.messagebox", "tkinter.font"],
                "correct": 1
            },
            {
                "question": "Variabel Tkinter yang digunakan untuk menyimpan nilai integer adalah...",
                "options": ["StringVar", "IntVar", "DoubleVar", "BooleanVar"],
                "correct": 1
            },
            {
                "question": "Event yang terjadi saat tombol mouse kiri ditekan adalah...",
                "options": ["<Button-1>", "<Key>", "<Motion>", "<Enter>"],
                "correct": 0
            },
            {
                "question": "Method yang digunakan untuk membatalkan timer setelah dijadwalkan adalah...",
                "options": ["after_cancel()", "cancel()", "stop()", "destroy()"],
                "correct": 0
            }
        ]

        # State management
        self.current_question = 0
        self.score = 0
        self.time_left = 30
        self.selected_answer = tk.IntVar(value=-1)
        self.answered = False
        self.timer_id = None

        self.buat_interface()
        self.load_question()
        self.start_timer()

        # Event handling keyboard shortcuts
        self.window.bind("<Return>", self.on_enter)
        self.window.bind("<Escape>", self.on_escape)

    def buat_interface(self):
        """Membuat seluruh elemen antarmuka."""
        self.main_frame = tk.Frame(self.window, bg="white")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header: nomor soal & timer
        top_frame = tk.Frame(self.main_frame, bg="white")
        top_frame.pack(fill="x")

        self.question_num_label = tk.Label(
            top_frame, text="Soal 1/10", font=("Arial", 12, "bold"), bg="white"
        )
        self.question_num_label.pack(side="left")

        self.timer_label = tk.Label(
            top_frame, text="Waktu: 30s", font=("Arial", 12, "bold"),
            fg="blue", bg="white"
        )
        self.timer_label.pack(side="right")

        # Score & progress bar
        score_frame = tk.Frame(self.main_frame, bg="white")
        score_frame.pack(fill="x", pady=10)

        self.score_label = tk.Label(
            score_frame, text="Skor: 0", font=("Arial", 12), bg="white"
        )
        self.score_label.pack(side="left")

        self.score_var = tk.IntVar(value=0)
        self.score_progress = ttk.Progressbar(
            score_frame, orient="horizontal", length=300,
            mode="determinate", maximum=len(self.questions),
            variable=self.score_var
        )
        self.score_progress.pack(side="right", padx=10)

        # Pertanyaan
        self.question_label = tk.Label(
            self.main_frame, text="", font=("Arial", 14, "bold"),
            wraplength=600, justify="left", bg="white"
        )
        self.question_label.pack(fill="x", pady=20)

        # Opsi jawaban
        self.options_frame = tk.Frame(self.main_frame, bg="white")
        self.options_frame.pack(fill="x", padx=20)

        # Feedback benar/salah
        self.feedback_label = tk.Label(
            self.main_frame, text="", font=("Arial", 12, "bold"), bg="white"
        )
        self.feedback_label.pack(pady=10)

        # Tombol aksi
        btn_frame = tk.Frame(self.main_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)

        self.submit_btn = tk.Button(
            btn_frame, text="Submit (Enter)", command=self.submit_answer,
            font=("Arial", 11), bg="#4CAF50", fg="white", width=15
        )
        self.submit_btn.pack(side="left", padx=5)

        self.skip_btn = tk.Button(
            btn_frame, text="Skip (Esc)", command=self.skip_question,
            font=("Arial", 11), bg="#FF9800", fg="white", width=15
        )
        self.skip_btn.pack(side="left", padx=5)

        self.next_btn = tk.Button(
            btn_frame, text="Next", command=self.next_question,
            font=("Arial", 11), bg="#2196F3", fg="white", width=15,
            state="disabled"
        )
        self.next_btn.pack(side="right", padx=5)

    def load_question(self):
        """Memuat soal ke antarmuka."""
        self.answered = False
        self.selected_answer.set(-1)
        self.feedback_label.config(text="", bg="white")
        self.submit_btn.config(state="normal")
        self.next_btn.config(state="disabled")
        self.skip_btn.config(state="normal")

        q = self.questions[self.current_question]
        self.question_label.config(text=q["question"])
        self.question_num_label.config(
            text=f"Soal {self.current_question + 1}/{len(self.questions)}"
        )

        # Hapus opsi lama
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Buat radio button baru
        for i, opt in enumerate(q["options"]):
            rb = tk.Radiobutton(
                self.options_frame, text=opt, variable=self.selected_answer,
                value=i, font=("Arial", 12), anchor="w", bg="white",
                activebackground="white", selectcolor="white"
            )
            rb.pack(fill="x", pady=2)

        self.update_score_progress()

    def start_timer(self):
        """Memulai timer countdown untuk soal saat ini."""
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

        self.time_left = 30
        self.timer_label.config(text=f"Waktu: {self.time_left}s")
        self.timer_id = self.window.after(1000, self.update_timer)

    def update_timer(self):
        """Update timer setiap detik."""
        if self.answered:
            return

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Waktu: {self.time_left}s")
            if self.time_left == 0:
                self.time_up()
            else:
                self.timer_id = self.window.after(1000, self.update_timer)
        else:
            self.time_up()

    def stop_timer(self):
        """Menghentikan timer."""
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

    def submit_answer(self, timeout=False):
        """Validasi dan proses jawaban."""
        if self.answered:
            return

        if not timeout and self.selected_answer.get() == -1:
            messagebox.showwarning("Peringatan", "Pilih jawaban terlebih dahulu!")
            return

        self.answered = True
        self.stop_timer()

        correct_idx = self.questions[self.current_question]["correct"]
        if timeout:
            is_correct = False
        else:
            is_correct = (self.selected_answer.get() == correct_idx)

        if is_correct:
            self.score += 1
            self.show_feedback(True)
        else:
            self.show_feedback(False)

        self.update_score_progress()
        self.disable_options()
        self.submit_btn.config(state="disabled")
        self.skip_btn.config(state="disabled")
        self.next_btn.config(state="normal")

    def skip_question(self, event=None):
        """Skip soal tanpa menjawab (Esc)."""
        if self.answered:
            return

        self.answered = True
        self.stop_timer()
        self.feedback_label.config(text="Soal dilewati", fg="orange")
        self.disable_options()
        self.submit_btn.config(state="disabled")
        self.skip_btn.config(state="disabled")
        self.next_btn.config(state="normal")

    def time_up(self):
        """Waktu habis, jawaban dianggap salah."""
        self.submit_answer(timeout=True)

    def next_question(self):
        """Lanjut ke soal berikutnya atau tampilkan hasil."""
        if not self.answered:
            return

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
            self.start_timer()
        else:
            self.show_result()

    def show_feedback(self, correct):
        """Menampilkan feedback benar/salah dengan animasi."""
        correct_idx = self.questions[self.current_question]["correct"]
        correct_text = self.questions[self.current_question]["options"][correct_idx]

        if correct:
            self.feedback_label.config(text="Benar!", fg="green")
        else:
            self.feedback_label.config(
                text=f"Salah! Jawaban benar: {correct_text}", fg="red"
            )

        self.animate_feedback(correct)

    def animate_feedback(self, correct):
        """Animasi visual kedip pada label feedback."""
        if correct:
            colors = ["lightgreen", "white", "lightgreen", "white"]
        else:
            colors = ["lightcoral", "white", "lightcoral", "white"]

        def step(i=0):
            if i < len(colors):
                self.feedback_label.config(bg=colors[i])
                self.window.after(150, lambda: step(i + 1))
            else:
                self.feedback_label.config(bg="white")

        step()

    def disable_options(self):
        """Menonaktifkan semua radio button."""
        for widget in self.options_frame.winfo_children():
            widget.config(state="disabled")

    def update_score_progress(self):
        """Update skor dan progress bar."""
        self.score_label.config(text=f"Skor: {self.score}")
        self.score_var.set(self.score)

    def on_enter(self, event):
        """Keyboard shortcut Enter: submit atau next."""
        if not self.answered:
            self.submit_answer()
        else:
            self.next_question()

    def on_escape(self, event):
        """Keyboard shortcut Esc: skip soal."""
        if not self.answered:
            self.skip_question()

    def show_result(self):
        """Tampilkan hasil akhir quiz."""
        self.stop_timer()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        result_frame = tk.Frame(self.main_frame, bg="white")
        result_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(
            result_frame, text="Quiz Selesai!", font=("Arial", 24, "bold"), bg="white"
        ).pack(pady=10)

        tk.Label(
            result_frame, text=f"Skor Akhir: {self.score}/{len(self.questions)}",
            font=("Arial", 18), bg="white"
        ).pack(pady=5)

        percentage = (self.score / len(self.questions)) * 100
        tk.Label(
            result_frame, text=f"Persentase: {percentage:.1f}%",
            font=("Arial", 14), bg="white"
        ).pack(pady=5)

        tk.Button(
            result_frame, text="Keluar", command=self.window.destroy,
            font=("Arial", 12), bg="#b50c00", fg="white", width=12
        ).pack(pady=20)

    def jalankan(self):
        """Menjalankan aplikasi."""
        self.window.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.jalankan()