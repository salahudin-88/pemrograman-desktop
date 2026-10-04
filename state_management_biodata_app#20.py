import tkinter as tk
from tkinter import messagebox
import os

# =========================================================
# DATA USER & WARNA ROLE
# =========================================================
users_db = {
    'admin':     'admin123',
    'user1':     'user123',
    'Salahudin(24106050088)': 'salahudin123'
}

user_colors = {
    'admin':     '#90EE90',   # Hijau
    'user1':     "#ADA9FC",   # Ungu
    'Salahudin(24106050088)': '#FFF176'    # Kuning
}

LOGIN_BG = "#FFFFFF"          # Putih (satu-satunya warna default)
current_user = None

# =========================================================
# WINDOW UTAMA
# =========================================================
window = tk.Tk()
window.title("Form Biodata - State Management & Interaktivitas")
window.configure(bg=LOGIN_BG)
window.resizable(True, True)
window.minsize(500, 600)
window.geometry("520x650")

# =========================================================
# VARIABEL KONTROL
# =========================================================
var_login_user = tk.StringVar()
var_login_pass = tk.StringVar()
var_remember   = tk.IntVar()

var_nama    = tk.StringVar()
var_nim     = tk.StringVar()
var_jurusan = tk.StringVar()
var_hp      = tk.StringVar()
var_email   = tk.StringVar()
var_setuju  = tk.IntVar()

# =========================================================
# FRAME LOGIN (BACKGROUND PUTIH)
# =========================================================
frame_login = tk.Frame(window, bg=LOGIN_BG)

lbl_login_title = tk.Label(frame_login, text="LOGIN", font=("Arial", 20, "bold"), bg=LOGIN_BG, fg="black")
lbl_login_title.pack(pady=20)

lbl_login_user = tk.Label(frame_login, text="Username:", font=("Arial", 12), bg=LOGIN_BG, fg="black")
lbl_login_user.pack()
entry_login_user = tk.Entry(frame_login, textvariable=var_login_user, width=30, font=("Arial", 12))
entry_login_user.pack(pady=5)

lbl_login_pass = tk.Label(frame_login, text="Password:", font=("Arial", 12), bg=LOGIN_BG, fg="black")
lbl_login_pass.pack()
entry_login_pass = tk.Entry(frame_login, textvariable=var_login_pass, width=30, font=("Arial", 12), show="*")
entry_login_pass.pack(pady=5)


def toggle_password():
    if entry_login_pass.cget("show") == "*":
        entry_login_pass.config(show="")
        btn_show_pass.config(text="Sembunyikan")
    else:
        entry_login_pass.config(show="*")
        btn_show_pass.config(text="Tampilkan")


btn_show_pass = tk.Button(frame_login, text="Tampilkan", command=toggle_password, bg="lightgray", width=15)
btn_show_pass.pack(pady=3)

chk_remember = tk.Checkbutton(frame_login, text="Remember Me", variable=var_remember, bg=LOGIN_BG, activebackground=LOGIN_BG)
chk_remember.pack(pady=3)

btn_login = tk.Button(frame_login, text="Login", font=("Arial", 12, "bold"), bg="lightgreen", width=20, command=lambda: login())
btn_login.pack(pady=15)

# =========================================================
# FRAME BIODATA (WARNA DINAMIS SESUAI ROLE)
# =========================================================
frame_biodata = tk.Frame(window, bg=LOGIN_BG)

main_frame = tk.Frame(frame_biodata, bg=LOGIN_BG)
main_frame.pack(padx=20, pady=20)

frame_input = tk.Frame(main_frame, bg=LOGIN_BG)
frame_input.grid(row=0, column=0, columnspan=2, sticky="W")

biodata_bg_widgets = [frame_biodata, main_frame, frame_input]


def add_label(parent, text, **kwargs):
    lbl = tk.Label(parent, text=text, font=("Arial", 12),
                   bg=LOGIN_BG, **kwargs)
    biodata_bg_widgets.append(lbl)
    return lbl


# --- Input Biodata ---
add_label(frame_input, "Nama:").grid(row=0, column=0, sticky="W", pady=5)
entry_nama = tk.Entry(frame_input, width=30, font=("Arial", 12), textvariable=var_nama)
entry_nama.grid(row=0, column=1, pady=5)

add_label(frame_input, "NIM:").grid(row=1, column=0, sticky="W", pady=5)
entry_nim = tk.Entry(frame_input, width=30, font=("Arial", 12), textvariable=var_nim)
entry_nim.grid(row=1, column=1, pady=5)

add_label(frame_input, "Jurusan:").grid(row=2, column=0, sticky="W", pady=5)
entry_jurusan = tk.Entry(frame_input, width=30, font=("Arial", 12), textvariable=var_jurusan)
entry_jurusan.grid(row=2, column=1, pady=5)

add_label(frame_input, "HP:").grid(row=3, column=0, sticky="W", pady=5)
entry_hp = tk.Entry(frame_input, width=30, font=("Arial", 12), textvariable=var_hp)
entry_hp.grid(row=3, column=1, pady=5)

add_label(frame_input, "Email:").grid(row=4, column=0, sticky="W", pady=5)
entry_email = tk.Entry(frame_input, width=30, font=("Arial", 12), textvariable=var_email)
entry_email.grid(row=4, column=1, pady=5)

add_label(frame_input, "Alamat:").grid(row=5, column=0, sticky="NW", pady=5)
text_alamat = tk.Text(frame_input, width=30, height=4, font=("Arial", 12))
text_alamat.grid(row=5, column=1, pady=5)

