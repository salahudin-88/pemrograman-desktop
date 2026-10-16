import time
import tkinter as tk


class StopwatchApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Stopwatch")
        self.root.geometry("320x420")
        self.root.resizable(False, False)

        # ===== STATE =====
        self.running = False  # Status stopwatch
        self.start_time = 0.0  # Timestamp mulai
        self.elapsed_time = 0.0  # Total waktu akumulasi (detik)
        self.timer_id = None  # ID root.after()
        self.lap_counter = 0  # Jumlah lap

        # ===== TAMPILAN WAKTU =====
        self.lbl_waktu = tk.Label(
            root,
            text="00:00:00",
            font=("Consolas", 36, "bold"),
            fg="#1e40af",
            bg="#f3f4f6",
            width=10,
            pady=10,
        )
        self.lbl_waktu.pack(pady=15, padx=15, fill="x")

        # ===== FRAME TOMBOL =====
        frame_tombol = tk.Frame(root)
        frame_tombol.pack(pady=5)

        self.btn_mulai = tk.Button(
            frame_tombol,
            text="Mulai",
            width=8,
            command=self.mulai,
            bg="#22c55e",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.btn_mulai.grid(row=0, column=0, padx=5)

        self.btn_stop = tk.Button(
            frame_tombol,
            text="Stop",
            width=8,
            command=self.stop,
            bg="#ef4444",
            fg="white",
            font=("Arial", 10, "bold"),
            state="disabled",
        )
        self.btn_stop.grid(row=0, column=1, padx=5)

        self.btn_reset = tk.Button(
            frame_tombol,
            text="Reset",
            width=8,
            command=self.reset,
            bg="#eab308",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.btn_reset.grid(row=0, column=2, padx=5)

        # Tombol Lap
        self.btn_lap = tk.Button(
            root,
            text="Catat Waktu (Lap)",
            width=25,
            command=self.lap,
            bg="#3b82f6",
            fg="white",
            font=("Arial", 10, "bold"),
            state="disabled",
        )
        self.btn_lap.pack(pady=10)

        # ===== DAFTAR LAP =====
        tk.Label(root, text="Daftar Lap:", font=("Arial", 10, "bold")).pack(
            anchor="w", padx=15
        )

        self.listbox_lap = tk.Listbox(root, height=8, font=("Consolas", 10))
        self.listbox_lap.pack(padx=15, pady=5, fill="both", expand=True)

        # Bind keyboard shortcut
        self.root.bind(
            "<space>",
            lambda e: self.mulai() if not self.running else self.stop(),
        )
        self.root.bind("<Escape>", lambda e: self.reset())

    # =====================================================
    #                   LOGIKA TIMER
    # =====================================================
    def mulai(self):
        """Mulai atau lanjutkan stopwatch."""
        if not self.running:
            self.running = True
            # Hitung titik acuan waktu mulai berdasarkan elapsed time yang ada
            self.start_time = time.perf_counter() - self.elapsed_time
            self.btn_mulai.config(state="disabled")
            self.btn_stop.config(state="normal")
            self.btn_lap.config(state="normal")
            self.tick()

    def stop(self):
        """Hentikan sementara stopwatch."""
        if self.running:
            self.running = False
            self.btn_mulai.config(state="normal")
            self.btn_stop.config(state="disabled")
            self.btn_lap.config(state="disabled")
            if self.timer_id is not None:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

    def reset(self):
        """Reset ke 00:00:00 dan bersihkan daftar lap."""
        self.stop()
        self.elapsed_time = 0.0
        self.lap_counter = 0
        self.lbl_waktu.config(text="00:00:00")
        self.listbox_lap.delete(0, tk.END)

    # =====================================================
    #               PERULANGAN PEWAKTUAN
    # =====================================================
    def tick(self):
        """Pembaruan waktu berdasarkan waktu sistem riil."""
        if not self.running:
            return

        self.elapsed_time = time.perf_counter() - self.start_time
        self.update_tampilan()

        # Pembaruan setiap ~15 ms (cukup tinggi untuk tampilan senti-detik)
        self.timer_id = self.root.after(15, self.tick)

    def update_tampilan(self):
        """Format detik -> MM:SS:CS (Menit : Detik : Senti-detik)."""
        total_cs = int(self.elapsed_time * 100)
        menit = total_cs // 6000
        detik = (total_cs % 6000) // 100
        cs = total_cs % 100

        self.lbl_waktu.config(text=f"{menit:02d}:{detik:02d}:{cs:02d}")

    # =====================================================
    #                       LAP
    # =====================================================
    def lap(self):
        """Catat waktu saat ini ke dalam listbox."""
        if self.running:
            self.lap_counter += 1
            waktu_sekarang = self.lbl_waktu.cget("text")
            self.listbox_lap.insert(
                tk.END, f"Lap {self.lap_counter:02d}  →  {waktu_sekarang}"
            )
            self.listbox_lap.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()