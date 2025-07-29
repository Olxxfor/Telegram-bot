# 🚀 Bot Telegram Advanced - TXT/VCF/XLS Converter

Bot Telegram canggih untuk konversi file dengan fitur **Rename**, **Merge**, **Split**, dan **Custom Ordering** yang lengkap!

## ✅ Status Bot
- **Bot Name**: EliteConvertVip🔱
- **Username**: @EliteConvertVip_bot
- **Status**: ✅ RUNNING (Advanced Version)
- **Admin ID**: 8141075788

## 🎯 Fitur Utama

### 🔄 Konversi Dasar
- **TXT** → **VCF** (Text ke Kontak)
- **VCF** → **TXT** (Kontak ke Text list)
- **XLS** → **VCF** (Excel ke Kontak)
- **VCF** → **XLS** (Kontak ke Excel)
- **TXT** ↔ **XLS** (Bidirectional)

### 📝 Rename Advanced
- **Rename File**: Custom nama file hasil
- **Rename Kontak**: Ganti nama semua kontak dalam file
- **Auto Numbering**: Customer_001, Customer_002, dst
- **Custom Pattern**: Atur format nama sesuai keinginan
- **Sequential**: Urutan berurutan otomatis

### 🔗 Merge (Gabungkan File)
- **Multiple Files**: Gabung 2+ file TXT/VCF/XLS
- **Custom Order**: Atur urutan penggabungan
- **Remove Duplicates**: Hapus duplikat otomatis
- **Custom Filename**: Nama file hasil sesuai keinginan
- **Mixed Formats**: Gabung berbeda format

### ✂️ Split (Pecah File)
- **Equal Split**: Bagi sama rata (2,3,4,5,10 file)
- **Custom Count**: Atur berapa data per file
- **Custom Range**: Tentukan range data spesifik
- **Quick Split**: Pecah cepat dengan preset
- **Auto Numbering**: File hasil ternomori otomatis

### 🎯 Custom Features
- **Flexible Ordering**: Urutan file sesuai keinginan
- **Custom Naming**: Pattern nama yang fleksibel
- **Batch Processing**: Proses multiple file sekaligus
- **Sequential Numbering**: Penomoran berurutan
- **Format Preservation**: Pertahankan struktur data

## 🎮 Cara Penggunaan

### 1. **Start Bot**
```
/start di @EliteConvertVip_bot
```

### 2. **Pilih Mode**
- 🔄 **Konversi File** - Konversi format dasar
- 📝 **Rename File** - Rename file & kontak
- 🔗 **Gabung File** - Merge multiple files
- ✂️ **Pecah File** - Split file custom

### 3. **Upload & Konfigurasi**
- Upload file sesuai mode yang dipilih
- Ikuti menu step-by-step
- Atur custom settings
- Download hasil

## 💡 Contoh Penggunaan

### 📝 Contoh Rename
**Before:**
```
contacts.txt:
John Doe - 081234567890
Jane Smith - 087654321
```

**After (Auto Numbering):**
```
numbered_contacts.txt:
Customer_001 - 081234567890
Customer_002 - 087654321
```

### 🔗 Contoh Merge
**Input Files:**
- `list1.txt` (100 kontak)
- `list2.txt` (50 kontak)
- `list3.vcf` (75 kontak)

**Result:**
- `merged_contacts.vcf` (225 kontak tanpa duplikat)

### ✂️ Contoh Split
**Input:**
- `big_contacts.vcf` (1000 kontak)

**Split Equal (5 files):**
- `split_01_big_contacts.vcf` (200 kontak)
- `split_02_big_contacts.vcf` (200 kontak)
- `split_03_big_contacts.vcf` (200 kontak)
- `split_04_big_contacts.vcf` (200 kontak)
- `split_05_big_contacts.vcf` (200 kontak)

### 🔄 Contoh Konversi
**TXT → VCF:**
```
Input: contacts.txt
John Doe - 081234567890 - john@email.com
Jane Smith - 087654321 - jane@email.com

Output: contacts.vcf
BEGIN:VCARD
VERSION:3.0
FN:John Doe
N:John Doe;;;;
TEL:081234567890
EMAIL:john@email.com
END:VCARD
...
```

