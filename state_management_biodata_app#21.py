import tkinter as tk
from tkinter import messagebox
import os
import re
import datetime

# =========================================================
# DATA USER & WARNA ROLE
# =========================================================
users_db = {
    'admin':     'admin123',
    'user1':     'user123',
    'Salahudin': '24106050088'
}

user_colors = {
    'admin':     '#90EE90',   # Hijau
    'user1':     "#FF83E4",   # Merah
    'Salahudin': '#FFF176'    # Kuning
}

LOGIN_BG = "#604F4F"
current_user = None

# =========================================================
# WINDOW UTAMA
# =========================================================
window = tk.Tk()
window.title("Form Biodata - State Management & Interaktivitas")
window.configure(bg=LOGIN_BG)
window.resizable(True, True)
window.geometry("520x650")
window.minsize(520, 650)

# =========================================================
# VARIABEL KONTROL
# =========================================================
var_login_user = tk.StringVar()
var_login_pass = tk.StringVar()
var_remember   = tk.IntVar()

var_nama          = tk.StringVar()
var_nim           = tk.StringVar()
var_jurusan       = tk.StringVar()
var_hp            = tk.StringVar()
var_email         = tk.StringVar()
var_tanggal_lahir = tk.StringVar()
var_setuju        = tk.IntVar()

# =========================================================
# FUNGSI VALIDASI MASING-MASING FIELD
# =========================================================
def validasi_nama(nama):
    """Nama: min 3 karakter, hanya huruf & spasi."""
    nama = nama.strip()
    if len(nama) < 3:
        return False, "Nama minimal 3 karakter."
    if not re.fullmatch(r"[A-Za-z\s\.\']+", nama):
        return False, "Nama hanya boleh berisi huruf dan spasi."
    return True, ""


def validasi_nim(nim):
    """NIM: hanya angka, panjang 8–15 digit."""
    nim = nim.strip()
    if not nim:
        return False, "NIM tidak boleh kosong."
    if not nim.isdigit():
        return False, "NIM hanya boleh berisi angka."
    if not (8 <= len(nim) <= 15):
        return False, "NIM harus 8–15 digit."
    return True, ""


def validasi_jurusan(jurusan):
    """Jurusan: min 3 karakter, hanya huruf & spasi."""
    jurusan = jurusan.strip()
    if len(jurusan) < 3:
        return False, "Jurusan minimal 3 karakter."
    if not re.fullmatch(r"[A-Za-z\s\.\,\-]+", jurusan):
        return False, "Jurusan hanya boleh berisi huruf dan spasi."
    return True, ""


def validasi_hp(hp):
    """HP: format Indonesia 08xx / +62xx / 62xx, 10–14 digit."""
    hp = hp.strip().replace(" ", "").replace("-", "")
    if not hp:
        return False, "Nomor HP tidak boleh kosong."
    pattern = r"^(\+62|62|0)8[1-9][0-9]{6,11}$"
    if not re.fullmatch(pattern, hp):
        return False, "Format HP salah. Contoh: 081234567890 atau +6281234567890"
    return True, ""


def validasi_email(email):
    """Email: format umum nama@domain.tld."""
    email = email.strip()
    if not email:
        return False, "Email tidak boleh kosong."
    pattern = r"^[\w\.\-\+]+@[\w\-]+(\.[\w\-]+)+$"
    if not re.fullmatch(pattern, email):
        return False, "Format email tidak valid. Contoh: nama@domain.com"
    return True, ""


def validasi_tanggal(tanggal):
    """Tanggal lahir: DD-MM-YYYY, harus tanggal valid."""
    tanggal = tanggal.strip()
    if not tanggal:
        return False, "Tanggal lahir tidak boleh kosong."
    parts = tanggal.split("-")
    if len(parts) != 3:
        return False, "Format harus DD-MM-YYYY. Contoh: 17-08-2005"
    d, m, y = parts
    if not (d.isdigit() and m.isdigit() and y.isdigit()):
        return False, "Tanggal, bulan, dan tahun harus berupa angka."
    d, m, y = int(d), int(m), int(y)
    if not (1900 <= y <= datetime.datetime.now().year):
        return False, f"Tahun harus antara 1900–{datetime.datetime.now().year}."
    try:
        datetime.date(y, m, d)
    except ValueError:
        return False, "Tanggal tidak valid (periksa jumlah hari di bulan tersebut)."
    return True, ""


