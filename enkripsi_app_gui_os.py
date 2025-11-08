import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import stat
import getpass
import platform
from pathlib import Path
from datetime import datetime

# psutil is optional: if missing, resource check will notify user
try:
    import psutil
except Exception:
    psutil = None

# ==============================
# FUNGSI-FUNGSI ENKRIPSI
# ==============================


# Caesar Cipher
def caesar_encrypt(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            ciphertext += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            ciphertext += char
    return ciphertext


def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)


# Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key = key.upper()
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            base = 65 if char.isupper() else 97
            ciphertext += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            ciphertext += char
    return ciphertext


def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key = key.upper()
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            base = 65 if char.isupper() else 97
            plaintext += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            plaintext += char
    return plaintext


# Transposition Cipher
def transposition_encrypt(plaintext, key):
    ciphertext = [""] * key
    for col in range(key):
        pointer = col
        while pointer < len(plaintext):
            ciphertext[col] += plaintext[pointer]
            pointer += key
    return "".join(ciphertext)


def transposition_decrypt(ciphertext, key):
    num_cols = key
    num_rows = len(ciphertext) // num_cols
    num_shaded_boxes = (num_cols * num_rows) - len(ciphertext)

    plaintext = [""] * num_rows
    col = 0
    row = 0
    for symbol in ciphertext:
        plaintext[row] += symbol
        row += 1
        if (row == num_rows) or (
            row == num_rows - 1 and col >= num_cols - num_shaded_boxes
        ):
            row = 0
            col += 1
    return "".join(plaintext)


# ==============================
# FUNGSI PENDUKUNG OS
# ==============================


def write_log(algorithm, mode, text):
    """Catat aktivitas user ke log file.

    Uses getpass.getuser() (more portable than os.getlogin()). Writes the
    log file next to this script to avoid surprises when running from
    a different working directory.
    """
    try:
        user = getpass.getuser()
    except Exception:
        user = "unknown"

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = Path(__file__).parent / "log_aktivitas.txt"
    try:
        with log_path.open("a", encoding="utf-8") as log:
            log.write(
                f"[{waktu}] ({user}) - {mode.upper()} menggunakan {algorithm} ({len(text)} karakter)\n"
            )
    except Exception:
        # Avoid crashing the app because logging failed
        pass


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        try:
            data = Path(filepath).read_text(encoding="utf-8")
            entry_text.delete("1.0", tk.END)
            entry_text.insert(tk.END, data)
            messagebox.showinfo(
                "File Dibuka", f"Berhasil membuka: {Path(filepath).name}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka file: {e}")


def save_result():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
    )
    if filepath:
        try:
            Path(filepath).write_text(text_result.get("1.0", tk.END), encoding="utf-8")
            # Only try to set Unix-like permissions on POSIX systems
            if platform.system() != "Windows":
                try:
                    os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR)
                except Exception:
                    pass
            messagebox.showinfo("Disimpan", f"Hasil disimpan di: {Path(filepath).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")


def show_resource_usage():
    if psutil is None:
        messagebox.showwarning(
            "Kinerja Sistem",
            "psutil tidak terinstal. Install dengan: pip install psutil",
        )
        return

    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    messagebox.showinfo("Kinerja Sistem", f"CPU Usage: {cpu}%\nMemory Usage: {mem}%")


# ==============================
# FUNGSI UTAMA ENKRIPSI/DEKRIPSI
# ==============================


def proses(mode):
    algo = combo_algo.get()
    text = entry_text.get("1.0", tk.END).strip()
    key = entry_key.get().strip()

    if not text or not key:
        messagebox.showwarning("Peringatan", "Teks dan Key harus diisi!")
        return

    try:
        if algo == "Caesar Cipher":
            try:
                key_int = int(key)
            except ValueError:
                messagebox.showerror("Error", "Key untuk Caesar harus angka (integer)!")
                return
            result = (
                caesar_encrypt(text, key_int)
                if mode == "encrypt"
                else caesar_decrypt(text, key_int)
            )

        elif algo == "Vigenère Cipher":
            if not key.isalpha():
                messagebox.showerror("Error", "Key untuk Vigenère harus huruf!")
                return
            result = (
                vigenere_encrypt(text, key)
                if mode == "encrypt"
                else vigenere_decrypt(text, key)
            )

        elif algo == "Transposition Cipher":
            try:
                key_int = int(key)
            except ValueError:
                messagebox.showerror(
                    "Error", "Key untuk Transposition harus angka (integer)!"
                )
                return
            result = (
                transposition_encrypt(text, key_int)
                if mode == "encrypt"
                else transposition_decrypt(text, key_int)
            )

        else:
            result = "Algoritma tidak dikenal."

        # tampilkan hasil
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, result)

        # catat log
        write_log(algo, mode, text)

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")


