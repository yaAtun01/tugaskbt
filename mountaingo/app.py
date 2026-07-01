import functools
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
# Secret key for flash messages
app.secret_key = 'mountaingo_secret_key'

DATABASE = 'database.db'
ADMIN_PASSWORD = os.environ.get('MOUNTAINGO_ADMIN_PASSWORD', 'admin123')

def get_db_connection():
    """Membuka koneksi ke database SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Mengembalikan hasil sebagai dictionary-like object
    return conn

def init_db():
    """Inisialisasi database dan membuat tabel bookings jika belum ada."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            whatsapp TEXT NOT NULL,
            email TEXT NOT NULL,
            tanggal_trip TEXT NOT NULL,
            jumlah_peserta INTEGER NOT NULL,
            paket TEXT NOT NULL,
            catatan TEXT,
            status TEXT NOT NULL DEFAULT 'Menunggu Konfirmasi'
        )
    ''')
    conn.commit()
    conn.close()
    print("Database berhasil diinisialisasi.")

def copy_placeholder_image():
    """Menyalin gambar bromo_sunrise dari folder artifact ke static/images jika belum ada."""
    target_dir = os.path.join(app.root_path, 'static', 'images')
    target_path = os.path.join(target_dir, 'bromo.jpg')
    
    if not os.path.exists(target_path):
        os.makedirs(target_dir, exist_ok=True)
        # Sumber gambar yang baru dibuat oleh AI
        source_dir = r"C:\Users\atun\.gemini\antigravity-ide\brain\d63c03c8-c854-4a57-857c-362a3d799e30"
        source_path = os.path.join(source_dir, "bromo_sunrise_1782834217975.png")
        
        if os.path.exists(source_path):
            try:
                import shutil
                shutil.copy(source_path, target_path)
                print(f"Berhasil menyalin gambar Bromo ke {target_path}")
            except Exception as e:
                print(f"Gagal menyalin gambar: {e}")
        else:
            print("Gambar sumber bromo_sunrise tidak ditemukan di folder artifact.")


def login_required(view_func):
    @functools.wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return view_func(*args, **kwargs)
    return wrapped_view

# --- ROUTES ---

@app.route('/')
def index():
    """Halaman Home."""
    return render_template('index.html')

@app.route('/paket')
def paket():
    """Halaman Paket Trip."""
    return render_template('paket.html')

@app.route('/detail')
def detail():
    """Halaman Detail Trip (Destinasi & Jadwal)."""
    return render_template('detail.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    """Halaman Form Pemesanan."""
    if request.method == 'POST':
        # Mengambil data dari form
        nama = request.form.get('nama')
        whatsapp = request.form.get('whatsapp')
        email = request.form.get('email')
        tanggal_trip = request.form.get('tanggal_trip')
        jumlah_peserta = request.form.get('jumlah_peserta')
        paket_pilihan = request.form.get('paket')
        catatan = request.form.get('catatan')
        
        # Validasi sederhana
        if not nama or not whatsapp or not email or not tanggal_trip or not jumlah_peserta or not paket_pilihan:
            flash("Semua field wajib diisi!", "error")
            return redirect(url_for('booking'))
        
        try:
            # Menyimpan ke database SQLite
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bookings (nama, whatsapp, email, tanggal_trip, jumlah_peserta, paket, catatan, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Menunggu Konfirmasi')
            ''', (nama, whatsapp, email, tanggal_trip, int(jumlah_peserta), paket_pilihan, catatan))
            conn.commit()
            conn.close()
            
            # Redirect ke halaman booking dengan query parameter sukses
            return redirect(url_for('booking', success=True))
        except Exception as e:
            flash(f"Terjadi kesalahan saat menyimpan data: {e}", "error")
            return redirect(url_for('booking'))
            
    # Ambil paket dari query string jika diarahkan dari halaman paket
    paket_pilihan = request.args.get('paket', '')
    # Cek apakah pemesanan berhasil
    success = request.args.get('success', False)
    
    return render_template('booking.html', paket_pilihan=paket_pilihan, success=success)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin'))

    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Login admin berhasil.', 'success')
            return redirect(url_for('admin'))
        flash('Password admin salah.', 'error')

    return render_template('login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Anda berhasil keluar dari panel admin.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin():
    """Halaman Admin Panel Sederhana."""
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings ORDER BY id DESC').fetchall()
    
    # Menghitung statistik untuk Dashboard Admin
    stats = {
        'total': len(bookings),
        'pending': sum(1 for b in bookings if b['status'] == 'Menunggu Konfirmasi'),
        'confirmed': sum(1 for b in bookings if b['status'] == 'Dikonfirmasi'),
        'done': sum(1 for b in bookings if b['status'] == 'Selesai')
    }
    
    conn.close()
    return render_template('admin.html', bookings=bookings, stats=stats)

@app.route('/admin/update-status', methods=['POST'])
@login_required
def update_status():
    """Route untuk mengubah status pemesanan."""
    booking_id = request.form.get('booking_id')
    status_baru = request.form.get('status')
    
    if booking_id and status_baru:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE bookings SET status = ? WHERE id = ?', (status_baru, booking_id))
            conn.commit()
            conn.close()
            flash("Status pemesanan berhasil diperbarui!", "success")
        except Exception as e:
            flash(f"Gagal memperbarui status: {e}", "error")
            
    return redirect(url_for('admin'))

@app.route('/about')
def about():
    """Halaman Tentang Kami."""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Halaman Kontak Kami."""
    return render_template('contact.html')

if __name__ == '__main__':
    # Inisialisasi database sebelum aplikasi berjalan
    init_db()
    # Salin gambar Bromo ke direktori static jika belum ada
    copy_placeholder_image()
    # Menjalankan aplikasi Flask di port 5000
    app.run(debug=True, host='127.0.0.1', port=5000)
