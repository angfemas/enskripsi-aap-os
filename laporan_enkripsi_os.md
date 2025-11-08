# Laporan Tugas: Program Enkripsi Sederhana + Integrasi Sistem Operasi

**Nama** : Femas Rendi alfian Salsabila

**Mata Kuliah** : Sistem Operasi

**Dosen** : Hemdani Rahendra Herlianto, S.Kom., M.T.I.

**Tanggal** : November 2025

---

## Kata Pengantar

Puji syukur ke hadirat Allah SWT atas terselesaikannya tugas ini yang berjudul "Program Enkripsi Sederhana + Integrasi Sistem Operasi". Laporan ini disusun untuk memenuhi tugas pada mata kuliah kriptografi. Dalam laporan ini dijelaskan latar belakang, metode implementasi, hasil pengujian, kesimpulan, dan saran terkait pengembangan aplikasi.

Penulis menyadari masih banyak kekurangan pada aplikasi dan laporan ini. Oleh karena itu, kritik dan saran sangat diharapkan untuk perbaikan di masa mendatang.

## Daftar Isi

- Kata Pengantar
- Daftar Isi
- Bab 1: Pendahuluan
  - 1.1 Latar Belakang
  - 1.2 Rumusan Masalah
  - 1.3 Tujuan
- Bab 2: Metode Implementasi
  - 2.1 Desain Sistem
  - 2.2 Deskripsi Algoritma
  - 2.3 Struktur Kode dan Modul
  - 2.4 Dependensi dan Persiapan Lingkungan
  - 2.5 Pengujian
- Bab 3: Hasil dan Pembahasan
  - 3.1 Tampilan Aplikasi
  - 3.2 Contoh Penggunaan
  - 3.3 Catatan Integrasi OS
- Bab 4: Kesimpulan dan Saran
- Daftar Pustaka

---

## Bab 1: Pendahuluan

### 1.1 Latar Belakang

Keamanan data merupakan aspek penting dalam sistem informasi. Salah satu teknik sederhana untuk melindungi isi pesan adalah dengan teknik kriptografi klasik seperti Caesar, Vigenère, dan Transposition. Pada tugas ini dibangun sebuah aplikasi GUI berbasis Python/Tkinter yang menyediakan fungsi enkripsi dan dekripsi menggunakan algoritma tersebut. Selain fungsi kriptografi, aplikasi juga menunjukkan integrasi dasar dengan sistem operasi, seperti membuka/menyimpan file, mengecek penggunaan sumber daya (CPU & memory) menggunakan `psutil`, serta pencatatan (logging) aktivitas pengguna.

### 1.2 Rumusan Masalah

- Bagaimana mengimplementasikan algoritma enkripsi klasik (Caesar, Vigenère, Transposition) dalam Python?
- Bagaimana mengemas fungsi tersebut menjadi aplikasi GUI yang mudah digunakan?
- Bagaimana mengintegrasikan fitur OS (buka/simpan file, cek kinerja, pencatatan aktivitas) secara aman dan portabel?

### 1.3 Tujuan

- Mengimplementasikan tiga algoritma enkripsi klasik.
- Menyediakan antarmuka grafis untuk enkripsi/dekripsi dan operasi file.
- Menambahkan fitur monitoring sistem dan pencatatan aktivitas.
- Menyusun dokumentasi dan melakukan pengujian dasar fungsi.

## Bab 2: Metode Implementasi

### 2.1 Desain Sistem

Aplikasi dibangun sebagai satu modul Python (`enkripsi_app_gui_os.py`) yang mengandung:

- Implementasi fungsi cipher (Caesar, Vigenère, Transposition).
- Fungsi pendukung I/O dan integrasi OS (buka file, simpan file, chmod pada POSIX, cek resource menggunakan `psutil`).
- GUI berbasis Tkinter yang berisi komponen input teks, pilihan algoritma, input kunci, tombol enkripsi/dekripsi, dan area hasil.

Arsitektur sederhana: fungsi-fungsi cipher dan utilitas dipisah dari bagian pembuatan GUI. GUI dibuat di dalam fungsi `main()` dan hanya dipanggil saat modul dijalankan langsung. Ini mempermudah pengujian unit.

### 2.2 Deskripsi Algoritma

- Caesar Cipher

  - Bergeserkan karakter alfabet sebanyak n posisi. Non-alfabet tidak diubah.
  - Implementasi menangani huruf besar/kecil.

- Vigenère Cipher

  - Kunci berbentuk kata; setiap huruf plaintext digeser sesuai huruf pada kunci (A=0, B=1, ...).
  - Implementasi mempertahankan kasus dan mengabaikan non-alfabet saat menerapkan penggeseran namun tetap mempertahankan posisi non-alfabet di teks hasil.

- Transposition Cipher
  - Penyusunan plaintext ke dalam kolom sebanyak k, kemudian membaca secara kolom untuk menghasilkan ciphertext.
  - Implementasi sederhana melakukan pemrosesan berdasarkan ukuran kunci (integer).

### 2.3 Struktur Kode dan Modul

File utama: `enkripsi_app_gui_os.py`