def run_thread(mode):
    """Jalankan proses enkripsi/dekripsi di thread terpisah agar GUI tidak hang"""
    t = threading.Thread(target=lambda: proses(mode))
    t.daemon = True
    t.start()


# ==============================
# GUI TKINTER (dibungkus dalam fungsi main)
# ==============================


def main():
    """Bangun dan jalankan GUI. Dipanggil hanya saat modul dijalankan langsung.

    Memisahkan pembuatan GUI dari definisi fungsi memungkinkan file ini diimport
    oleh unit test tanpa menjalankan jendela Tkinter secara otomatis.
    """

    root = tk.Tk()
    root.title("🔐 Program Enkripsi Terintegrasi OS")
    root.geometry("700x600")
    root.resizable(False, False)

    # Judul
    tk.Label(
        root,
        text="🔐 Program Enkripsi Sederhana + OS Integration",
        font=("Helvetica", 16, "bold"),
    ).pack(pady=10)

    # Frame algoritma
    frame_top = tk.Frame(root)
    frame_top.pack(pady=5)
    tk.Label(frame_top, text="Pilih Algoritma:", font=("Helvetica", 11)).grid(
        row=0, column=0, padx=5
    )
    global combo_algo
    combo_algo = ttk.Combobox(
        frame_top,
        values=["Caesar Cipher", "Vigenère Cipher", "Transposition Cipher"],
        state="readonly",
        width=25,
    )
    combo_algo.current(0)
    combo_algo.grid(row=0, column=1, padx=5)

    # Input teks
    tk.Label(root, text="Masukkan Teks:", font=("Helvetica", 11)).pack()
    global entry_text
    entry_text = tk.Text(root, height=6, width=70)
    entry_text.pack(pady=5)

    # Tombol file
    frame_file = tk.Frame(root)
    frame_file.pack(pady=5)
    tk.Button(frame_file, text="📂 Buka File", width=15, command=open_file).grid(
        row=0, column=0, padx=5
    )
    tk.Button(frame_file, text="💾 Simpan Hasil", width=15, command=save_result).grid(
        row=0, column=1, padx=5
    )
    tk.Button(
        frame_file, text="⚙️ Cek Kinerja Sistem", width=20, command=show_resource_usage
    ).grid(row=0, column=2, padx=5)

    # Input key
    frame_key = tk.Frame(root)
    frame_key.pack(pady=5)
    tk.Label(frame_key, text="Key:", font=("Helvetica", 11)).grid(
        row=0, column=0, padx=5
    )
    global entry_key
    entry_key = tk.Entry(frame_key, width=30)
    entry_key.grid(row=0, column=1, padx=5)

    # Tombol aksi
    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=10)
    tk.Button(
        frame_btn, text="🔒 Enkripsi", width=15, command=lambda: run_thread("encrypt")
    ).grid(row=0, column=0, padx=10)
    tk.Button(
        frame_btn, text="🔓 Dekripsi", width=15, command=lambda: run_thread("decrypt")
    ).grid(row=0, column=1, padx=10)

    # Output hasil
    tk.Label(root, text="Hasil:", font=("Helvetica", 11, "bold")).pack()
    global text_result
    text_result = tk.Text(root, height=6, width=70, fg="blue")
    text_result.pack(pady=5)

    # Footer
    tk.Label(
        root,
        text="© 2025 - Femas Jaya Motor | Integrasi Kriptografi x Sistem Operasi",
        font=("Helvetica", 9, "italic"),
    ).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
