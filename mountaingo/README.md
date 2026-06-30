# MountainGo Bromo Trip 🌋

Website pemesanan trip wisata Gunung Bromo sederhana berbasis **Python Flask**, **HTML**, **CSS**, **JavaScript**, dan **SQLite**. Proyek ini dirancang agar mudah dipahami oleh pemula.

---

## 📁 Struktur Folder Proyek
```text
mountaingo/
├── app.py                # File utama Flask backend & setup database
├── requirements.txt      # Daftar dependensi Python (Flask)
├── database.db           # File database SQLite (dibuat otomatis saat dijalankan)
├── test_app.py           # File unit testing database
├── README.md             # Panduan instalasi dan penggunaan
├── templates/            # Template HTML (Jinja2)
│   ├── base.html         # Layout utama (Navbar, Footer, CSS/JS link)
│   ├── index.html        # Halaman Home
│   ├── paket.html        # Halaman Pilihan Paket Trip
│   ├── detail.html       # Halaman Detail Itinerary & Destinasi
│   ├── booking.html      # Halaman Form Pemesanan & Pop-up Sukses
│   ├── admin.html        # Halaman Dashboard Admin & Pengubah Status
│   ├── about.html        # Halaman Tentang Kami
│   └── contact.html      # Halaman Kontak & Integrasi WhatsApp Chat
└── static/               # File Aset Statis
    ├── css/
    │   └── style.css     # Desain web (Theme Bromo, Grid, Animations, Responsive)
    ├── js/
    │   └── script.js     # Logika menu mobile, auto-select paket, modal popup
    └── images/
        └── bromo.jpg     # Foto Bromo (Premium)
```

---

## 🛠️ Cara Menjalankan Project di VS Code (Windows)

Ikuti langkah-langkah di bawah ini untuk menjalankan proyek di komputer Anda:

### 1. Prasyarat
Pastikan Anda sudah menginstal **Python** (versi 3.8 ke atas disarankan) di laptop/PC Anda.
* Anda bisa mengunduhnya di [python.org](https://www.python.org/downloads/).
* **PENTING**: Saat menginstal Python di Windows, pastikan mencentang opsi **"Add Python to PATH"**.

### 2. Buka Folder Proyek di VS Code
1. Jalankan aplikasi **VS Code**.
2. Klik menu **File** > **Open Folder...** di pojok kiri atas.
3. Arahkan dan pilih folder **`mountaingo`** yang berada di dalam folder workspace Anda (`projectkbta/mountaingo`).
4. Klik **Select Folder**.

### 3. Buka Terminal di VS Code
1. Buka terminal baru dengan menekan tombol kombinasi ``Ctrl + ` `` (Backtick) di keyboard Anda, atau klik menu **Terminal** > **New Terminal** di menu bar atas VS Code.

### 4. Instalasi Dependensi
Ketik perintah berikut di terminal VS Code lalu tekan **Enter** untuk menginstal Flask:
```bash
pip install -r requirements.txt
```
*(Tunggu hingga proses instalasi selesai)*

### 5. Jalankan Aplikasi Flask
Ketik perintah berikut untuk menjalankan server website:
```bash
python app.py
```
Setelah dijalankan, terminal akan memunculkan output seperti ini:
```text
Database berhasil diinisialisasi.
Berhasil menyalin gambar Bromo ke static/images/bromo.jpg
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### 6. Buka Website di Browser
Buka browser favorit Anda (Google Chrome, Microsoft Edge, dll.), lalu masukkan URL berikut di address bar:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Cara Menjalankan Uji Coba Database (Unit Test)
Jika Anda ingin memastikan database SQLite berjalan lancar, terstruktur dengan benar, dan dapat melakukan operasi tambah/ubah status pesanan secara internal, ketik perintah berikut di terminal:
```bash
python test_app.py
```
Output yang sukses akan memunculkan:
```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.045s

OK
```

---

## 🌟 Fitur Utama Proyek
1. **Responsive Navbar & Footer:** Nyaman diakses lewat Smartphone Android/iOS maupun Laptop.
2. **Auto-Select Package:** Memilih paket di halaman **Paket Trip** akan otomatis menyeleksi paket tersebut ketika Anda masuk ke form pemesanan.
3. **Interactive Success Modal:** Setelah booking berhasil dikirim, data otomatis tersimpan di database SQLite dan menampilkan popup modal sukses yang modern.
4. **Interactive Admin Dashboard:** Menampilkan total pesanan, memisahkan statistik berdasarkan status, serta menyediakan formulir update status transaksi yang terintegrasi langsung dengan database.
5. **Direct WhatsApp Chat Integration:** Halaman kontak menyediakan tombol instan untuk mengirim chat langsung ke nomor admin dengan pesan otomatis.
