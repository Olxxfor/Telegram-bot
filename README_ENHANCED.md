# 🚀 Enhanced Bot Telegram - TXT/VCF/XLS dengan Custom Features

Bot Telegram yang telah diperbaiki sesuai permintaan dengan fitur **custom TXT to VCF** yang sangat canggih!

## ✅ Status Bot
- **Bot Name**: EliteConvertVip🔱
- **Username**: @EliteConvertVip_bot
- **Status**: ✅ RUNNING (Enhanced Version)
- **Admin ID**: 8141075788

## 🎯 Fitur TXT → VCF Custom (SESUAI PERMINTAAN)

### 📝 **Custom Settings yang Bisa Diatur:**
1. **📁 Nama File**: Contoh `OLXX` → hasil `OLXX_001.vcf`, `OLXX_002.vcf`
2. **👤 Nama Kontak**: Contoh `REXX` → kontak `REXX_2100`, `REXX_2101`
3. **📊 Jumlah per File**: Contoh `50` → setiap file berisi 50 kontak
4. **🔢 Nomor Urutan Mulai**: Contoh `2100` → dimulai dari REXX_2100

### 🎮 **Cara Menggunakan (Step-by-Step):**

1. **Buka bot** @EliteConvertVip_bot di Telegram
2. **Kirim `/start`** untuk memulai
3. **Pilih "🔄 TXT → VCF Custom"**
4. **Upload file TXT** Anda
5. **Masukan nama file**: `OLXX` (tanpa .vcf)
6. **Masukan nama kontak**: `REXX` 
7. **Sebutkan mau dibagi berapa per file**: `50`
8. **Mulai dari urutan berapa**: `2100`
9. **Bot akan otomatis membuat file VCF** sesuai setting!

### 💡 **Contoh Real (Persis Seperti Permintaan):**

#### Input User:
```
📝 Nama file: OLXX
👤 Nama kontak: REXX  
📊 Per file: 50
🔢 Mulai dari: 2100
```

#### Output Bot:
```
📂 File hasil:
- OLXX_001.vcf (kontak 1-50: REXX_2100 sampai REXX_2149)
- OLXX_002.vcf (kontak 51-100: REXX_2150 sampai REXX_2199)
- OLXX_003.vcf (kontak 101-150: REXX_2200 sampai REXX_2249)
- dst...
```

#### Isi VCF File:
```
BEGIN:VCARD
VERSION:3.0
FN:REXX_2100
N:REXX_2100;;;;
TEL:081234567890
EMAIL:john@email.com
NOTE:Original: John Doe
END:VCARD

BEGIN:VCARD
VERSION:3.0
FN:REXX_2101
N:REXX_2101;;;;
TEL:087654321
EMAIL:jane@email.com
NOTE:Original: Jane Smith
END:VCARD
```

## 🔄 **Fitur Lainnya:**

### 📞 **VCF → TXT**
- Konversi kontak VCF ke text list
- Format: `Nama - Phone - Email`

### 📊 **XLS → VCF** 
- Konversi Excel ke kontak VCF
- Kolom 1: Nama, 2: Phone, 3: Email

### 🔄 **Konversi Biasa**
- Konversi standar tanpa custom settings

## 🛠️ **Management Commands**

```bash
# Status bot
./manage_enhanced_bot.sh status

# Lihat demo fitur custom
./manage_enhanced_bot.sh demo

# Test functionality 
./manage_enhanced_bot.sh test

# Start/stop/restart
./manage_enhanced_bot.sh start|stop|restart
```

## 📋 **Format Input TXT**

Bot mendukung berbagai format input TXT:

```
# Format 1: Nama saja
John Doe
Jane Smith

# Format 2: Nama + Phone
John Doe - 081234567890
Jane Smith - 087654321

# Format 3: Nama + Phone + Email  
John Doe - 081234567890 - john@email.com
Jane Smith - 087654321 - jane@email.com
```

## 🎯 **Custom Features Detail**

