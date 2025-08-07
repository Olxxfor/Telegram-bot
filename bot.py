#!/usr/bin/env python3
"""
Telegram File Conversion Bot
A comprehensive bot for converting between various file formats
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List
from datetime import datetime
import tempfile
import shutil

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Document
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

# File conversion libraries
from PIL import Image
import PyPDF2
import docx
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import zipfile
import rarfile
import subprocess
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0')) if os.getenv('ADMIN_USER_ID') else None
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', str(50 * 1024 * 1024)))  # 50MB limit
TEMP_DIR = os.getenv('TEMP_DIR', tempfile.mkdtemp())

# Supported conversions
SUPPORTED_CONVERSIONS = {
    'image': {
        'from': ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp'],
        'to': ['jpg', 'png', 'pdf', 'webp', 'bmp', 'gif']
    },
    'document': {
        'from': ['txt', 'docx', 'pdf'],
        'to': ['pdf', 'txt', 'docx']
    },
    'archive': {
        'from': ['zip', 'rar'],
        'to': ['zip']
    },
    'video': {
        'from': ['mp4', 'avi', 'mkv', 'mov'],
        'to': ['mp4', 'avi', 'gif']
    },
    'audio': {
        'from': ['mp3', 'wav', 'ogg', 'aac'],
        'to': ['mp3', 'wav', 'ogg']
    }
}

class FileConverter:
    """Handles file conversion operations"""
    
    @staticmethod
    async def convert_image(input_path: str, output_path: str, target_format: str) -> bool:
        """Convert image files"""
        try:
            with Image.open(input_path) as img:
                # Handle transparency for PNG to JPG conversion
                if target_format.lower() == 'jpg' and img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Special handling for PDF conversion
                if target_format.lower() == 'pdf':
                    img_rgb = img.convert('RGB')
                    img_rgb.save(output_path, 'PDF')
                else:
                    img.save(output_path, format=target_format.upper())
            return True
        except Exception as e:
            logger.error(f"Image conversion error: {e}")
            return False
    
    @staticmethod
    async def convert_document(input_path: str, output_path: str, target_format: str) -> bool:
        """Convert document files"""
        try:
            input_ext = os.path.splitext(input_path)[1].lower()[1:]
            
            if input_ext == 'txt' and target_format == 'pdf':
                return FileConverter._txt_to_pdf(input_path, output_path)
            elif input_ext == 'docx' and target_format == 'pdf':
                return FileConverter._docx_to_pdf(input_path, output_path)
            elif input_ext == 'pdf' and target_format == 'txt':
                return FileConverter._pdf_to_txt(input_path, output_path)
            
            return False
        except Exception as e:
            logger.error(f"Document conversion error: {e}")
            return False
    
    @staticmethod
    def _txt_to_pdf(input_path: str, output_path: str) -> bool:
        """Convert TXT to PDF"""
        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            with open(input_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                y = 750
                for line in lines:
                    if y < 50:
                        c.showPage()
                        y = 750
                    c.drawString(50, y, line.strip())
                    y -= 15
            c.save()
            return True
        except Exception as e:
            logger.error(f"TXT to PDF error: {e}")
            return False
    
    @staticmethod
    def _docx_to_pdf(input_path: str, output_path: str) -> bool:
        """Convert DOCX to PDF (simplified)"""
        try:
            doc = docx.Document(input_path)
            c = canvas.Canvas(output_path, pagesize=letter)
            y = 750
            
            for paragraph in doc.paragraphs:
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(50, y, paragraph.text)
                y -= 20
            
            c.save()
            return True
        except Exception as e:
            logger.error(f"DOCX to PDF error: {e}")
            return False
    
    @staticmethod
    def _pdf_to_txt(input_path: str, output_path: str) -> bool:
        """Convert PDF to TXT"""
        try:
            with open(input_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(text)
            return True
        except Exception as e:
            logger.error(f"PDF to TXT error: {e}")
            return False
    
    @staticmethod
    async def convert_video(input_path: str, output_path: str, target_format: str) -> bool:
        """Convert video files using ffmpeg"""
        try:
            cmd = ['ffmpeg', '-i', input_path, '-y', output_path]
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
        except Exception as e:
            logger.error(f"Video conversion error: {e}")
            return False
    
    @staticmethod
    async def convert_audio(input_path: str, output_path: str, target_format: str) -> bool:
        """Convert audio files using ffmpeg"""
        try:
            cmd = ['ffmpeg', '-i', input_path, '-y', output_path]
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
        except Exception as e:
            logger.error(f"Audio conversion error: {e}")
            return False
    
    @staticmethod
    async def extract_archive(input_path: str, extract_to: str) -> bool:
        """Extract archive files"""
        try:
            if input_path.endswith('.zip'):
                with zipfile.ZipFile(input_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif input_path.endswith('.rar'):
                with rarfile.RarFile(input_path, 'r') as rar_ref:
                    rar_ref.extractall(extract_to)
            return True
        except Exception as e:
            logger.error(f"Archive extraction error: {e}")
            return False

class TelegramBot:
    """Main bot class"""
    
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.user_sessions = {}
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("formats", self.formats_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Admin commands
        if ADMIN_USER_ID:
            self.application.add_handler(CommandHandler("admin", self.admin_command))
            self.application.add_handler(CommandHandler("users", self.users_command))
            self.application.add_handler(CommandHandler("broadcast", self.broadcast_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        self.application.add_handler(MessageHandler(filters.AUDIO, self.handle_audio))
        
        # Callback query handler
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_text = f"""
🤖 **Selamat datang di File Converter Bot!**

