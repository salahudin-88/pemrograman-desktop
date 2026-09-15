# Mengimpor library tkinter
import tkinter as tk

# Membuat jendela utama
window = tk.Tk()

# Memberikan judul pada jendela
window.title("Form Biodata Mahasiswa")

# Mengatur ukuran jendela (lebar x tinggi)
window.geometry("500x600")

# Mencegah jendela dapat diubah ukurannya
window.resizable(False, False)

# Mengatur warna latar belakang jendela
window.configure(bg="dark goldenrod")
# Membuat frame utama
main_frame = tk.Frame(master=window, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.columnconfigure(1, weight=1)

# Judul menggunakan grid
label_judul = tk.Label(master=main_frame, text="FORM BIODATA MAHASISWA", font=("Arial", 16, "bold"))
label_judul.grid(row=0, column=0, columnspan=2, pady=20)

# Input nama dengan grid
label_nama = tk.Label(master=main_frame, text="Nama Lengkap:", font=("Arial", 12))
label_nama.grid(row=1, column=0, sticky="W", pady=5)

entry_nama = tk.Entry(master=main_frame, width=30, font=("Arial", 12))
entry_nama.grid(row=1, column=1, pady=5)

# Menjalankan event loop
window.mainloop()