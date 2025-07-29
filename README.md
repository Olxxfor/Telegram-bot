# Contact Manager System

Sistem manajemen kontak lengkap dengan fitur konversi, pembagian file, dan sistem admin premium.

## Fitur Utama

### 🔄 Konversi File
- **VCF to TXT**: Konversi file VCF ke format TXT
- **XLS to VCF**: Konversi file Excel ke format VCF
- **TXT to VCF**: Konversi file TXT ke format VCF

### 📁 Manajemen File
- **Pecah File**: Membagi file besar menjadi beberapa file kecil
- **Gabungkan File**: Menggabungkan beberapa file menjadi satu
- **Rename File & Kontak**: Mengubah nama file dan kontak di dalamnya

### 🔍 Deteksi & Validasi
- **Deteksi Duplikat**: Otomatis mendeteksi kontak duplikat (Premium)
- **Validasi Format**: Memastikan format file sesuai standar

### 👨‍💼 Sistem Admin
- **Login Admin**: Sistem autentikasi admin
- **Manajemen User Premium**: Tambah, edit, hapus user premium
- **Deteksi Expired**: Otomatis mendeteksi user yang expired
- **Statistik Sistem**: Monitoring penggunaan sistem

## Instalasi

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
Database akan otomatis dibuat saat pertama kali menjalankan aplikasi.

### 3. Login Admin Default
- Username: `admin`
- Password: `admin123`

## Cara Penggunaan

### 1. Menjalankan Contact Manager
```bash
python contact_manager.py
```

### 2. Menjalankan Admin Panel
```bash
python admin_panel.py
```

### 3. Format Pembagian File
Gunakan format: `OLXX-REXX-81-50`
- `OLXX`: Nama kontak (bisa ditambah angka)
- `REXX`: Nama file (bisa ditambah angka)
- `81`: Urutan file mulai
- `50`: Jumlah kontak per file

**Contoh:**
- Input: `OLXX-REXX-81-50`
- Output: 
  - `OLXX-81.vcf` (kontak 1-50)
  - `OLXX-82.vcf` (kontak 51-100)
  - dst.

## Fitur Premium

### Fitur yang Memerlukan Premium:
- Deteksi duplikat otomatis
- Operasi bulk (mass operations)
- Export advanced
- Tidak ada batasan jumlah kontak

### Fitur Free:
- Konversi dasar (VCF ↔ TXT, XLS → VCF)
- Pembagian file (maksimal 1000 kontak)
- Merge file (maksimal 5 file)

## Struktur Database

### Tabel Admin
```sql
CREATE TABLE admins (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT,
    created_date TEXT
);
```

### Tabel Premium Users
```sql
CREATE TABLE premium_users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT,
    premium_expiry TEXT,
    features TEXT,
    created_date TEXT
);
```

## Contoh Penggunaan

### 1. Konversi VCF ke TXT
```
Menu: 2
File VCF: contacts.vcf
Output: contacts.txt
```

### 2. Pembagian File
```
Menu: 4
File input: contacts.txt
Format: OLXX-REXX-81-50
Output: OLXX-81.vcf, OLXX-82.vcf, dst.
```

### 3. Deteksi Duplikat
```
Menu: 7
File: contacts.vcf
Output: 
- Total: 150
- Unique: 145
- Duplicates: 5
```

### 4. Admin - Tambah User Premium
```
Menu: 1
Username: john_doe
Email: john@example.com
Duration: 30
Features: duplicate_detection,bulk_operations
```

## File yang Dihasilkan

### Contact Manager
- `contact_manager.py` - Aplikasi utama
- `contact_manager.db` - Database SQLite
- `config.json` - Konfigurasi sistem

### Admin Panel
- `admin_panel.py` - Panel admin
- `requirements.txt` - Dependencies

## Keamanan

- Password di-hash menggunakan SHA-256
- Validasi input untuk mencegah SQL injection
- Pengecekan permission untuk fitur premium
- Logging aktivitas admin

## Troubleshooting

### Error: "Module not found"
```bash
pip install pandas openpyxl xlrd
```

### Error: "File not found"
Pastikan file yang direferensikan ada di direktori yang sama.

### Error: "Permission denied"
Pastikan folder memiliki permission write.

## Support

Untuk bantuan lebih lanjut, silakan buat issue di repository ini.

## License

MIT License - Silakan gunakan untuk keperluan komersial maupun non-komersial.