## 🛠️ Management Commands

```bash
# Status lengkap
./manage_advanced_bot.sh status

# Lihat semua fitur
./manage_advanced_bot.sh features

# Start/Stop/Restart
./manage_advanced_bot.sh start|stop|restart

# Test fungsionalitas
./manage_advanced_bot.sh test

# Lihat log
./manage_advanced_bot.sh log
```

## 📋 Format yang Didukung

| Format | Input | Output | Notes |
|--------|-------|--------|-------|
| **TXT** | ✅ | ✅ | Plain text, satu data per baris |
| **VCF** | ✅ | ✅ | vCard format standar |
| **XLS** | ✅ | ✅ | Excel spreadsheet |
| **XLSX** | ✅ | ✅ | Excel modern format |
| **CSV** | ✅ | ✅ | Comma-separated values |

## 🎯 Advanced Settings

### Pattern Naming
- `Customer_[num]` → Customer_001, Customer_002
- `Client_[num]` → Client_001, Client_002
- `Contact_[num]` → Contact_001, Contact_002
- Custom pattern sesuai kebutuhan

### Split Options
- **Equal**: Bagi sama rata
- **Custom Count**: 10,20,30 data per file
- **Custom Range**: File 1 (1-50), File 2 (51-100)
- **Quick**: Auto optimal split

### Merge Options
- **Sequential**: File 1 + File 2 + File 3
- **Custom Order**: File 3 + File 1 + File 2
- **Deduplicate**: Remove duplikat otomatis
- **Mixed Format**: TXT + VCF + XLS → VCF

## 📊 Statistics & Features

### User Statistics
- Total konversi per user
- File yang diproses
- Mode yang sering digunakan
- History aktivitas

### Admin Features
- Monitoring global usage
- User statistics
- Error tracking
- Performance metrics

## 🔒 Security & Limits

- **File Size**: Max 20MB per file
- **Formats**: Hanya TXT/VCF/XLS/XLSX/CSV
- **Processing**: Auto cleanup temporary files
- **Admin Controls**: Restricted admin commands
- **Error Handling**: Comprehensive error catching

## 🚀 Technical Details

### Dependencies
```bash
python-telegram-bot==20.0
pandas>=2.0.0
openpyxl>=3.1.0
python-dotenv==1.0.0
```

### File Structure
```
/workspace/
├── advanced_bot.py          # Main bot dengan semua fitur
├── advanced_handlers.py     # Handlers untuk rename/merge/split
├── manage_advanced_bot.sh   # Management script
├── advanced_bot.log         # Bot logs
├── .env                     # Configuration
└── temp_* files             # Temporary processing files
```

### Architecture
```
AdvancedBot
├── ConversionEngine (TXT/VCF/XLS conversion)
├── RenameHandler (File & contact renaming)
├── MergeHandler (Multiple file merging)
├── SplitHandler (Custom file splitting)
├── SessionManager (User session handling)
└── AdminPanel (Statistics & monitoring)
```

## 📞 Support & Info

- **Bot Username**: @EliteConvertVip_bot
- **Admin ID**: 8141075788
- **Log File**: `advanced_bot.log`
- **Management**: `./manage_advanced_bot.sh`

## 🎉 Kesimpulan

Bot Telegram Advanced TXT/VCF/XLS Converter telah berhasil dikonfigurasi dengan fitur lengkap:

✅ **Konversi**: TXT ↔ VCF ↔ XLS semua arah  
✅ **Rename**: File & kontak dengan auto numbering  
✅ **Merge**: Gabung multiple file dengan custom order  
✅ **Split**: Pecah file dengan pengaturan fleksibel  
✅ **Custom**: Nama, urutan, dan numbering sesuai keinginan  
✅ **Sequential**: Semua hasil berurutan dan terorganisir  

Bot siap untuk penggunaan advanced dengan semua fitur yang diminta! 🚀

---

### 🔥 Fitur Unggulan
- **Custom nama file** sesuai keinginan
- **Custom nama kontak** dengan pattern
- **Gabungkan file** dengan urutan fleksibel
- **Pecah file** dengan jumlah custom
- **Semua berurutan** dan terorganisir
- **Pengaturan fleksibel** untuk semua operasi