# =========================================================
# FUNGSI TOGGLE LOGIN BUTTON
# =========================================================
def toggle_login_button(*args):
    if var_remember.get() == 1:
        btn_login.config(state=tk.NORMAL, bg="lightgreen")
    else:
        btn_login.config(state=tk.DISABLED, bg="lightgray")

# =========================================================
# FRAME LOGIN (BACKGROUND PUTIH)
# =========================================================
frame_login = tk.Frame(window, bg=LOGIN_BG)

lbl_login_title = tk.Label(frame_login, text="LOGIN",
                            font=("Arial", 20, "bold"),
                            bg=LOGIN_BG, fg="black")
lbl_login_title.pack(pady=20)

lbl_login_user = tk.Label(frame_login, text="Username:",
                           font=("Arial", 12), bg=LOGIN_BG, fg="black")
lbl_login_user.pack()
entry_login_user = tk.Entry(frame_login, textvariable=var_login_user,
                             width=30, font=("Arial", 12))
entry_login_user.pack(pady=5)

lbl_login_pass = tk.Label(frame_login, text="Password:",
                           font=("Arial", 12), bg=LOGIN_BG, fg="black")
lbl_login_pass.pack()
entry_login_pass = tk.Entry(frame_login, textvariable=var_login_pass,
                             width=30, font=("Arial", 12), show="*")
entry_login_pass.pack(pady=5)


def toggle_password():
    if entry_login_pass.cget("show") == "*":
        entry_login_pass.config(show="")
        btn_show_pass.config(text="Sembunyikan")
    else:
        entry_login_pass.config(show="*")
        btn_show_pass.config(text="Tampilkan")


btn_show_pass = tk.Button(frame_login, text="Tampilkan",
                           command=toggle_password,
                           bg="lightgray", width=15)
btn_show_pass.pack(pady=3)

chk_remember = tk.Checkbutton(frame_login, text="Remember Me",
                                variable=var_remember,
                                bg=LOGIN_BG, activebackground=LOGIN_BG,
                                command=toggle_login_button)
chk_remember.pack(pady=3)

lbl_info = tk.Label(frame_login,
                     text="* Centang 'Remember Me' untuk mengaktifkan tombol Login",
                     font=("Arial", 9, "italic"),
                     bg=LOGIN_BG, fg="gray")
lbl_info.pack(pady=2)

btn_login = tk.Button(frame_login, text="Login",
                       font=("Arial", 12, "bold"),
                       bg="lightgray", fg="white",
                       width=20,
                       state=tk.DISABLED,
                       command=lambda: login())
btn_login.pack(pady=15)

# =========================================================
# FRAME BIODATA
# =========================================================
frame_biodata = tk.Frame(window, bg=LOGIN_BG)

main_frame = tk.Frame(frame_biodata, bg=LOGIN_BG)
main_frame.pack(padx=20, pady=20)

# ✅ JUDUL FORM BIODATA
lbl_biodata_title = tk.Label(
    main_frame,
    text="FORM BIODATA",
    font=("Arial", 20, "bold"),
    bg=LOGIN_BG, fg="black"
)
lbl_biodata_title.grid(row=0, column=0, columnspan=3, pady=(0, 15))

# Sub-judul role user
lbl_biodata_sub = tk.Label(
    main_frame,
    text="",
    font=("Arial", 11, "italic"),
    bg=LOGIN_BG, fg="black"
)
lbl_biodata_sub.grid(row=1, column=0, columnspan=3, pady=(0, 10))

# Frame input
frame_input = tk.Frame(main_frame, bg=LOGIN_BG)
frame_input.grid(row=2, column=0, columnspan=3, sticky="W")

biodata_bg_widgets = [frame_biodata, main_frame, lbl_biodata_title,
                       lbl_biodata_sub, frame_input]


def add_label(parent, text, **kwargs):
    lbl = tk.Label(parent, text=text, font=("Arial", 12),
                   bg=LOGIN_BG, **kwargs)
    biodata_bg_widgets.append(lbl)
    return lbl


def add_error_label(parent, row):
    """Label kecil untuk pesan error per field."""
    lbl = tk.Label(parent, text="", font=("Arial", 9, "italic"),
                   bg=LOGIN_BG, fg="red")
    lbl.grid(row=row, column=2, sticky="W", padx=5)
    biodata_bg_widgets.append(lbl)
    return lbl


# --- Nama ---
add_label(frame_input, "Nama:").grid(row=0, column=0, sticky="W", pady=5)
entry_nama = tk.Entry(frame_input, width=30, font=("Arial", 12),
                       textvariable=var_nama)
entry_nama.grid(row=0, column=1, pady=5)
err_nama = add_error_label(frame_input, 0)

