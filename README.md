# MountainGo Bromo Trip

MountainGo adalah landing page dan sistem pemesanan trip wisata ke Bromo yang dibuat dalam satu file HTML. Website ini memungkinkan pengunjung melihat paket wisata, memilih destinasi, mengisi formulir booking, mengunggah bukti pembayaran, serta mengelola pesanan melalui dashboard admin.

## Fitur Utama

- Tampilan landing page yang menarik untuk wisata Bromo
- Daftar paket trip dengan harga dan fasilitas
- Informasi destinasi wisata populer di Bromo
- Form pemesanan dengan validasi input
- Upload bukti pembayaran dalam format gambar
- Halaman admin untuk melihat daftar booking
- Fitur ubah status pesanan, hapus pesanan, dan ekspor ke Excel
- Dukungan penyimpanan lokal, cloud, atau server (Google Apps Script)

## Struktur File

- `gomountain.html` — file utama berisi seluruh tampilan, logika booking, dan dashboard admin

## Cara Menjalankan

1. Buka file `gomountain.html` di browser.
2. Jika ingin dijalankan melalui server lokal, gunakan perintah berikut:

```bash
python -m http.server 8000
```

3. Lalu buka alamat:

```text
http://localhost:8000/gomountain.html
```

## Admin

Akun admin untuk Password sama user sesuikan sama yang diinginkan

Untuk membuka halaman admin, buka URL dengan hash `#admin`:

```text
http://localhost:8000/gomountain.html#admin
```

## Catatan Penting

- Website ini menggunakan CDN untuk font dan library Excel.
- Jika ingin data booking tersimpan secara sinkron antar perangkat, Anda bisa menghubungkan ke Google Apps Script dengan mengedit nilai `API_URL` di dalam file `gomountain.html`.
- Jika tidak diatur, sistem akan memakai localStorage pada browser pengguna.

## Teknologi yang Digunakan

- HTML
- CSS
- JavaScript
- SheetJS untuk ekspor Excel

## Penulis

Proyek ini dibuat untuk kebutuhan promosi dan pemesanan trip wisata MountainGo Bromo.