- Fungsi cipher: `caesar_encrypt`, `caesar_decrypt`, `vigenere_encrypt`, `vigenere_decrypt`, `transposition_encrypt`, `transposition_decrypt`.
- Utilitas OS: `open_file`, `save_result`, `show_resource_usage`, `write_log`.
- Pengaturan GUI dan kontrol berada dalam `main()`.
- `write_log` menulis file `log_aktivitas.txt` di folder yang sama dengan file script, menggunakan `getpass.getuser()` untuk mengenali user secara portabel.

Tambahan: `README.md`, `requirements.txt`, dan direktori `tests/` berisi `test_ciphers.py` untuk unit test fungsi cipher.

### 2.4 Dependensi dan Persiapan Lingkungan

- Python 3.8 atau lebih baru.
- Dependensi opsional: `psutil` (untuk mengecek CPU & memory). Daftar dependensi tersedia pada `requirements.txt`.

Langkah singkat setup (Windows PowerShell):

```powershell
pip install -r requirements.txt
python -m unittest discover -v tests
python enkripsi_app_gui_os.py
```

Catatan: apabila `psutil` tidak terpasang, tombol cek kinerja akan menampilkan peringatan instruktif.

### 2.5 Pengujian

- Unit tests (unittest) telah dibuat pada `tests/test_ciphers.py` untuk memverifikasi fungsi cipher bekerja (happy path dan round-trip Vigenère).
- Pengujian manual GUI: buka aplikasi, masukkan teks, pilih algoritma, masukkan key yang sesuai (angka untuk Caesar/Transposition, huruf untuk Vigenère), tekan Enkripsi lalu Simpan.

## Bab 3: Hasil dan Pembahasan

### 3.1 Tampilan Aplikasi

Aplikasi memiliki GUI sederhana berukuran tetap 700x600 dengan:

- Dropdown untuk memilih algoritma
- Area teks input
- Input key
- Tombol buka file, simpan hasil, cek kinerja
- Tombol enkripsi dan dekripsi
- Area teks hasil

(Tangkapan layar dapat ditambahkan pada laporan akhir jika diminta.)

### 3.2 Contoh Penggunaan

1. Pilih "Caesar Cipher".
2. Masukkan teks: `HELLO WORLD`.
3. Masukkan key: `3`.
4. Klik `🔒 Enkripsi` → hasil `KHOOR ZRUOG` akan muncul di area hasil.
5. Klik `💾 Simpan Hasil` untuk menyimpan ke file teks.

### 3.3 Catatan Integrasi OS

- Pencatatan aktivitas: setiap operasi enkripsi/dekripsi dicatat ke `log_aktivitas.txt` dengan timestamp, user, mode (ENCRYPT/DECRYPT), nama algoritma, dan jumlah karakter input.
- Pengaturan permission file hanya dicoba pada sistem POSIX; pada Windows aplikasi akan menyimpan tanpa mencoba `chmod`.
- Fitur cek kinerja menggunakan `psutil` bila terpasang. Jika tidak, pengguna diberitahu bagaimana memasangnya.

## Bab 4: Kesimpulan dan Saran

### 4.1 Kesimpulan

- Aplikasi berhasil mengimplementasikan tiga algoritma kriptografi klasik dan menyediakan GUI yang mudah digunakan.
- Integrasi dasar dengan sistem operasi (I/O file, logging, resource check) telah diimplementasikan dengan pendekatan yang lebih portabel.
- Unit test sederhana memastikan fungsi cipher berfungsi pada skenario dasar.

### 4.2 Saran

- Tambahkan validasi lebih lengkap dan penanganan error untuk teks sangat panjang atau input kunci yang tidak valid.
- Perluasan suite pengujian untuk kasus batas (empty string, non-alphabet only, kunci panjang vs pendek).
- Tambahkan enkripsi modern (AES) bila perlu keamanan nyata—tetapi dengan penanganan kunci dan dependensi yang tepat.
- Gunakan modul `logging` dengan rotasi file (RotatingFileHandler) untuk pengelolaan log yang lebih baik.
- Untuk distribusi ke pengguna non-teknis, kemas aplikasi menjadi executable (mis. dengan PyInstaller) dan berikan installer yang sesuai.

## Daftar Pustaka

1. Stallings, W. (2017). Cryptography and Network Security: Principles and Practice. (Dasar-dasar kriptografi klasik disederhanakan untuk tugas ini.)
2. Python Software Foundation. Python Documentation — https://docs.python.org/3/
3. psutil documentation — https://psutil.readthedocs.io/
4. Tkinter (Tk) documentation and tutorials — https://docs.python.org/3/library/tkinter.html
5. Schneier, B. (1996). Applied Cryptography: Protocols, Algorithms, and Source Code in C. (Referensi umum kriptografi)

---

### Lampiran: File penting di repository

- `enkripsi_app_gui_os.py` — source code aplikasi
- `README.md` — petunjuk singkat menjalankan aplikasi
- `requirements.txt` — dependensi (psutil)
- `tests/test_ciphers.py` — unit tests untuk fungsi cipher
- `log_aktivitas.txt` — contoh log aktivitas (dihasilkan oleh aplikasi)