# --- NIM ---
add_label(frame_input, "NIM:").grid(row=1, column=0, sticky="W", pady=5)
entry_nim = tk.Entry(frame_input, width=30, font=("Arial", 12),
                      textvariable=var_nim)
entry_nim.grid(row=1, column=1, pady=5)
err_nim = add_error_label(frame_input, 1)

# --- Jurusan ---
add_label(frame_input, "Jurusan:").grid(row=2, column=0, sticky="W", pady=5)
entry_jurusan = tk.Entry(frame_input, width=30, font=("Arial", 12),
                          textvariable=var_jurusan)
entry_jurusan.grid(row=2, column=1, pady=5)
err_jurusan = add_error_label(frame_input, 2)

# --- HP ---
add_label(frame_input, "No. HP:").grid(row=3, column=0, sticky="W", pady=5)
entry_hp = tk.Entry(frame_input, width=30, font=("Arial", 12),
                     textvariable=var_hp)
entry_hp.grid(row=3, column=1, pady=5)
err_hp = add_error_label(frame_input, 3)

# --- Email ---
add_label(frame_input, "Email:").grid(row=4, column=0, sticky="W", pady=5)
entry_email = tk.Entry(frame_input, width=30, font=("Arial", 12),
                        textvariable=var_email)
entry_email.grid(row=4, column=1, pady=5)
err_email = add_error_label(frame_input, 4)

# --- Tanggal Lahir ---
add_label(frame_input, "Tanggal Lahir:").grid(row=5, column=0, sticky="W", pady=5)
entry_tanggal_lahir = tk.Entry(frame_input, width=30, font=("Arial", 12),
                                textvariable=var_tanggal_lahir)
entry_tanggal_lahir.grid(row=5, column=1, pady=5)
err_tgl = add_error_label(frame_input, 5)

lbl_format_tgl = tk.Label(frame_input,
                           text="(format: DD-MM-YYYY, contoh: 17-08-2005)",
                           font=("Arial", 9, "italic"),
                           bg=LOGIN_BG, fg="gray")
lbl_format_tgl.grid(row=6, column=1, sticky="W")
biodata_bg_widgets.append(lbl_format_tgl)

# --- Alamat ---
add_label(frame_input, "Alamat:").grid(row=7, column=0, sticky="NW", pady=5)
text_alamat = tk.Text(frame_input, width=30, height=4, font=("Arial", 12))
text_alamat.grid(row=7, column=1, pady=5)
err_alamat = add_error_label(frame_input, 7)

# --- Persetujuan ---
check_setuju = tk.Checkbutton(
    master=frame_input,
    text="Saya menyetujui pengumpulan data ini.",
    variable=var_setuju,
    font=("Arial", 10),
    bg=LOGIN_BG,
    command=lambda: validate_form()
)
check_setuju.grid(row=8, column=1, sticky="W", pady=5)
biodata_bg_widgets.append(check_setuju)

# --- Tombol Submit ---
btn_submit = tk.Button(
    master=main_frame,
    text="Submit Biodata",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    command=lambda: submit_data(),
    state=tk.DISABLED
)
btn_submit.grid(row=3, column=0, columnspan=3, pady=10)

default_btn_bg = btn_submit.cget("bg")

# --- Label Hasil ---
label_hasil = tk.Label(
    master=main_frame,
    text="",
    font=("Arial", 12, "italic"),
    bg="lightyellow",
    fg="green",
    justify=tk.LEFT
)
label_hasil.grid(row=4, column=0, columnspan=3, sticky="W", padx=10)

# --- Tombol Logout ---
btn_logout = tk.Button(
    master=main_frame,
    text="Logout",
    font=("Arial", 11, "bold"),
    bg="salmon",
    width=15,
    command=lambda: logout()
)
btn_logout.grid(row=5, column=0, columnspan=3, pady=10)

