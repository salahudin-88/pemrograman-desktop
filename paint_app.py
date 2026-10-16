import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog


class PaintApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Paint App - Event Handling Demo")
        self.window.geometry("800x600")

        # Variabel untuk painting
        self.last_x = None
        self.last_y = None
        self.pen_color = "black"
        self.pen_size = 2
        self.is_drawing = False

        # Untuk label posisi mouse
        self.pos_label = None
        self.pos_after_id = None

        self.buat_interface()
        self.bind_events()

    def buat_interface(self):
        # Frame toolbar
        toolbar = tk.Frame(self.window, bg="lightgray", height=50)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        toolbar.pack_propagate(False)

        # Canvas
        self.canvas = tk.Canvas(self.window, bg="white", cursor="pencil")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Tombol pilih warna
        btn_color = tk.Button(
            toolbar,
            text="Pilih Warna",
            command=self.pilih_warna,
            bg="lightblue"
        )
        btn_color.pack(side=tk.LEFT, padx=5, pady=5)

        # Label dan slider ukuran pen
        tk.Label(toolbar, text="Ukuran:", bg="lightgray").pack(side=tk.LEFT, padx=5)

        self.size_var = tk.IntVar(value=2)
        size_scale = tk.Scale(
            toolbar,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            command=self.ubah_ukuran
        )
        size_scale.pack(side=tk.LEFT, padx=5)

        # Tombol clear
        btn_clear = tk.Button(
            toolbar,
            text="Clear",
            command=self.clear_canvas,
            bg="red",
            fg="white"
        )
        btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

        # Label info
        self.info_label = tk.Label(
            toolbar,
            text=f"Warna: {self.pen_color} | Ukuran: {self.pen_size}",
            bg="lightgray"
        )
        self.info_label.pack(side=tk.RIGHT, padx=10)

    def bind_events(self):
        """Binding semua event."""
        # Mouse events untuk menggambar
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Mouse event untuk info posisi
        self.canvas.bind("<Motion>", self.show_position)

        # Keyboard shortcuts
        self.window.bind("<Control-s>", self.save_image)
        self.window.bind("<Control-o>", self.open_image)
        self.window.bind("<Control-n>", self.new_canvas)

        # Window event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def pilih_warna(self):
        """Event handler untuk memilih warna."""
        color = colorchooser.askcolor(title="Pilih Warna Pen")
        if color[1]:
            self.pen_color = color[1]
            self.update_info()

    def ubah_ukuran(self, value):
        """Event handler untuk mengubah ukuran pen."""
        self.pen_size = int(value)
        self.update_info()

    def clear_canvas(self):
        """Event handler untuk membersihkan canvas."""
        if messagebox.askyesno("Konfirmasi", "Hapus semua gambar?"):
            self.canvas.delete("all")

    def update_info(self):
        """Update info di toolbar."""
        self.info_label.config(
            text=f"Warna: {self.pen_color} | Ukuran: {self.pen_size}"
        )

    def start_draw(self, event):
        """Saat mouse ditekan."""
        self.last_x = event.x
        self.last_y = event.y
        self.is_drawing = True

    def draw(self, event):
        """Saat mouse digeser sambil ditekan."""
        if self.is_drawing and self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                width=self.pen_size,
                fill=self.pen_color,
                capstyle=tk.ROUND,
                smooth=True
            )
            self.last_x = event.x
            self.last_y = event.y

    def stop_draw(self, event):
        """Saat mouse dilepas."""
        self.is_drawing = False
        self.last_x = None
        self.last_y = None

    def show_position(self, event):
        """Menampilkan posisi mouse sementara."""
        # Batalkan timer lama
        if self.pos_after_id is not None:
            self.window.after_cancel(self.pos_after_id)
            self.pos_after_id = None

        # Hapus label lama
        if self.pos_label is not None:
            self.pos_label.destroy()

        self.pos_label = tk.Label(
            self.window,
            text=f"Posisi: ({event.x}, {event.y})",
            bg="yellow"
        )

        # Offset y +60 karena ada toolbar di atas
        self.pos_label.place(x=event.x + 10, y=event.y + 60)

        label_ref = self.pos_label

        def hapus_label():
            if self.pos_label is label_ref:
                self.pos_label.destroy()
                self.pos_label = None
            self.pos_after_id = None

        self.pos_after_id = self.window.after(1000, hapus_label)

    def save_image(self, event=None):
        """Ctrl+S untuk menyimpan gambar."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")]
        )
        if filename:
            self.canvas.postscript(file=filename)
            messagebox.showinfo("Info", f"Gambar disimpan sebagai {filename}")

    def open_image(self, event=None):
        """Ctrl+O untuk membuka gambar."""
        messagebox.showinfo("Info", "Fitur buka gambar belum diimplementasi")

    def new_canvas(self, event=None):
        """Ctrl+N untuk canvas baru."""
        if messagebox.askyesno(
            "Canvas Baru",
            "Buat canvas baru? Gambar saat ini akan hilang."
        ):
            self.canvas.delete("all")

    def on_closing(self):
        """Saat jendela akan ditutup."""
        if messagebox.askokcancel(
            "Keluar",
            "Yakin ingin keluar? Gambar yang belum disimpan akan hilang."
        ):
            self.window.destroy()

    def jalankan(self):
        """Menjalankan aplikasi."""
        self.window.mainloop()


if __name__ == "__main__":
    app = PaintApp()
    app.jalankan()