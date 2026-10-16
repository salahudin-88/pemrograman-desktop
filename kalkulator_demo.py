import tkinter as tk
from typing import Optional


OPERATORS = ("+", "-", "*", "/")


def hitung(angka1: float, operator: str, angka2: float) -> float:
    """Hitung satu operasi aritmetika."""
    if operator == "+":
        return angka1 + angka2
    if operator == "-":
        return angka1 - angka2
    if operator == "*":
        return angka1 * angka2
    if operator == "/":
        if angka2 == 0:
            raise ZeroDivisionError("Tidak dapat membagi dengan nol.")
        return angka1 / angka2
    raise ValueError(f"Operator tidak valid: {operator}")


def kalkulator_prosedural() -> None:
    print("=== KALKULATOR PROSEDURAL ===")
    print("Program berjalan berurutan, user harus mengikuti alur")

    while True:
        try:
            angka1 = float(input("Masukkan angka pertama: "))
            break
        except ValueError:
            print("Input harus berupa angka!")

    while True:
        operator = input("Masukkan operator (+, -, *, /): ")
        if operator in OPERATORS:
            break
        print("Operator tidak valid!")

    while True:
        try:
            angka2 = float(input("Masukkan angka kedua: "))
            break
        except ValueError:
            print("Input harus berupa angka!")

    try:
        hasil = hitung(angka1, operator, angka2)
    except ZeroDivisionError:
        print("Error: Pembagian dengan nol!")
        return

    print(f"Hasil: {angka1} {operator} {angka2} = {hasil}")
    print("Program selesai")


class KalkulatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Kalkulator Demo - Prosedural vs OOP")
        self.configure(bg="#c92828")
        self.geometry("360x440")
        self.minsize(320, 400)

        self.current_input = "0"
        self.nilai_tersimpan: Optional[float] = None
        self.operator_aktif: Optional[str] = None
        self.input_baru = True

        self._buat_tampilan()
        self.bind("<Key>", self._tangani_tombol_keyboard)

    def _buat_tampilan(self) -> None:
        font_button = ("Arial", 16)
        main_frame = tk.Frame(self, bg="#c92828")
        main_frame.pack(expand=True, fill="both", padx=12, pady=12)
        main_frame.columnconfigure(tuple(range(4)), weight=1)
        main_frame.rowconfigure(tuple(range(5)), weight=1)

        self.display = tk.Entry(
            main_frame,
            font=("Arial", 24),
            borderwidth=2,
            relief="solid",
            justify="right",
            state="readonly",
            readonlybackground="white",
        )
        self.display.grid(
            row=0, column=0, columnspan=4, sticky="nsew", padx=4, pady=8
        )

        tombol = (
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("+", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("*", 3, 3),
            ("AC", 4, 0), ("0", 4, 1), (".", 4, 2), ("/", 4, 3),
        )
        for label, row, column in tombol:
            if label in OPERATORS:
                command = lambda op=label: self.pilih_operator(op)
            elif label == "AC":
                command = self.bersihkan
            elif label == "DEL":
                command = self.hapus_digit
            elif label == ".":
                command = self.tambah_desimal
            else:
                command = lambda digit=label: self.tambah_angka(digit)

            tk.Button(
                main_frame,
                text=label,
                font=font_button,
                command=command,
            ).grid(row=row, column=column, sticky="nsew", padx=3, pady=3)

        tk.Button(
            main_frame,
            text="DEL",
            font=font_button,
            command=self.hapus_digit,
        ).grid(row=5, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)
        tk.Button(
            main_frame,
            text="=",
            font=font_button,
            command=self.hitung_hasil,
        ).grid(row=5, column=2, columnspan=2, sticky="nsew", padx=3, pady=3)
        main_frame.rowconfigure(5, weight=1)
        self._perbarui_display()

    def _perbarui_display(self) -> None:
        self.display.configure(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)
        self.display.configure(state="readonly")

    def tambah_angka(self, angka: str) -> None:
        if self.input_baru or self.current_input == "Error":
            self.current_input = angka
            self.input_baru = False
        elif self.current_input == "0":
            self.current_input = angka
        else:
            self.current_input += angka
        self._perbarui_display()

    def tambah_desimal(self) -> None:
        if self.input_baru or self.current_input == "Error":
            self.current_input = "0."
            self.input_baru = False
        elif "." not in self.current_input:
            self.current_input += "."
        self._perbarui_display()

    def pilih_operator(self, operator: str) -> None:
        if self.current_input == "Error":
            return
        try:
            nilai_sekarang = float(self.current_input)
            if self.nilai_tersimpan is not None and self.operator_aktif:
                if not self.input_baru:
                    nilai_sekarang = hitung(
                        self.nilai_tersimpan, self.operator_aktif, nilai_sekarang
                    )
                    self.current_input = self._format_hasil(nilai_sekarang)
                    self._perbarui_display()
            self.nilai_tersimpan = nilai_sekarang
            self.operator_aktif = operator
            self.input_baru = True
        except ZeroDivisionError:
            self._tampilkan_error()

    def hitung_hasil(self) -> None:
        if (
            self.nilai_tersimpan is None
            or self.operator_aktif is None
            or self.input_baru
        ):
            return
        try:
            hasil = hitung(
                self.nilai_tersimpan,
                self.operator_aktif,
                float(self.current_input),
            )
        except ZeroDivisionError:
            self._tampilkan_error()
            return

        self.current_input = self._format_hasil(hasil)
        self.nilai_tersimpan = None
        self.operator_aktif = None
        self.input_baru = True
        self._perbarui_display()

    @staticmethod
    def _format_hasil(hasil: float) -> str:
        return format(hasil, ".12g")

    def _tampilkan_error(self) -> None:
        self.current_input = "Error"
        self.nilai_tersimpan = None
        self.operator_aktif = None
        self.input_baru = True
        self._perbarui_display()

    def bersihkan(self) -> None:
        self.current_input = "0"
        self.nilai_tersimpan = None
        self.operator_aktif = None
        self.input_baru = True
        self._perbarui_display()

    def hapus_digit(self) -> None:
        if self.current_input == "Error":
            self.bersihkan()
            return
        self.current_input = self.current_input[:-1] or "0"
        if self.current_input in ("", "-"):
            self.current_input = "0"
        self.input_baru = False
        self._perbarui_display()

    def _tangani_tombol_keyboard(self, event: tk.Event) -> None:
        karakter = event.char
        if karakter.isdigit():
            self.tambah_angka(karakter)
        elif karakter == ".":
            self.tambah_desimal()
        elif karakter in OPERATORS:
            self.pilih_operator(karakter)
        elif karakter == "=" or event.keysym == "Return":
            self.hitung_hasil()
        elif event.keysym == "Escape":
            self.bersihkan()
        elif event.keysym == "BackSpace":
            self.hapus_digit()


if __name__ == "__main__":
    KalkulatorApp().mainloop()