# =========================================================
# FUNGSI VALIDASI REAL-TIME
# =========================================================
def validate_form(*args):
    """Validasi semua field, tampilkan pesan error, atur state tombol submit."""
    # Nama
    ok, msg = validasi_nama(var_nama.get())
    err_nama.config(text="" if ok or not var_nama.get() else msg)
    nama_ok = ok

    # NIM
    ok, msg = validasi_nim(var_nim.get())
    err_nim.config(text="" if ok or not var_nim.get() else msg)
    nim_ok = ok

    # Jurusan
    ok, msg = validasi_jurusan(var_jurusan.get())
    err_jurusan.config(text="" if ok or not var_jurusan.get() else msg)
    jurusan_ok = ok

    # HP
    ok, msg = validasi_hp(var_hp.get())
    err_hp.config(text="" if ok or not var_hp.get() else msg)
    hp_ok = ok

    # Email
    ok, msg = validasi_email(var_email.get())
    err_email.config(text="" if ok or not var_email.get() else msg)
    email_ok = ok

    # Tanggal Lahir
    ok, msg = validasi_tanggal(var_tanggal_lahir.get())
    err_tgl.config(text="" if ok or not var_tanggal_lahir.get() else msg)
    tgl_ok = ok

    # Alamat
    alamat_ok = text_alamat.get("1.0", tk.END).strip() != ""
    err_alamat.config(text="" if alamat_ok or not text_alamat.get("1.0", tk.END).strip() else "Alamat tidak boleh kosong.")

    # Persetujuan
    setuju_ok = var_setuju.get() == 1

    # Aktifkan tombol submit jika semua valid
    if all([nama_ok, nim_ok, jurusan_ok, hp_ok, email_ok,
            tgl_ok, alamat_ok, setuju_ok]):
        btn_submit.config(state=tk.NORMAL)
    else:
        btn_submit.config(state=tk.DISABLED)

# =========================================================
# FUNGSI SUBMIT DATA
# =========================================================
def submit_data():
    nama          = var_nama.get().strip()
    nim           = var_nim.get().strip()
    jurusan       = var_jurusan.get().strip()
    hp            = var_hp.get().strip()
    email         = var_email.get().strip()
    tanggal_lahir = var_tanggal_lahir.get().strip()
    alamat        = text_alamat.get("1.0", tk.END).strip()
    setuju        = var_setuju.get()

    # Validasi ulang saat submit
    validators = [
        (validasi_nama(nama),                    "Nama"),
        (validasi_nim(nim),                      "NIM"),
        (validasi_jurusan(jurusan),              "Jurusan"),
        (validasi_hp(hp),                        "No. HP"),
        (validasi_email(email),                  "Email"),
        (validasi_tanggal(tanggal_lahir),        "Tanggal Lahir"),
    ]
    for (ok, msg), field_name in validators:
        if not ok:
            messagebox.showerror("Error Validasi", f"{field_name}: {msg}")
            return

    if not alamat:
        messagebox.showerror("Error Validasi", "Alamat tidak boleh kosong.")
        return

    if setuju != 1:
        messagebox.showerror("Error Validasi", "Anda harus menyetujui pengumpulan data.")
        return

    hasil = (
        f"Nama: {nama}\n"
        f"NIM: {nim}\n"
        f"Jurusan: {jurusan}\n"
        f"No. HP: {hp}\n"
        f"Email: {email}\n"
        f"Tanggal Lahir: {tanggal_lahir}\n"
        f"Alamat: {alamat}\n"
        f"Persetujuan: {'Ya' if setuju == 1 else 'Tidak'}"
    )

    messagebox.showinfo("Sukses", "Biodata berhasil disubmit!")
    label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")

# =========================================================
# HOVER TOMBOL SUBMIT
# =========================================================
def on_enter(event):
    if btn_submit['state'] == tk.NORMAL:
        btn_submit.config(bg="lightblue")


def on_leave(event):
    btn_submit.config(bg=default_btn_bg)

# =========================================================
# SHORTCUT ENTER
# =========================================================
def submit_shortcut(event=None):
    if btn_submit['state'] == tk.NORMAL:
        submit_data()
    return "break"

# =========================================================
# SIMPAN HASIL
# =========================================================
def simpan_hasil():
    hasil_tersimpan = label_hasil.cget("text")
    if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
        messagebox.showwarning(
            "Peringatan",
            "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu."
        )
        return
    with open("biodata_tersimpan.txt", "w") as file:
        file.write(hasil_tersimpan)
    messagebox.showinfo(
        "Info",
        "Data berhasil disimpan ke file 'biodata_tersimpan.txt'."
    )

# =========================================================
# KELUAR APLIKASI
# =========================================================
def keluar_aplikasi():
    if messagebox.askokcancel(
        "Keluar",
        "Apakah Anda yakin ingin keluar dari aplikasi?"
    ):
        window.destroy()

