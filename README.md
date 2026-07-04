# AI Daily Activity Planner - Kelompok Schedulix (ITH)

Aplikasi penjadwalan aktivitas harian mahasiswa bebas konflik waktu (anti-bentrok) yang menerapkan metode **Constraint Satisfaction Problem (CSP)** dan algoritma **Backtracking Search**. Proyek ini dibuat sebagai syarat kelulusan tugas akhir mata kuliah Kecerdasan Buatan di Program Studi Ilmu Komputer, Institut Teknologi Bacharuddin Jusuf Habibie (ITH).

---

## ✨ Fitur Utama

1.  **Dua Modul Solver**:
    *   **`python-constraint`**: Menggunakan pustaka standar Python untuk menyelesaikan CSP secara instan.
    *   **Backtracking Solver Kustom**: Solver yang ditulis khusus untuk mencatat setiap langkah keputusan variabel, uji konsistensi, bentrokan, dan langkah mundur (*backtrack*).
2.  **Simulator Alur Backtracking (Edukasi)**:
    *   Kontrol navigasi lengkap: **Play, Pause, Kembali, Lanjut**, dan Slider Langkah.
    *   Menampilkan visualisasi jadwal sementara secara dinamis pada setiap langkah pencarian.
3.  **Preset Kasus Pengujian Laporan**:
    *   **Kasus Ideal (Beban Ringan)**: Jadwal kuliah dan belajar santai, tersusun kurang dari 0.5 detik.
    *   **Kasus Konflik (Beban Padat)**: Mendeteksi bentrokan rapat dengan kuliah tetap, otomatis menggeser rapat ke sore hari.
    *   **Kasus Pelanggaran Aturan**: Memaksa belajar mandiri di jam istirahat siang (12.00) ditolak sistem karena melanggar batasan keras.
4.  **Tab Landasan Teori CSP**:
    *   Secara interaktif menjabarkan representasi formal matematika dari Variabel ($V$), Domain ($D$), dan Batasan ($C$) berdasarkan data aktivitas yang Anda inputkan secara real-time.
5.  **Desain Premium**:
    *   Antarmuka modern dengan font premium (Plus Jakarta Sans), pewarnaan berkode warna per kategori, dan tampilan kartu responsif.

---

## 🛠️ Panduan Instalasi & Menjalankan Aplikasi

Pastikan Anda telah memasang **Python 3.10** ke atas di sistem Anda.

### 1. Masuk ke Direktori Proyek
Buka terminal (Command Prompt / PowerShell / Git Bash) di direktori ini:
```bash
cd "d:\AI Daily Activity Planner"
```

### 2. Instal Dependensi Pustaka
Instal pustaka yang dibutuhkan menggunakan pip:
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
Jalankan server pengembangan Streamlit:
```bash
streamlit run app.py
```

Setelah perintah di atas dijalankan, peramban (browser) Anda akan otomatis membuka halaman aplikasi di alamat lokal:
`http://localhost:8501`

---

## 👥 Anggota Kelompok (Schedulix - Kelas IK24)

1.  **Mutawalli Hasim** (241011054 / IK24B) - Koordinator Proyek, CSP Logic Designer.
2.  **Frisca Apriliya** (241011054 / IK24B) - System Analyst & Dokumentasi.
3.  **Sabila Nur Sakila** (241011079 / IK24B) - UI/UX Designer & Streamlit Frontend.
4.  **Nabila Sakinah** (241011084 / IK24A) - Core CSP Implementation.
5.  **Alfiana Muhsin** (241011086 / IK24A) - Black-box Tester & Quality Assurance.
# AI-Daily-Activity-Planner
