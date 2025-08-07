"""
Configuration file for Telegram File Converter Bot
"""

import os
from typing import Dict, List

# Bot Token Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# File Processing Limits
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_CONVERSION_TIME = 300  # 5 minutes
CLEANUP_INTERVAL = 3600  # 1 hour

# Supported File Formats
SUPPORTED_FORMATS = {
    'image': {
        'input': ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp', 'ico'],
        'output': ['jpg', 'png', 'pdf', 'webp', 'bmp', 'gif', 'ico']
    },
    'document': {
        'input': ['txt', 'docx', 'pdf', 'rtf'],
        'output': ['pdf', 'txt', 'docx']
    },
    'archive': {
        'input': ['zip', 'rar', '7z', 'tar', 'gz'],
        'output': ['zip']
    },
    'video': {
        'input': ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm'],
        'output': ['mp4', 'avi', 'gif', 'webm']
    },
    'audio': {
        'input': ['mp3', 'wav', 'ogg', 'aac', 'flac', 'm4a', 'wma'],
        'output': ['mp3', 'wav', 'ogg', 'aac']
    }
}

# Quality Settings
QUALITY_SETTINGS = {
    'image': {
        'jpg_quality': 95,
        'png_optimize': True,
        'webp_quality': 90
    },
    'video': {
        'default_bitrate': '1000k',
        'gif_fps': 10,
        'gif_scale': 'scale=480:-1'
    },
    'audio': {
        'default_bitrate': '128k',
        'sample_rate': 44100
    }
}

# Bot Messages (Indonesian)
MESSAGES = {
    'welcome': """
🤖 **Selamat datang di File Converter Bot!**

Halo {name}! 👋

Bot ini dapat mengkonversi berbagai jenis file:
📸 **Gambar**: JPG, PNG, PDF, WebP, BMP, GIF
📄 **Dokumen**: TXT, DOCX, PDF
🗜️ **Arsip**: ZIP, RAR, 7Z
🎥 **Video**: MP4, AVI, MKV, MOV → MP4, AVI, GIF
🎵 **Audio**: MP3, WAV, OGG, AAC

**Cara menggunakan:**
1. Kirim file yang ingin dikonversi
2. Pilih format tujuan dari menu
3. Tunggu proses konversi selesai
4. Unduh file hasil konversi

Gunakan /help untuk bantuan lebih lanjut!
    """,
    
    'help': """
🔧 **Panduan Penggunaan Bot**

**Fitur Utama:**
• Konversi format file otomatis
• Dukungan multiple format
• Proses cepat dan aman
• Antarmuka yang mudah digunakan

**Langkah-langkah:**
1️⃣ Kirim file (foto, dokumen, video, audio)
2️⃣ Pilih format konversi yang diinginkan
3️⃣ Tunggu proses selesai
4️⃣ Unduh file hasil konversi

**Batasan:**
• Maksimal ukuran file: {max_size}MB
• File akan dihapus setelah 1 jam
• Konversi video/audio membutuhkan waktu lebih lama

**Perintah yang tersedia:**
/start - Mulai menggunakan bot
/help - Tampilkan bantuan ini
/formats - Lihat format yang didukung
/stats - Lihat statistik penggunaan

**Tips:**
💡 File gambar akan mempertahankan kualitas original
💡 Konversi PDF mendukung multiple halaman
💡 File arsip dapat diekstrak otomatis
    """,
    
    'formats': """
📋 **Format File yang Didukung**

**🖼️ GAMBAR**
Input: JPG, JPEG, PNG, BMP, GIF, TIFF, WebP, ICO
Output: JPG, PNG, PDF, WebP, BMP, GIF, ICO

**📄 DOKUMEN**
Input: TXT, DOCX, PDF, RTF
Output: PDF, TXT, DOCX

**🗜️ ARSIP**
Input: ZIP, RAR, 7Z, TAR, GZ
Output: ZIP (ekstraksi)

**🎥 VIDEO**
Input: MP4, AVI, MKV, MOV, WMV, FLV, WebM
Output: MP4, AVI, GIF, WebM

**🎵 AUDIO**
Input: MP3, WAV, OGG, AAC, FLAC, M4A, WMA
Output: MP3, WAV, OGG, AAC

**Catatan Khusus:**
• Konversi gambar ke PDF membuat dokumen single-page
• PDF ke TXT mengekstrak teks yang dapat dibaca
• Video ke GIF dibatasi 10 detik pertama
• Kualitas audio dapat disesuaikan
    """,
    
    'file_received': """📁 **File diterima:** `{filename}`
📊 **Ukuran:** {size}
🔄 **Pilih format konversi:**""",
    
    'processing': "🔄 **Memproses konversi...**",
    'success': "✅ **Konversi berhasil!** File telah dikirim.",
    'error': "❌ **Konversi gagal.** Silakan coba lagi atau gunakan format lain.",
    'file_too_large': "❌ File terlalu besar! Maksimal {max_size}MB",
    'unsupported_format': "❌ Format file `{format}` tidak didukung untuk konversi.",
    'session_expired': "❌ Sesi expired. Silakan upload file lagi.",
    'cancelled': "❌ Konversi dibatalkan."
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'bot.log'
}

# Advanced Features
FEATURES = {
    'enable_stats': True,
    'enable_user_limits': True,
    'enable_admin_commands': True,
    'enable_batch_processing': False,
    'enable_cloud_storage': False
}

# Rate Limiting
RATE_LIMITS = {
    'conversions_per_hour': 10,
    'conversions_per_day': 50,
    'max_concurrent_conversions': 3
}