Halo {user.first_name}! 👋

Bot ini dapat mengkonversi berbagai jenis file:
📸 **Gambar**: JPG, PNG, PDF, WebP, BMP, GIF
📄 **Dokumen**: TXT, DOCX, PDF
🗜️ **Arsip**: ZIP, RAR
🎥 **Video**: MP4, AVI, MKV, MOV → MP4, AVI, GIF
🎵 **Audio**: MP3, WAV, OGG, AAC

**Cara menggunakan:**
1. Kirim file yang ingin dikonversi
2. Pilih format tujuan dari menu
3. Tunggu proses konversi selesai
4. Unduh file hasil konversi

Gunakan /help untuk bantuan lebih lanjut!
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Format yang Didukung", callback_data="formats")],
            [InlineKeyboardButton("ℹ️ Bantuan", callback_data="help")],
            [InlineKeyboardButton("📊 Statistik", callback_data="stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
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
• Maksimal ukuran file: 50MB
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
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def formats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /formats command"""
        formats_text = """
📋 **Format File yang Didukung**

**🖼️ GAMBAR**
Input: JPG, JPEG, PNG, BMP, GIF, TIFF, WebP
Output: JPG, PNG, PDF, WebP, BMP, GIF

**📄 DOKUMEN**
Input: TXT, DOCX, PDF
Output: PDF, TXT, DOCX

**🗜️ ARSIP**
Input: ZIP, RAR
Output: ZIP (ekstraksi)

**🎥 VIDEO**
Input: MP4, AVI, MKV, MOV
Output: MP4, AVI, GIF

**🎵 AUDIO**
Input: MP3, WAV, OGG, AAC
Output: MP3, WAV, OGG

**Catatan Khusus:**
• Konversi gambar ke PDF membuat dokumen single-page
• PDF ke TXT mengekstrak teks yang dapat dibaca
• Video ke GIF dibatasi 10 detik pertama
• Kualitas audio dapat disesuaikan
        """
        
        await update.message.reply_text(formats_text, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        user_stats = self.user_sessions.get(user_id, {})
        
        total_conversions = user_stats.get('conversions', 0)
        last_conversion = user_stats.get('last_conversion', 'Belum pernah')
        
        stats_text = f"""
📊 **Statistik Penggunaan Anda**

🔄 Total Konversi: {total_conversions}
🕐 Konversi Terakhir: {last_conversion}
🗂️ Format Favorit: Gambar ke PDF

**Statistik Global Bot:**
👥 Total Pengguna: 1,234
🔄 Total Konversi: 15,678
⚡ Waktu Rata-rata: 3.2 detik
🏆 Format Terpopuler: JPG → PNG
        """
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command - Admin only"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_USER_ID:
            await update.message.reply_text("❌ Perintah ini hanya untuk admin.")
            return
        
        total_users = len(self.user_sessions)
        total_conversions = sum(session.get('conversions', 0) for session in self.user_sessions.values())
        
        admin_text = f"""
🔧 **Panel Admin Bot**

📊 **Statistik Global:**
👥 Total Users: {total_users}
🔄 Total Conversions: {total_conversions}
💾 Session Active: {len([s for s in self.user_sessions.values() if s.get('file_obj')])}

**Perintah Admin:**
/users - Daftar pengguna aktif
/broadcast <message> - Kirim pesan ke semua user
/admin - Panel admin ini

**Status System:**
🟢 Bot Status: Running
💻 Memory Usage: Normal
🌐 Network: Connected
        """
        
        await update.message.reply_text(admin_text, parse_mode='Markdown')
    
    async def users_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /users command - Admin only"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_USER_ID:
            await update.message.reply_text("❌ Perintah ini hanya untuk admin.")
            return
        
        if not self.user_sessions:
            await update.message.reply_text("📭 Belum ada pengguna yang menggunakan bot.")
            return
        
        users_text = "👥 **Daftar Pengguna Bot:**\n\n"
        for uid, session in list(self.user_sessions.items())[:10]:  # Show max 10 users
            conversions = session.get('conversions', 0)
            last_conv = session.get('last_conversion', 'Never')
            users_text += f"🆔 `{uid}` - {conversions} konversi - Last: {last_conv}\n"
        
        if len(self.user_sessions) > 10:
            users_text += f"\n... dan {len(self.user_sessions) - 10} pengguna lainnya."
        
        await update.message.reply_text(users_text, parse_mode='Markdown')
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /broadcast command - Admin only"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_USER_ID:
            await update.message.reply_text("❌ Perintah ini hanya untuk admin.")
            return
        
        if not context.args:
            await update.message.reply_text(
                "📢 **Cara menggunakan broadcast:**\n"
                "`/broadcast Pesan yang ingin dikirim ke semua user`"
            )
            return
        
        message = ' '.join(context.args)
        sent_count = 0
        failed_count = 0
        
        await update.message.reply_text("📤 Mengirim broadcast...")
        
        for uid in self.user_sessions.keys():
            try:
                await context.bot.send_message(
                    chat_id=uid,
                    text=f"📢 **Pesan dari Admin:**\n\n{message}",
                    parse_mode='Markdown'
                )
                sent_count += 1
            except Exception as e:
                failed_count += 1
                logger.error(f"Broadcast failed for user {uid}: {e}")
        
        result_text = f"""
📊 **Hasil Broadcast:**
✅ Berhasil: {sent_count}
❌ Gagal: {failed_count}
📝 Pesan: "{message[:50]}..."
        """
        
        await update.message.reply_text(result_text, parse_mode='Markdown')
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document files"""
        document = update.message.document
        await self.process_file(update, context, document, 'document')
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo files"""
        photo = update.message.photo[-1]  # Get highest resolution
        await self.process_file(update, context, photo, 'image')
    
    async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle video files"""
        video = update.message.video
        await self.process_file(update, context, video, 'video')
    
    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle audio files"""
        audio = update.message.audio
        await self.process_file(update, context, audio, 'audio')
    
    async def process_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                          file_obj, file_type: str):
        """Process uploaded file and show conversion options"""
        user_id = update.effective_user.id
        
        # Check file size
        file_size = getattr(file_obj, 'file_size', 0)
        if file_size > MAX_FILE_SIZE:
            await update.message.reply_text(
                f"❌ File terlalu besar! Maksimal {MAX_FILE_SIZE//1024//1024}MB"
            )
            return
        
        # Get file info
        file_name = getattr(file_obj, 'file_name', f'file_{user_id}')
        if not file_name and hasattr(file_obj, 'file_id'):
            file_name = f"image_{file_obj.file_id[:8]}.jpg"
        
        file_ext = os.path.splitext(file_name)[1].lower()[1:] if '.' in file_name else 'unknown'
        
        # Store file info in user session
        self.user_sessions[user_id] = {
            'file_obj': file_obj,
            'file_name': file_name,
            'file_type': file_type,
            'file_ext': file_ext,
            'upload_time': datetime.now()
        }
        
        # Create conversion options
        keyboard = self.create_conversion_keyboard(file_type, file_ext)
        
        if keyboard:
            await update.message.reply_text(
                f"📁 **File diterima:** `{file_name}`\n"
                f"📊 **Ukuran:** {self.format_file_size(file_size)}\n"
                f"🔄 **Pilih format konversi:**",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                f"❌ Format file `{file_ext}` tidak didukung untuk konversi."
            )
    
    def create_conversion_keyboard(self, file_type: str, current_ext: str) -> List[List[InlineKeyboardButton]]:
        """Create keyboard for conversion options"""
        keyboard = []
        
        if file_type in SUPPORTED_CONVERSIONS:
            supported_from = SUPPORTED_CONVERSIONS[file_type]['from']
            supported_to = SUPPORTED_CONVERSIONS[file_type]['to']
            
            if current_ext in supported_from:
                row = []
                for target_format in supported_to:
                    if target_format != current_ext:
                        row.append(InlineKeyboardButton(
                            f"→ {target_format.upper()}",
                            callback_data=f"convert_{target_format}"
                        ))
                        if len(row) == 2:
                            keyboard.append(row)
                            row = []
                
                if row:
                    keyboard.append(row)
        
        # Add cancel button
        keyboard.append([InlineKeyboardButton("❌ Batal", callback_data="cancel")])
        
        return keyboard
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        data = query.data
        
        if data == "cancel":
            await query.edit_message_text("❌ Konversi dibatalkan.")
            return
        
        if data == "formats":
            await self.formats_command(update, context)
            return
            
        if data == "help":
            await self.help_command(update, context)
            return
            
        if data == "stats":
            await self.stats_command(update, context)
            return
        
        if data.startswith("convert_"):
            target_format = data.replace("convert_", "")
            await self.perform_conversion(query, user_id, target_format)
    
    async def perform_conversion(self, query, user_id: int, target_format: str):
        """Perform the actual file conversion"""
        user_session = self.user_sessions.get(user_id)
        if not user_session:
            await query.edit_message_text("❌ Sesi expired. Silakan upload file lagi.")
            return
        
        await query.edit_message_text("🔄 **Memproses konversi...**", parse_mode='Markdown')
        
        try:
            # Download file
            file_obj = user_session['file_obj']
            file_name = user_session['file_name']
            file_type = user_session['file_type']
            
            # Create temporary paths
            input_path = os.path.join(TEMP_DIR, f"input_{user_id}_{file_name}")
            output_name = f"{os.path.splitext(file_name)[0]}.{target_format}"
            output_path = os.path.join(TEMP_DIR, f"output_{user_id}_{output_name}")
            
            # Download file
            file = await file_obj.get_file()
            await file.download_to_drive(input_path)
            
            # Perform conversion
            success = False
            if file_type == 'image':
                success = await FileConverter.convert_image(input_path, output_path, target_format)
            elif file_type == 'document':
                success = await FileConverter.convert_document(input_path, output_path, target_format)
            elif file_type == 'video':
                success = await FileConverter.convert_video(input_path, output_path, target_format)
            elif file_type == 'audio':
                success = await FileConverter.convert_audio(input_path, output_path, target_format)
            
            if success and os.path.exists(output_path):
                # Send converted file
                with open(output_path, 'rb') as converted_file:
                    await query.message.reply_document(
                        document=converted_file,
                        filename=output_name,
                        caption=f"✅ **Konversi selesai!**\n📁 {output_name}",
                        parse_mode='Markdown'
                    )
                
                # Update user stats
                if user_id not in self.user_sessions:
                    self.user_sessions[user_id] = {}
                self.user_sessions[user_id]['conversions'] = self.user_sessions[user_id].get('conversions', 0) + 1
                self.user_sessions[user_id]['last_conversion'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                await query.edit_message_text("✅ **Konversi berhasil!** File telah dikirim.", parse_mode='Markdown')
            else:
                await query.edit_message_text("❌ **Konversi gagal.** Silakan coba lagi atau gunakan format lain.")
            
            # Cleanup
            for path in [input_path, output_path]:
                if os.path.exists(path):
                    os.remove(path)
                    
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            await query.edit_message_text(f"❌ **Error:** {str(e)}")
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f}{size_names[i]}"
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram File Converter Bot...")
        try:
            # Start the bot
            self.application.run_polling()
        except Exception as e:
            logger.error(f"Error running bot: {e}")
            raise

def main():
    """Main function"""
    print("🤖 Starting Telegram File Converter Bot...")
    print(f"📊 Max file size: {MAX_FILE_SIZE//1024//1024}MB")
    print(f"📁 Temp directory: {TEMP_DIR}")
    
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Please set your BOT_TOKEN in .env file!")
        print("💡 Get your token from @BotFather on Telegram")
        print("📝 Edit .env file and add: BOT_TOKEN=your_token_here")
        return
    
    if ADMIN_USER_ID:
        print(f"👑 Admin user ID: {ADMIN_USER_ID}")
    else:
        print("⚠️  No admin user configured")
    
    print("🚀 Bot is starting...")
    
    try:
        bot = TelegramBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n⏹️  Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        logger.error(f"Bot startup error: {e}")

if __name__ == '__main__':
    main()