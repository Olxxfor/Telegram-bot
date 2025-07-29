# 🤖 Bot Telegram Konversi TXT/VCF/XLS

Bot Telegram yang sederhana dan fokus untuk konversi file antara format **TXT**, **VCF**, dan **XLS**.

## ✅ Status Bot
- **Bot Name**: EliteConvertVip🔱
- **Username**: @EliteConvertVip_bot
- **Status**: ✅ RUNNING 
- **Admin ID**: 8141075788

## 📝 Format yang Didukung

### Input ➡️ Output
- **TXT** → VCF, XLS, XLSX, CSV
- **VCF** → TXT, XLS, XLSX, CSV  
- **XLS/XLSX** → TXT, VCF, CSV
- **CSV** → TXT, VCF, XLS, XLSX

## 🎯 Cara Penggunaan

1. **Start Bot**: Kirim `/start` ke @EliteConvertVip_bot
2. **Upload File**: Kirim file TXT/VCF/XLS yang ingin dikonversi
3. **Pilih Format**: Bot akan menampilkan pilihan format tujuan
4. **Download**: File hasil konversi akan dikirim otomatis

## 💡 Contoh Konversi

### TXT → VCF
**Input (contacts.txt):**
```
John Doe
Jane Smith
Bob Wilson
```

**Output (contacts.vcf):**
```
BEGIN:VCARD
VERSION:3.0
FN:John Doe
N:John Doe;;;;
END:VCARD

BEGIN:VCARD
VERSION:3.0
FN:Jane Smith
N:Jane Smith;;;;
END:VCARD
```

### VCF → XLS
- VCF contacts dikonversi ke Excel spreadsheet
- Kolom: Name, Phone, Email

### XLS → TXT
- Data Excel dikonversi ke text list
- Setiap baris = satu line text

## 🔧 Management Bot

### Scripts Tersedia:
```bash
# Status bot
./manage_focused_bot.sh status

# Start bot
./manage_focused_bot.sh start

# Stop bot  
./manage_focused_bot.sh stop

# Restart bot
./manage_focused_bot.sh restart

# Lihat log
./manage_focused_bot.sh log
```

## 📊 Fitur

### ✅ Yang Didukung:
- Konversi TXT ↔ VCF ↔ XLS ↔ CSV
- File size maksimal: 20MB
- Auto-detect format file
- Interface Indonesia
- Statistik pengguna
- Admin panel
- Error handling

### ❌ Yang Tidak Didukung:
- Gambar (JPG, PNG, dll)
- Video/Audio
- PDF
- Dokumen Word
- Arsip (ZIP, RAR, dll)

## 🛠️ Technical Details

### Dependencies:
- `python-telegram-bot` - Telegram bot framework
- `pandas` - Data processing untuk Excel/CSV
- `openpyxl` - Excel file handling
- `python-dotenv` - Environment variables

### File Structure:
```
/workspace/
├── .env                    # Bot configuration
├── focused_bot.py         # Main bot file  
├── requirements_focused.txt # Dependencies
├── manage_focused_bot.sh  # Management script
├── focused_bot.log        # Bot logs
└── temp_* files           # Temporary conversion files
```

## ⚙️ Configuration

### Environment Variables (.env):
```bash
BOT_TOKEN=7882343563:AAGbil4zOXtmQtN5GitqzFbMBSEpwWkTpdY
ADMIN_USER_ID=8141075788
```

## 📈 Stats & Monitoring

### User Statistics:
- Total conversions per user
- Last conversion type
- Global usage statistics

### Admin Commands:
- `/admin` - Admin panel
- Statistics tracking
- User management

## 🔒 Security Features

- File size limits (20MB)
- Format validation
- Temporary file cleanup
- Admin-only commands
- Error logging

## 🚀 Quick Start

1. **Pastikan bot running:**
   ```bash
   ./manage_focused_bot.sh status
   ```

2. **Jika bot tidak running:**
   ```bash
   ./manage_focused_bot.sh start
   ```

3. **Test bot:**
   - Buka Telegram
   - Cari @EliteConvertVip_bot
   - Kirim `/start`
   - Upload file TXT/VCF/XLS

## 📞 Support

- **Admin ID**: 8141075788
- **Bot Username**: @EliteConvertVip_bot
- **Log Location**: `focused_bot.log`

---

## 🎉 Ringkasan

Bot Telegram untuk konversi file **TXT/VCF/XLS** telah berhasil dikonfigurasi dan berjalan dengan fitur:

✅ **Konversi 5 format**: TXT, VCF, XLS, XLSX, CSV  
✅ **Interface Indonesia** yang user-friendly  
✅ **Auto-detection** format file  
✅ **Management scripts** untuk administrasi  
✅ **Admin panel** dengan statistik  
✅ **Error handling** yang robust  

Bot siap digunakan untuk konversi file secara real-time melalui Telegram! 🚀