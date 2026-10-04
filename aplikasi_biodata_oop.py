import tkinter as tk
from tkinter import messagebox
import datetime
import logging
import re
import os

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Warna validasi field
EMPTY_COLOR = "#FFB3B3"   # merah muda (field kosong)
FILLED_COLOR = "white"    # putih (field terisi)


class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x780")
        self.resizable(True, True)
        self.configure(bg="lightyellow")

        # Database user dengan role
        self.users_db = {
            "admin":           {"password": "123",       "role": "admin"},
            "user1":           {"password": "password1", "role": "user"},
            "mahasiswa":       {"password": "123456",    "role": "user"},
            "Salahudin-24106050088": {"password": "salahudin123",   "role": "user"},
            "superadmin":      {"password": "super123",  "role": "superadmin"},
        }

        # Warna tema per role
        self.role_colors = {
            "user":       "#90EE90",
            "admin":      "#FF7F7F",
            "superadmin": "#FFF176",
        }

        self.current_user = None
        self.current_role = None
        self.frame_aktif = None

        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        self._load_remembered_username()
        self._pindah_ke(self.frame_login)

        logging.info("Aplikasi dimulai")

    # ==================================================================
    # TAMPILAN LOGIN
    # ==================================================================
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=80, bg="lightyellow")
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        tk.Label(self.frame_login, text="HALAMAN LOGIN",
                 font=("Arial", 16, "bold"), bg="lightyellow").grid(
            row=0, column=0, columnspan=3, pady=20)

        tk.Label(self.frame_login, text="Username:",
                 font=("Arial", 12), bg="lightyellow").grid(
            row=1, column=0, sticky="W", pady=5)
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, columnspan=2, pady=5, sticky="EW")

        tk.Label(self.frame_login, text="Password:",
                 font=("Arial", 12), bg="lightyellow").grid(
            row=2, column=0, sticky="W", pady=5)
        self.entry_password = tk.Entry(self.frame_login, font=("Arial", 12), show="*")
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

        self.btn_show_pass = tk.Button(self.frame_login, text="Show",
                                       command=self._toggle_password,
                                       font=("Arial", 9))
        self.btn_show_pass.grid(row=2, column=2, padx=5)

        self.var_remember = tk.BooleanVar()
        self.check_remember = tk.Checkbutton(
            self.frame_login, text="Remember Me",
            variable=self.var_remember, bg="lightyellow",
            font=("Arial", 10)
        )
        self.check_remember.grid(row=3, column=1, sticky="W", pady=5)

        self.btn_login = tk.Button(self.frame_login, text="Login",
                                   font=("Arial", 12, "bold"),
                                   command=self._coba_login)
        self.btn_login.grid(row=4, column=0, columnspan=3, pady=20, sticky="EW")

        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        info_label = tk.Label(
            self.frame_login,
            text=("Info: Username yang tersedia:\n"
                  "superadmin (password: super123)   -> role: superadmin (kuning)\n"
                  "admin      (password: 123)        -> role: admin (merah)\n"
                  "user1      (password: password1)  -> role: user (hijau)\n"
                  "mahasiswa  (password: 123456)     -> role: user (hijau)\n"
                  "Salahudin-24106050088 (password: salahudin123) -> role: user (hijau)"),
            font=("Arial", 9), fg="gray", justify=tk.LEFT, bg="lightyellow"
        )
        info_label.grid(row=5, column=0, columnspan=3, pady=10)

    def _toggle_password(self):
        if self.entry_password.cget("show") == "*":
            self.entry_password.config(show="")
            self.btn_show_pass.config(text="Hide")
        else:
            self.entry_password.config(show="*")
            self.btn_show_pass.config(text="Show")

    def _load_remembered_username(self):
        if os.path.exists("remember.txt"):
            with open("remember.txt", "r") as f:
                username = f.read().strip()
                if username:
                    self.entry_username.insert(0, username)
                    self.var_remember.set(True)

    def _save_remembered_username(self, username):
        if self.var_remember.get():
            with open("remember.txt", "w") as f:
                f.write(username)
        else:
            if os.path.exists("remember.txt"):
                os.remove("remember.txt")

    # ==================================================================
    # TAMPILAN BIODATA
    # ==================================================================
    def _buat_tampilan_biodata(self):
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_tgl = tk.StringVar()

        # Trace: setiap perubahan -> validasi + warna
        for v in (self.var_nama, self.var_nim, self.var_jurusan, self.var_email, self.var_telepon, self.var_tgl):
            v.trace_add("write", self.validate_form)

        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20, bg="lightyellow")
        self.frame_biodata.columnconfigure(1, weight=1)

        self.label_judul = tk.Label(self.frame_biodata, text="FORM BIODATA MAHASISWA", font=("Arial", 16, "bold"), bg="lightyellow")
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=15)

        self.frame_input = tk.Frame(self.frame_biodata, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10, bg="lightyellow")

        # --- Nama ---
        tk.Label(self.frame_input, text="Nama Lengkap:", font=("Arial", 12), bg="lightyellow").grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_nama)
        self.entry_nama.grid(row=0, column=1, pady=2)

        # --- NIM ---
        tk.Label(self.frame_input, text="NIM:", font=("Arial", 12), bg="lightyellow").grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_nim)
        self.entry_nim.grid(row=1, column=1, pady=2)

        # --- Jurusan ---
        tk.Label(self.frame_input, text="Jurusan:", font=("Arial", 12), bg="lightyellow").grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_jurusan)
        self.entry_jurusan.grid(row=2, column=1, pady=2)

        # --- Email ---
        tk.Label(self.frame_input, text="Email:", font=("Arial", 12), bg="lightyellow").grid(row=3, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_email)
        self.entry_email.grid(row=3, column=1, pady=2)

        # --- Telepon ---
        tk.Label(self.frame_input, text="Telepon:", font=("Arial", 12), bg="lightyellow").grid(row=4, column=0, sticky="W", pady=2)
        self.entry_telepon = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_telepon)
        self.entry_telepon.grid(row=4, column=1, pady=2)

        # --- Tanggal Lahir ---
        tk.Label(self.frame_input, text="Tanggal Lahir (DD/MM/YYYY):", font=("Arial", 12), bg="lightyellow").grid(row=5, column=0, sticky="W", pady=2)
        self.entry_tgl = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_tgl)
        self.entry_tgl.grid(row=5, column=1, pady=2)

        # --- Alamat (Text + Scrollbar) ---
        tk.Label(self.frame_input, text="Alamat:", font=("Arial", 12), bg="lightyellow").grid(row=6, column=0, sticky="NW", pady=2)
        self.frame_alamat = tk.Frame(self.frame_input, relief=tk.SUNKEN, borderwidth=1, bg="lightyellow")
        self.scrollbar_alamat = tk.Scrollbar(self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_alamat = tk.Text(self.frame_alamat, height=4, width=28, font=("Arial", 12))
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        self.frame_alamat.grid(row=6, column=1, pady=2)

        # Bind perubahan pada Text widget
        self.text_alamat.bind("<KeyRelease>", lambda e: self.validate_form())
        self.text_alamat.bind("<<Paste>>", lambda e: self.after(50, self.validate_form))
        self.text_alamat.bind("<<Cut>>", lambda e: self.after(50, self.validate_form))

        # --- Jenis Kelamin ---
        tk.Label(self.frame_input, text="Jenis Kelamin:", font=("Arial", 12), bg="lightyellow").grid(row=7, column=0, sticky="W", pady=2)
        self.frame_jk = tk.Frame(self.frame_input, bg="lightyellow")
        self.frame_jk.grid(row=7, column=1, sticky="W")
        self.radio_pria = tk.Radiobutton(self.frame_jk, text="Pria", variable=self.var_jk, value="Pria", bg="lightyellow")
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita", bg="lightyellow")
        self.radio_wanita.pack(side=tk.LEFT)

        # --- Checkbox persetujuan ---
        self.check_setuju = tk.Checkbutton(
            self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form,
            bg="lightyellow"
        )
        self.check_setuju.grid(row=8, column=0, columnspan=2, pady=10, sticky="W")

        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

        # --- Tombol Submit & Reset ---
        btn_frame = tk.Frame(self.frame_biodata, bg="lightyellow")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        self.btn_submit = tk.Button(btn_frame, text="Submit Biodata", font=("Arial", 12, "bold"), command=self.submit_data, state=tk.DISABLED)
        self.btn_submit.grid(row=0, column=0, sticky="EW", padx=5)
        self.default_btn_bg = self.btn_submit.cget("bg")

        self.btn_reset = tk.Button(btn_frame, text="Reset Form", font=("Arial", 12), command=self._reset_form_biodata)
        self.btn_reset.grid(row=0, column=1, sticky="EW", padx=5)

        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        for entry in (self.entry_nama, self.entry_nim, self.entry_jurusan,self.entry_email, self.entry_telepon, self.entry_tgl):
            entry.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # --- Label hasil ---
        self.label_hasil = tk.Label(self.frame_biodata, text="", font=("Arial", 12, "italic"), justify=tk.LEFT, bg="lightyellow")
        self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10)

        self._buat_menu()

        # Set warna awal: semua field kosong -> merah
        self.after(50, self.validate_form)

    # ==================================================================
    # THEME BERDASARKAN ROLE
    # ==================================================================
    def _apply_theme(self, color):
        self.configure(bg=color)

        def recolor(widget):
            if isinstance(widget, (tk.Frame, tk.Label, tk.Radiobutton, tk.Checkbutton)):
                try:
                    widget.configure(bg=color)
                except tk.TclError:
                    pass
            for child in widget.winfo_children():
                recolor(child)

        recolor(self.frame_biodata)

    def _apply_login_theme(self, color):
        self.configure(bg="lightyellow")

        def recolor(widget):
            if isinstance(widget, (tk.Frame, tk.Label, tk.Radiobutton, tk.Checkbutton)):
                try:
                    widget.configure(bg="lightyellow")
                except tk.TclError:
                    pass
            for child in widget.winfo_children():
                recolor(child)

        recolor(self.frame_login)

    # ==================================================================
    # NAVIGASI & LOGIN
    # ==================================================================
    def _pindah_ke(self, frame_tujuan):
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        if frame_tujuan == self.frame_login:
            self._hapus_menu()
        elif frame_tujuan == self.frame_biodata:
            self._buat_menu()

        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    def _coba_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        logging.info(f"Login attempt for username: {username}")

        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        if username in self.users_db and self.users_db[username]["password"] == password:
            self.current_user = username
            self.current_role = self.users_db[username]["role"]
            logging.info(f"Successful login for user: {username} (role: {self.current_role})")

            warna = self.role_colors.get(self.current_role, "#FFFFFF")
            self._apply_theme(warna)

            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat Datang, {username}!\nRole Anda: {self.current_role}"
            )

            self._save_remembered_username(username)
            self._reset_form_biodata()
            self._update_title_with_user()
            self._pindah_ke(self.frame_biodata)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    # ==================================================================
    # HELPER
    # ==================================================================
    def _reset_form_biodata(self):
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.var_email.set("")
        self.var_telepon.set("")
        self.var_tgl.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")
        self.validate_form()

    def _update_title_with_user(self):
        if self.current_user:
            self.title(f"Aplikasi Biodata - {self.current_user} [{self.current_role}]")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def _update_field_color(self, widget, is_valid):
        """Ubah warna widget: merah jika kosong, putih jika terisi."""
        try:
            widget.config(bg=FILLED_COLOR if is_valid else EMPTY_COLOR)
        except tk.TclError:
            pass

    # ==================================================================
    # LOGOUT, MENU, KELUAR
    # ==================================================================
    def _logout(self):
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user} (role: {self.current_role})")
            self.current_user = None
            self.current_role = None

            self._apply_login_theme("lightyellow")

            self._hapus_menu()
            self._update_title_with_user()
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)
            self.entry_username.focus_set()

    def _buat_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

    # ==================================================================
    # SIMPAN FILE
    # ==================================================================
    def simpan_hasil(self):
        try:
            hasil_tersimpan = self.label_hasil.cget("text")
            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                return

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user} ({self.current_role})\n")
                file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")
            logging.info(f"Data saved to file: {filename} by {self.current_user}")
        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")
            logging.error(f"Error saving file: {str(e)}")

    # ==================================================================
    # SUBMIT & VALIDASI
    # ==================================================================
    def submit_data(self):
        try:
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            email = self.entry_email.get().strip()
            telepon = self.entry_telepon.get().strip()
            tgl = self.entry_tgl.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            if not nama or not nim or not jurusan or not email or not telepon or not tgl:
                messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
                return

            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
                self.entry_nim.focus_set()
                return

            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self.entry_nama.focus_set()
                return

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showwarning("Format Email Salah", "Masukkan email yang valid!")
                self.entry_email.focus_set()
                return

            if not telepon.isdigit() or not (10 <= len(telepon) <= 13):
                messagebox.showwarning("Format Telepon Salah", "Telepon harus angka 10-13 digit!")
                self.entry_telepon.focus_set()
                return

            try:
                datetime.datetime.strptime(tgl, "%d/%m/%Y")
            except ValueError:
                messagebox.showwarning("Format Tanggal Salah", "Gunakan format DD/MM/YYYY!")
                self.entry_tgl.focus_set()
                return

            hasil = (f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\n"
                     f"Email: {email}\nTelepon: {telepon}\nTanggal Lahir: {tgl}\n"
                     f"Alamat: {alamat}\nJenis Kelamin: {jenis_kelamin}")

            messagebox.showinfo("Data Tersimpan", hasil)

            hasil_lengkap = (f"BIODATA TERSIMPAN:\n"
                             f"Diinput oleh: {self.current_user} ({self.current_role})\n\n{hasil}")
            self.label_hasil.config(text=hasil_lengkap)

            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")
        except Exception as e:
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        email_valid = self.var_email.get().strip() != ""
        telepon_valid = self.var_telepon.get().strip() != ""
        tgl_valid = self.var_tgl.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        # === Verifikasi warna merah untuk field kosong ===
        self._update_field_color(self.entry_nama, nama_valid)
        self._update_field_color(self.entry_nim, nim_valid)
        self._update_field_color(self.entry_jurusan, jurusan_valid)
        self._update_field_color(self.entry_email, email_valid)
        self._update_field_color(self.entry_telepon, telepon_valid)
        self._update_field_color(self.entry_tgl, tgl_valid)

        # Text alamat
        alamat_valid = self.text_alamat.get("1.0", tk.END).strip() != ""
        self._update_field_color(self.text_alamat, alamat_valid)

        if (nama_valid and nim_valid and jurusan_valid and email_valid and telepon_valid and tgl_valid and setuju_valid):
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg=self.default_btn_bg)

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL: 
            self.submit_data()


if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()