### 📁 **Custom Nama File**
- Input: `OLXX` 
- Output: `OLXX_001.vcf`, `OLXX_002.vcf`, `OLXX_003.vcf`
- Pattern: `{nama}_{nomor:03d}.vcf`

### 👤 **Custom Nama Kontak**
- Input: `REXX`
- Output: `REXX_2100`, `REXX_2101`, `REXX_2102`
- Pattern: `{prefix}_{urutan:04d}`

### 📊 **Custom Split File**
- Input: `50` kontak per file
- Bot otomatis split sesuai jumlah
- File dinomori urut: 001, 002, 003

### 🔢 **Custom Nomor Urutan**
- Input: `2100` (mulai dari nomor ini)
- Kontak pertama: `REXX_2100`
- Kontak kedua: `REXX_2101`  
- Berurutan tanpa putus

## 🔒 **Keamanan & Limits**

- **File Size**: Max 20MB per file
- **Formats**: TXT, VCF, XLS, XLSX, CSV
- **Processing**: Auto cleanup temporary files
- **Validation**: Input validation untuk semua custom settings
- **Error Handling**: Comprehensive error messages

## 📊 **Statistics & Monitoring**

### User Statistics
- Total konversi per user
- Mode yang sering digunakan
- Custom settings history

### Admin Features  
- Global usage monitoring
- Error tracking
- Performance metrics

## 🚀 **Technical Implementation**

### Enhanced Features
```python
class UserSession:
    - current_action: "txt_vcf_custom"
    - current_step: "input_filename|input_contactname|input_perfile|input_startnum"
    - custom_settings: {
        'filename': 'OLXX',
        'contactname': 'REXX', 
        'perfile': 50,
        'startnum': 2100
      }
```

### Conversion Logic
```python
async def convert_txt_to_vcf_custom(source_path, filename_prefix, contact_prefix, per_file, start_num):
    # 1. Read TXT file
    # 2. Split into chunks by per_file
    # 3. Generate VCF files with custom naming
    # 4. Sequential numbering from start_num
    # 5. Return list of generated files
```

## 📱 **User Experience**

### Step-by-Step Wizard
1. ✅ **Upload file** → Bot deteksi format
2. ✅ **Input nama file** → Validasi nama
3. ✅ **Input nama kontak** → Validasi prefix  
4. ✅ **Input per file** → Validasi range 1-1000
5. ✅ **Input nomor urutan** → Validasi range 1-999999
6. ✅ **Show summary** → Konfirmasi settings
7. ✅ **Process & send** → Download hasil

### Error Handling
- ❌ Invalid filename → Clear error message
- ❌ Invalid contact name → Validation hint
- ❌ Invalid numbers → Range information
- ❌ File too large → Size limit info

## 🎉 **BERHASIL SESUAI PERMINTAAN!**

Bot Enhanced telah **berhasil diimplementasi persis** sesuai permintaan Anda:

### ✅ **Fitur yang Diminta:**
1. ✅ **Masukan nama file: OLXX** ✓
2. ✅ **Masukan nama kontak: REXX** ✓
3. ✅ **Sebutkan mau dibagi berapa per file: 50** ✓
4. ✅ **Mulai dari urutan berapa: 2100** ✓
5. ✅ **Bot membuat file VCF dengan setting tersebut** ✓

### 🎯 **Hasil Sesuai Ekspektasi:**
- **File**: `OLXX_001.vcf`, `OLXX_002.vcf`, dst
- **Kontak**: `REXX_2100`, `REXX_2101`, `REXX_2102`, dst  
- **Split**: 50 kontak per file
- **Sequential**: Nomor urut berkesinambungan
- **Original**: Data asli tersimpan di NOTE field

## 📞 **Ready to Use!**

**Bot @EliteConvertVip_bot** sudah siap dengan fitur TXT → VCF Custom yang **100% sesuai permintaan Anda!**

🚀 **Silakan dicoba langsung di Telegram!** 🚀