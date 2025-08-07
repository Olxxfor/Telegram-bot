# 🤖 Telegram File Converter Bot

Bot Telegram yang komprehensif untuk mengkonversi berbagai format file dengan mudah dan cepat.

## ✨ Fitur Utama

### 📸 Konversi Gambar
- **Input**: JPG, JPEG, PNG, BMP, GIF, TIFF, WebP, ICO
- **Output**: JPG, PNG, PDF, WebP, BMP, GIF, ICO
- Mempertahankan kualitas gambar original
- Dukungan transparansi untuk PNG
- Konversi batch untuk multiple gambar

### 📄 Konversi Dokumen
- **Input**: TXT, DOCX, PDF, RTF
- **Output**: PDF, TXT, DOCX
- Ekstraksi teks dari PDF
- Konversi dokumen Word ke PDF
- Format teks yang rapi

### 🗜️ Pengelolaan Arsip
- **Input**: ZIP, RAR, 7Z, TAR, GZ
- **Output**: ZIP (ekstraksi otomatis)
- Ekstraksi file arsip
- Kompres multiple file ke ZIP

### 🎥 Konversi Video
- **Input**: MP4, AVI, MKV, MOV, WMV, FLV, WebM
- **Output**: MP4, AVI, GIF, WebM
- Konversi video ke GIF animasi
- Optimasi ukuran file
- Dukungan berbagai codec

### 🎵 Konversi Audio
- **Input**: MP3, WAV, OGG, AAC, FLAC, M4A, WMA
- **Output**: MP3, WAV, OGG, AAC
- Konversi format audio populer
- Pengaturan bitrate dan sample rate
- Kompresi audio lossless/lossy

## 🚀 Instalasi Cepat

### 1. Clone Repository
```bash
git clone https://github.com/username/telegram-file-converter-bot.git
cd telegram-file-converter-bot
```

### 2. Jalankan Setup Script (Recommended)
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Manual Setup
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip ffmpeg unrar p7zip-full

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 4. Konfigurasi Bot Token
1. Buat bot baru di [@BotFather](https://t.me/BotFather)
2. Dapatkan token bot Anda
3. Edit file `.env`:
```bash
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

### 5. Jalankan Bot
```bash
# Menggunakan startup script
./start_bot.sh

# Atau manual
source venv/bin/activate
python bot.py
```

## 📋 Requirements

### System Requirements
- **OS**: Linux, Ubuntu 18.04+ (Recommended)
- **Python**: 3.8 atau lebih tinggi
- **RAM**: Minimal 512MB (1GB+ recommended)
- **Storage**: 1GB free space untuk temporary files
- **Network**: Koneksi internet stabil

### Dependencies
- `python-telegram-bot>=20.7`: Framework bot Telegram
- `Pillow>=10.1.0`: Image processing
- `PyPDF2>=3.0.1`: PDF manipulation
- `reportlab>=4.0.7`: PDF generation
- `python-docx>=1.1.0`: Word document processing
- `rarfile>=4.1`: RAR archive support
- `ffmpeg`: Video/audio conversion (system package)

## 🎯 Cara Penggunaan

### Perintah Bot
- `/start` - Memulai bot dan menampilkan menu utama
- `/help` - Panduan lengkap penggunaan bot
- `/formats` - Daftar format file yang didukung
- `/stats` - Statistik penggunaan personal

### Langkah Konversi
1. **Kirim File**: Upload file yang ingin dikonversi
2. **Pilih Format**: Bot akan menampilkan opsi konversi yang tersedia
3. **Tunggu Proses**: Bot akan memproses file Anda
4. **Download**: Unduh file hasil konversi

### Batasan
- **Ukuran File**: Maksimal 50MB per file
- **Waktu Konversi**: Maksimal 5 menit per file
- **Rate Limit**: 10 konversi per jam, 50 per hari
- **Concurrent**: Maksimal 3 konversi bersamaan

## ⚙️ Konfigurasi

### Environment Variables
```bash
# Required
BOT_TOKEN=your_telegram_bot_token

# Optional
ADMIN_USER_ID=your_telegram_user_id
MAX_FILE_SIZE=52428800
LOG_LEVEL=INFO
```

### config.py
Customize bot behavior dengan mengedit `config.py`:
- Supported formats
- Quality settings
- Rate limits
- Messages (localization)

## 🔧 Advanced Setup

### Sebagai System Service
```bash
# Copy service file
sudo cp telegram-bot.service /etc/systemd/system/

# Enable and start service
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

# Check status
sudo systemctl status telegram-bot
```

### Docker Setup (Optional)
```bash
# Build image
docker build -t telegram-converter-bot .

# Run container
docker run -d --name tg-bot \
  -e BOT_TOKEN=your_token \
  -v $(pwd)/data:/app/data \
  telegram-converter-bot
```

## 📊 Monitoring & Logs

### Logs Location
- Bot logs: `logs/bot.log`
- System logs: `journalctl -u telegram-bot`

### Statistics
Bot menyimpan statistik penggunaan:
- Total konversi per user
- Format konversi populer
- Waktu rata-rata proses
- Error rate

## 🛠️ Development

### Project Structure
```
telegram-file-converter-bot/
├── bot.py              # Main bot application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── setup.sh           # Automated setup script
├── start_bot.sh       # Quick start script
├── check_requirements.py # Dependency checker
├── .env               # Environment variables
├── logs/              # Log files
├── temp/              # Temporary files
├── data/              # User data & stats
└── venv/              # Virtual environment
```

### Adding New Formats
1. Update `SUPPORTED_FORMATS` in `config.py`
2. Implement converter method in `FileConverter` class
3. Add format detection logic
4. Test thoroughly

### Custom Messages
Edit `MESSAGES` dict in `config.py` for localization atau custom text.

## 🐛 Troubleshooting

### Common Issues

**1. Bot tidak merespon**
```bash
# Check bot status
systemctl status telegram-bot

# Check logs
tail -f logs/bot.log
```

**2. FFmpeg not found**
```bash
# Install ffmpeg
sudo apt-get install ffmpeg

# Verify installation
ffmpeg -version
```

**3. Permission errors**
```bash
# Fix permissions
chmod +x setup.sh start_bot.sh
chown -R $USER:$USER /path/to/bot
```

**4. Module import errors**
```bash
# Check dependencies
python check_requirements.py

# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

## 📞 Support

### Getting Help
1. Check [Issues](https://github.com/username/repo/issues) for common problems
2. Read documentation thoroughly
3. Check logs for error messages
4. Create new issue dengan detail lengkap

### Reporting Bugs
Include:
- OS and Python version
- Error logs
- Steps to reproduce
- Expected vs actual behavior

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Pillow](https://pillow.readthedocs.io/) - Image processing library
- [FFmpeg](https://ffmpeg.org/) - Video/audio processing
- [ReportLab](https://www.reportlab.com/) - PDF generation

## 📈 Roadmap

- [ ] Batch file processing
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] Web interface
- [ ] Advanced video editing features
- [ ] AI-powered image enhancement
- [ ] Multiple language support
- [ ] File preview generation
- [ ] Webhook support for high-volume usage

---

**⚡ Quick Start**: Run `./setup.sh` then edit `.env` with your bot token!

**💡 Pro Tip**: Use `/stats` to monitor your usage and `/formats` to see all supported conversions.

**🔒 Security**: Never share your bot token publicly. Use environment variables or secure config files.
