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

# Input NIM
label_nim = tk.Label(master=window, text="NIM:", font=("Arial", 12))
label_nim.pack(pady=5)
entry_nim = tk.Entry(master=window, width=50)
entry_nim.pack(pady=5)

# Input Jurusan  
label_jurusan = tk.Label(master=window, text="Jurusan:", font=("Arial", 12))
label_jurusan.pack(pady=5)
entry_jurusan = tk.Entry(master=window, width=50)
entry_jurusan.pack(pady=5)

# Menjalankan event loop
window.mainloop()