import tkinter as tk
from tkinter import messagebox

# ==========================
# Window & Frame Utama
# ==========================
window = tk.Tk()
window.title("Form Biodata - State Management & Interaktivitas")

bg_color = "#ffc118"
window.configure(bg=bg_color)

window.resizable(True, True)
window.minsize(500, 600)

main_frame = tk.Frame(window)
main_frame.pack(padx=20, pady=20)

frame_input = tk.Frame(main_frame)
frame_input.grid(row=0, column=0, columnspan=2, sticky="W")

# ==========================
# Variabel Kontrol
# ==========================
var_setuju = tk.IntVar()
var_nama = tk.StringVar()
var_nim = tk.StringVar()
var_jurusan = tk.StringVar()
var_hp = tk.StringVar()
var_email = tk.StringVar()

# ==========================
# Fungsi-fungsi
# ==========================
def validate_form(*args):
    nama_valid = var_nama.get().strip() != ""
    nim_valid = var_nim.get().strip() != ""
    jurusan_valid = var_jurusan.get().strip() != ""
    hp_valid = var_hp.get().strip() != ""
    email_valid = var_email.get().strip() != ""
    alamat_valid = text_alamat.get("1.0", tk.END).strip() != ""
    setuju_valid = var_setuju.get() == 1

    if nama_valid and nim_valid and jurusan_valid and alamat_valid and hp_valid and email_valid and setuju_valid:
        btn_submit.config(state=tk.NORMAL)
    else:
        btn_submit.config(state=tk.DISABLED)


def submit_data():
    nama = var_nama.get().strip()
    nim = var_nim.get().strip()
    jurusan = var_jurusan.get().strip()
    alamat = text_alamat.get("1.0", tk.END).strip()
    hp = var_hp.get().strip()
    email = var_email.get().strip()
    setuju = var_setuju.get()

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


def on_enter(event):
    if btn_submit['state'] == tk.NORMAL:
        btn_submit.config(bg="dark green")


def on_leave(event):
    btn_submit.config(bg=default_bg)


def submit_shortcut(event=None):
    if btn_submit['state'] == tk.NORMAL:
        submit_data()
    return "break"


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


def keluar_aplikasi():
    if messagebox.askokcancel(
        "Keluar",
        "Apakah Anda yakin ingin keluar dari aplikasi?"
    ):
        window.destroy()

# ==========================
# Widget Input
# ==========================
tk.Label(frame_input, text="Nama:", font=("Arial", 12)).grid(
    row=0, column=0, sticky="W", pady=5
)
entry_nama = tk.Entry(
    frame_input, width=30, font=("Arial", 12), textvariable=var_nama
)
entry_nama.grid(row=0, column=1, pady=5)

tk.Label(frame_input, text="NIM:", font=("Arial", 12)).grid(
    row=1, column=0, sticky="W", pady=5
)
entry_nim = tk.Entry(
    frame_input, width=30, font=("Arial", 12), textvariable=var_nim
)
entry_nim.grid(row=1, column=1, pady=5)

tk.Label(frame_input, text="Jurusan:", font=("Arial", 12)).grid(
    row=2, column=0, sticky="W", pady=5
)
entry_jurusan = tk.Entry(
    frame_input, width=30, font=("Arial", 12), textvariable=var_jurusan
)
entry_jurusan.grid(row=2, column=1, pady=5)

tk.Label(frame_input, text="HP:", font=("Arial", 12)).grid(
    row=3, column=0, sticky="W", pady=5
)
entry_hp = tk.Entry(
    frame_input, width=30, font=("Arial", 12), textvariable=var_hp
)
entry_hp.grid(row=3, column=1, pady=5)

tk.Label(frame_input, text="Email:", font=("Arial", 12)).grid(
    row=4, column=0, sticky="W", pady=5
)
entry_email = tk.Entry(
    frame_input, width=30, font=("Arial", 12), textvariable=var_email
)
entry_email.grid(row=4, column=1, pady=5)

tk.Label(frame_input, text="Alamat:", font=("Arial", 12)).grid(
    row=5, column=0, sticky="NW", pady=5
)
text_alamat = tk.Text(frame_input, width=30, height=4, font=("Arial", 12))
text_alamat.grid(row=5, column=1, pady=5)

check_setuju = tk.Checkbutton(
    master=frame_input,
    text="Saya menyetujui pengumpulan data ini.",
    variable=var_setuju,
    font=("Arial", 10),
    command=validate_form
)
check_setuju.grid(row=6, column=1, sticky="W", pady=5)

btn_submit = tk.Button(
    master=main_frame,
    text="Submit Biodata",
    font=("Arial", 12, "bold"),
    bg="dark green",
    fg="white",
    command=submit_data,
    state=tk.DISABLED
)
btn_submit.grid(row=7, column=0, columnspan=2, pady=10)

default_bg = btn_submit.cget("bg")

label_hasil = tk.Label(
    master=main_frame,
    text="",
    font=("Arial", 12, "italic"),
    bg="lightyellow",
    fg="green",
    justify=tk.LEFT
)
label_hasil.grid(row=8, column=0, columnspan=2, sticky="W", padx=10)

# ==========================
# Trace untuk validasi real-time
# ==========================
var_nama.trace_add("write", validate_form)
var_nim.trace_add("write", validate_form)
var_hp.trace_add("write", validate_form)
var_email.trace_add("write", validate_form)

# ==========================
# Event Binding
# ==========================
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

entry_nama.bind("<Return>", submit_shortcut)
entry_nim.bind("<Return>", submit_shortcut)
entry_hp.bind("<Return>", submit_shortcut)
entry_email.bind("<Return>", submit_shortcut)
text_alamat.bind("<Return>", submit_shortcut)

# ==========================
# Menu Bar
# ==========================
menu_bar = tk.Menu(master=window)
window.config(menu=menu_bar)

file_menu = tk.Menu(master=menu_bar, tearoff=0)
menu_bar.add_cascade(label="Dashboard", menu=file_menu)

file_menu.add_command(label="Simpan Hasil", command=simpan_hasil)
file_menu.add_separator()
file_menu.add_command(label="Keluar", command=keluar_aplikasi)

# Validasi awal saat aplikasi pertama dibuka
validate_form()

window.mainloop()