# =========================================================
# FUNGSI WARNA / THEME
# =========================================================
def apply_theme(username=None):
    if username is None:
        color = LOGIN_BG
    else:
        color = user_colors.get(username, LOGIN_BG)

    for w in biodata_bg_widgets:
        try:
            w.configure(bg=color)
        except tk.TclError:
            pass

    # Update teks sub-judul dengan info user & role
    if username:
        role_map = {
            'admin':     'Administrator',
            'user1':     'User Biasa',
            'Salahudin': 'Mahasiswa'
        }
        role = role_map.get(username, 'User')
        lbl_biodata_sub.config(text=f"Login sebagai: {username} ({role})")
    else:
        lbl_biodata_sub.config(text="")

# =========================================================
# FUNGSI LOGIN
# =========================================================
def login():
    global current_user

    username = var_login_user.get().strip()
    password = var_login_pass.get()

    if not username or not password:
        messagebox.showwarning("Login Gagal",
                               "Username dan Password tidak boleh kosong.")
        entry_login_user.focus_set()
        return

    if len(username) < 3:
        messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
        entry_login_user.focus_set()
        return

    if username in users_db and users_db[username] == password:
        current_user = username

        if var_remember.get() == 1:
            with open("remember.txt", "w") as f:
                f.write(username)
        else:
            if os.path.exists("remember.txt"):
                os.remove("remember.txt")

        apply_theme(username)
        window.configure(bg=user_colors.get(username, LOGIN_BG))

        role_map = {
            'admin': 'Administrator',
            'user1': 'User Biasa',
            'Salahudin': 'Mahasiswa'
        }
        role = role_map.get(username, 'User')
        window.title(f"Form Biodata - {username} ({role})")

        frame_login.pack_forget()
        frame_biodata.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        var_login_pass.set("")
        messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
    else:
        messagebox.showerror("Login Gagal", "Username atau Password salah.")
        var_login_pass.set("")
        entry_login_user.focus_set()

# =========================================================
# FUNGSI LOGOUT
# =========================================================
def logout():
    global current_user

    if messagebox.askyesno("Logout",
                           f"Apakah {current_user} yakin ingin logout?"):
        current_user = None

        apply_theme(None)
        window.configure(bg=LOGIN_BG)
        window.title("Form Biodata - State Management & Interaktivitas")

        # Reset form biodata
        var_nama.set("")
        var_nim.set("")
        var_jurusan.set("")
        var_hp.set("")
        var_email.set("")
        var_tanggal_lahir.set("")
        var_setuju.set(0)
        text_alamat.delete("1.0", tk.END)
        label_hasil.config(text="")
        validate_form()

        frame_biodata.pack_forget()
        frame_login.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        var_login_user.set("")
        var_login_pass.set("")
        toggle_login_button()
        entry_login_user.focus_set()

# =========================================================
# LOAD REMEMBERED USERNAME
# =========================================================
if os.path.exists("remember.txt"):
    try:
        with open("remember.txt", "r") as f:
            last_user = f.read().strip()
            if last_user:
                var_login_user.set(last_user)
                var_remember.set(1)
    except Exception:
        pass

# =========================================================
# EVENT BINDING
# =========================================================
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

for entry in (entry_nama, entry_nim, entry_jurusan, entry_hp,
              entry_email, entry_tanggal_lahir):
    entry.bind("<Return>", submit_shortcut)

text_alamat.bind("<Return>", submit_shortcut)

entry_login_user.bind("<Return>",
                      lambda e: login() if btn_login['state'] == tk.NORMAL else None)
entry_login_pass.bind("<Return>",
                      lambda e: login() if btn_login['state'] == tk.NORMAL else None)

# =========================================================
# TRACE VALIDASI REAL-TIME
# =========================================================
for var in (var_nama, var_nim, var_jurusan, var_hp,
            var_email, var_tanggal_lahir, var_setuju):
    var.trace_add("write", validate_form)

text_alamat.bind("<KeyRelease>", lambda e: validate_form())
var_remember.trace_add("write", toggle_login_button)

# =========================================================
# MENU BAR
# =========================================================
menu_bar = tk.Menu(master=window)
window.config(menu=menu_bar)

file_menu = tk.Menu(master=menu_bar, tearoff=0)
menu_bar.add_cascade(label="Dashboard", menu=file_menu)

file_menu.add_command(label="Simpan Hasil", command=simpan_hasil)
file_menu.add_separator()
file_menu.add_command(label="Keluar", command=keluar_aplikasi)

# =========================================================
# TAMPILKAN HALAMAN LOGIN PERTAMA KALI
# =========================================================
frame_biodata.pack_forget()
frame_login.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
window.configure(bg=LOGIN_BG)

validate_form()
toggle_login_button()
entry_login_user.focus_set()

# =========================================================
# JALANKAN
# =========================================================
window.mainloop()