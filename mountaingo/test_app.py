import os
import sqlite3
import unittest
from app import init_db, get_db_connection, DATABASE

class TestMountainGoApp(unittest.TestCase):

    def setUp(self):
        """Set up environment sebelum menjalankan test."""
        # Menghapus database lama jika ada agar bersih
        if os.path.exists(DATABASE):
            try:
                os.remove(DATABASE)
            except OSError:
                pass
        init_db()

    def tearDown(self):
        """Clean up setelah test selesai."""
        if os.path.exists(DATABASE):
            try:
                os.remove(DATABASE)
            except OSError:
                pass

    def test_database_creation(self):
        """Memverifikasi bahwa database dan tabel bookings berhasil dibuat."""
        self.assertTrue(os.path.exists(DATABASE), "File database.db harus dibuat.")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Mengecek apakah tabel bookings ada
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings';")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists, "Tabel 'bookings' harus ada di database.")
        
        # Mengecek kolom-kolom tabel
        cursor.execute("PRAGMA table_info(bookings);")
        columns = {col['name']: col['type'] for col in cursor.fetchall()}
        
        expected_columns = {
            'id': 'INTEGER',
            'nama': 'TEXT',
            'whatsapp': 'TEXT',
            'email': 'TEXT',
            'tanggal_trip': 'TEXT',
            'jumlah_peserta': 'INTEGER',
            'paket': 'TEXT',
            'catatan': 'TEXT',
            'status': 'TEXT'
        }
        
        for col_name, col_type in expected_columns.items():
            self.assertIn(col_name, columns, f"Kolom '{col_name}' harus ada.")
            self.assertEqual(columns[col_name], col_type, f"Kolom '{col_name}' harus bertipe {col_type}.")
            
        conn.close()

    def test_booking_insertion(self):
        """Memverifikasi bahwa data booking bisa dimasukkan dengan status default."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Input data testing
        cursor.execute('''
            INSERT INTO bookings (nama, whatsapp, email, tanggal_trip, jumlah_peserta, paket, catatan)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ("Budi Pekerti", "081299998888", "budi@example.com", "2026-08-17", 4, "Private", "Butuh penjemputan di hotel"))
        conn.commit()
        
        # Ambil data yang dimasukkan
        cursor.execute("SELECT * FROM bookings WHERE nama = ?", ("Budi Pekerti",))
        booking = cursor.fetchone()
        
        self.assertIsNotNone(booking, "Data booking harus berhasil disimpan.")
        self.assertEqual(booking['whatsapp'], "081299998888")
        self.assertEqual(booking['email'], "budi@example.com")
        self.assertEqual(booking['tanggal_trip'], "2026-08-17")
        self.assertEqual(booking['jumlah_peserta'], 4)
        self.assertEqual(booking['paket'], "Private")
        self.assertEqual(booking['catatan'], "Butuh penjemputan di hotel")
        self.assertEqual(booking['status'], "Menunggu Konfirmasi", "Status default harus 'Menunggu Konfirmasi'.")
        
        conn.close()

    def test_status_update(self):
        """Memverifikasi bahwa status pemesanan dapat diperbarui."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Masukkan data testing awal
        cursor.execute('''
            INSERT INTO bookings (nama, whatsapp, email, tanggal_trip, jumlah_peserta, paket)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ("Siti Aminah", "085711112222", "siti@example.com", "2026-09-01", 2, "Reguler"))
        booking_id = cursor.lastrowid
        conn.commit()
        
        # Update status ke Dikonfirmasi
        cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", ("Dikonfirmasi", booking_id))
        conn.commit()
        
        # Ambil data setelah update
        cursor.execute("SELECT status FROM bookings WHERE id = ?", (booking_id,))
        status_after = cursor.fetchone()['status']
        self.assertEqual(status_after, "Dikonfirmasi", "Status harus diperbarui menjadi 'Dikonfirmasi'.")
        
        # Update status ke Selesai
        cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", ("Selesai", booking_id))
        conn.commit()
        
        cursor.execute("SELECT status FROM bookings WHERE id = ?", (booking_id,))
        status_done = cursor.fetchone()['status']
        self.assertEqual(status_done, "Selesai", "Status harus diperbarui menjadi 'Selesai'.")
        
        conn.close()

if __name__ == '__main__':
    unittest.main()
