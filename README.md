# Program Enkripsi Sederhana + OS Integration

Aplikasi GUI sederhana (Tkinter) untuk enkripsi/dekripsi menggunakan:

- Caesar Cipher
- Vigenère Cipher
- Transposition Cipher

Fitur tambahan:

- Buka / Simpan file teks
- Cek kinerja sistem (menggunakan psutil, opsional)
- Pencatatan aktivitas di `log_aktivitas.txt`

Cara jalankan (Windows):

1. Pastikan Python 3.8+ terpasang.
2. (Opsional) buat virtualenv dan aktifkan.
3. Instal dependensi:

```powershell
pip install -r requirements.txt
```

4. Jalankan aplikasi:

```powershell
python enkripsi_app_gui_os.py
```

Catatan:

- Jika `psutil` tidak terinstal, tombol Cek Kinerja Sistem akan menampilkan pemberitahuan.
- Log aktivitas disimpan di folder yang sama dengan script.
