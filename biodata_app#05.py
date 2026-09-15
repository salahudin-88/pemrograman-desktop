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

# Membuat label judul
label_judul = tk.Label(
    master=window,
    text="FORM BIODATA MAHASISWA",
    font=("Arial", 16, "bold")
)

# Menampilkan label dengan pack
label_judul.pack(pady=20)


# Menjalankan event loop
window.mainloop()