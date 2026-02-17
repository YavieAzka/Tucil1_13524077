
# Tucil1_[NIM] - Queens Game Solver

## a. Deskripsi Singkat Program
Program ini adalah penyelesai otomatis (solver) untuk permainan logika **Queens** yang terdapat pada platform LinkedIn. Tujuan dari permainan ini adalah menempatkan tepat satu ratu (queen) di setiap baris, kolom, dan daerah warna pada papan persegi tanpa ada dua ratu yang saling bersebelahan (termasuk secara diagonal).

Program ini mengimplementasikan algoritma **Brute Force murni** menggunakan bahasa **C++** untuk mencari solusi penempatan ratu secara komprehensif. Selain itu, program ini dilengkapi dengan antarmuka grafis (**GUI**) interaktif berbasis **Python (PyQt6)** yang memungkinkan pengguna untuk merancang papan secara visual, melihat proses iterasi secara *live*, dan mendapatkan *output* solusi dengan mudah. Program juga dilengkapi fitur *toggle* optimasi (heuristik) pada GUI untuk mempercepat waktu pencarian.

## b. Requirement Program dan Instalasi
Untuk dapat melakukan kompilasi dan menjalankan program dengan antarmuka GUI, pastikan sistem Anda memiliki lingkungan berikut:
1. **C++ Compiler**: GCC (g++) atau compiler C++ lainnya yang mendukung standar C++11 ke atas.
2. **Python 3.x**: Lingkungan Python untuk menjalankan GUI.
3. **PyQt6**: Library GUI untuk Python.
   Cara instalasi:
   ```
   pip install PyQt6


## c. Cara Mengkompilasi Program (Opsional)

*(Catatan: Seluruh program yang terdapat di repository ini sudah dicompile, sehingga step ini bisa di-skip).* Program utama (solver C++) perlu dikompilasi sebelum GUI dapat digunakan. Buka terminal/Command Prompt pada direktori *root* repositori ini, lalu jalankan perintah kompilasi berikut:

**Untuk Windows:**

```bash
g++ src/solver.cpp -o bin/solver.exe

```

**Untuk Linux/macOS:**

```bash
g++ src/solver.cpp -o bin/solver

```

*(Catatan: Pastikan nama file output adalah `solver` atau `solver.exe` dan diletakkan di dalam folder `bin` agar dapat dideteksi oleh aplikasi GUI).*

## d. Cara Menjalankan dan Menggunakan Program

### Menjalankan via GUI

1. Buka terminal pada direktori *root* repositori.
2. Jalankan skrip Python GUI:
```
 python main.py
```
Atau jika anda mendownload/meng-clone repository ini, cukup klik dua kali pada aplikasi `QueenSolver.exe`. **Pastikan untuk tidak mengubah struktur folder, karena akan menyebabkan error**.

3. **Cara Penggunaan:**
* **Atur Ukuran:** Tentukan dimensi papan () pada bagian atas.
* **Konfigurasi Input:** Klik tombol warna pada "Palet Warna" di sebelah kiri, lalu warnai kotak-kotak pada tabel "Konfigurasi Input" untuk membentuk *region*. Pastikan *region* dengan warna yang sama saling menyambung.
* **Opsi Load:** Anda juga dapat menggunakan tombol "Load dari TXT" untuk memuat konfigurasi papan dari file berformat `.txt` secara otomatis.
* **Fitur Optimasi:** Centang "Enable Optimization" jika ingin memangkas cabang pencarian yang tidak valid lebih awal, memungkinkan komputasi untuk ukuran papan yang lebih besar
* **SOLVE:** Klik tombol biru "SOLVE" untuk mencari solusi.
* **Lihat Iterasi:** Setelah solusi ditemukan, klik "Lihat Iterasi" untuk melihat jejak langkah penempatan ratu secara visual.





### Menjalankan via CLI tanpa GUI

Jika Anda hanya ingin menjalankan solver C++ tanpa GUI:

1. Siapkan file konfigurasi input dalam format `.txt`  dan letakkan di dalam folder `test/`. (contoh: `test/input.txt`).
2. Jalankan perintah berikut pada terminal di *root* repository (pastikan nama file input sesuai):
```bash
./bin/solver test/input.txt

```


3. Hasil solusi, waktu pencarian, dan jumlah iterasi akan dicetak pada terminal dan disimpan di `test/output.txt`, sementara langkah iterasi akan disimpan pada `test/iteration.txt`

## e. Author

* **Nama:** Yavie Azka Putra Araly
* **NIM:** 13524077
* **Program Studi:** Teknik Informatika
* **Mata Kuliah:** IF2211 Strategi Algoritma