check_setuju = tk.Checkbutton(
    master=frame_input,
    text="Saya menyetujui pengumpulan data ini.",
    variable=var_setuju,
    font=("Arial", 10),
    bg=LOGIN_BG,
    command=lambda: validate_form()
)
check_setuju.grid(row=6, column=1, sticky="W", pady=5)
biodata_bg_widgets.append(check_setuju)

btn_submit = tk.Button(
    master=main_frame,
    text="Submit Biodata",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    command=lambda: submit_data(),
    state=tk.DISABLED
)
btn_submit.grid(row=7, column=0, columnspan=2, pady=10)

default_btn_bg = btn_submit.cget("bg")

label_hasil = tk.Label(
    master=main_frame,
    text="",
    font=("Arial", 12, "italic"),
    bg="lightyellow",
    fg="green",
    justify=tk.LEFT
)
label_hasil.grid(row=8, column=0, columnspan=2, sticky="W", padx=10)

btn_logout = tk.Button(
    master=main_frame,
    text="Logout",
    font=("Arial", 11, "bold"),
    bg="salmon",
    width=15,
    command=lambda: logout()
)
btn_logout.grid(row=9, column=0, columnspan=2, pady=10)

# =========================================================
# FUNGSI VALIDASI FORM BIODATA
# =========================================================
def validate_form(*args):
    nama_valid    = var_nama.get().strip() != ""
    nim_valid     = var_nim.get().strip() != ""
    jurusan_valid = var_jurusan.get().strip() != ""
    hp_valid      = var_hp.get().strip() != ""
    email_valid   = var_email.get().strip() != ""
    alamat_valid  = text_alamat.get("1.0", tk.END).strip() != ""
    setuju_valid  = var_setuju.get() == 1

    if all([nama_valid, nim_valid, jurusan_valid, hp_valid,
            email_valid, alamat_valid, setuju_valid]):
        btn_submit.config(state=tk.NORMAL)
    else:
        btn_submit.config(state=tk.DISABLED)

# =========================================================
# FUNGSI SUBMIT DATA
# =========================================================
def submit_data():
    nama    = var_nama.get().strip()
    nim     = var_nim.get().strip()
    jurusan = var_jurusan.get().strip()
    alamat  = text_alamat.get("1.0", tk.END).strip()
    hp      = var_hp.get().strip()
    email   = var_email.get().strip()
    setuju  = var_setuju.get()

    hasil = (
        f"Nama: {nama}\n"
        f"NIM: {nim}\n"
        f"Jurusan: {jurusan}\n"
        f"Alamat: {alamat}\n"
        f"HP: {hp}\n"
        f"Email: {email}\n"
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
# SHORTCUT ENTER UNTUK SUBMIT
# =========================================================
def submit_shortcut(event=None):
    if btn_submit['state'] == tk.NORMAL:
        submit_data()
    return "break"

# =========================================================
# SIMPAN HASIL KE FILE
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
# FUNGSI WARNA / THEME (HANYA BIODATA)
# =========================================================
def apply_theme(username=None):
    """Terapkan warna background sesuai role user (khusus halaman biodata)."""
    if username is None:
        color = LOGIN_BG
    else:
        color = user_colors.get(username, LOGIN_BG)

    for w in biodata_bg_widgets:
        try:
            w.configure(bg=color)
        except tk.TclError:
            pass

# =========================================================
# FUNGSI LOGIN
# =========================================================
def login():
    global current_user

    username = var_login_user.get().strip()
    password = var_login_pass.get()

    if not username or not password:
        messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
        entry_login_user.focus_set()
        return

    if len(username) < 3:
        messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
        entry_login_user.focus_set()
        return

    if username in users_db and users_db[username] == password:
        current_user = username

        # Remember Me
        if var_remember.get() == 1:
            with open("remember.txt", "w") as f:
                f.write(username)
        else:
            if os.path.exists("remember.txt"):
                os.remove("remember.txt")

        # Terapkan warna biodata sesuai role
        apply_theme(username)
        window.configure(bg=user_colors.get(username, LOGIN_BG))

        # Title + role
        role_map = {
            'admin': 'Admin',
            'user1': 'User1',
            'Salahudin(24106050088)': 'Salahudin-24106050088'
        }
        role = role_map.get(username, 'User')
        window.title(f"Form Biodata - {username} ({role})")

        # Sembunyikan login, tampilkan biodata
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
        var_setuju.set(0)
        text_alamat.delete("1.0", tk.END)
        label_hasil.config(text="")
        validate_form()

        # Sembunyikan biodata, tampilkan login
        frame_biodata.pack_forget()
        frame_login.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        var_login_user.set("")
        var_login_pass.set("")
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

entry_nama.bind("<Return>", submit_shortcut)
entry_nim.bind("<Return>", submit_shortcut)
entry_hp.bind("<Return>", submit_shortcut)
entry_email.bind("<Return>", submit_shortcut)
text_alamat.bind("<Return>", submit_shortcut)

entry_login_user.bind("<Return>", lambda e: login())
entry_login_pass.bind("<Return>", lambda e: login())

# =========================================================
# TRACE VALIDASI REAL-TIME
# =========================================================
var_nama.trace_add("write", validate_form)
var_nim.trace_add("write", validate_form)
var_jurusan.trace_add("write", validate_form)
var_hp.trace_add("write", validate_form)
var_email.trace_add("write", validate_form)

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
entry_login_user.focus_set()

# =========================================================
# JALANKAN
# =========================================================
window.mainloop()