#!/usr/bin/env python3
"""
Simple Telegram File Converter Bot
A working implementation with basic conversion features
"""

import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from PIL import Image
import tempfile
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0')) if os.getenv('ADMIN_USER_ID') else None

# Global variables
user_files = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_text = f"""
🤖 **Selamat datang di File Converter Bot!**

Halo {user.first_name}! 👋

Bot ini dapat mengkonversi file gambar:
📸 **Gambar**: JPG ↔ PNG ↔ WebP

**Cara menggunakan:**
1. Kirim foto atau dokumen gambar
2. Pilih format tujuan dari menu
3. Unduh file hasil konversi

Gunakan /help untuk bantuan lebih lanjut!
    """
    
    keyboard = [
        [InlineKeyboardButton("ℹ️ Bantuan", callback_data="help")],
        [InlineKeyboardButton("📊 Status", callback_data="status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🔧 **Panduan Penggunaan Bot**

**Fitur:**
• Konversi gambar JPG/PNG/WebP
• Interface yang mudah digunakan
• Proses cepat

**Cara Pakai:**
1️⃣ Kirim foto atau file gambar
2️⃣ Pilih format yang diinginkan
3️⃣ Unduh file hasil konversi

**Admin Commands:** (ID: {admin_id})
/admin - Panel admin

**Batasan:**
• Maksimal ukuran file: 20MB
• File dihapus setelah konversi
    """.format(admin_id=ADMIN_USER_ID if ADMIN_USER_ID else "Not configured")
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command"""
    user_id = update.effective_user.id
    
    if ADMIN_USER_ID and user_id == ADMIN_USER_ID:
        admin_text = f"""
🔧 **Panel Admin Bot**

📊 **Statistik:**
👥 Active Users: {len(user_files)}
🔄 Files in Queue: {sum(1 for files in user_files.values() if files)}

**Status:** ✅ Bot Running
**Admin ID:** {ADMIN_USER_ID}
**Bot Token:** {BOT_TOKEN[:10]}...
        """
        await update.message.reply_text(admin_text, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Perintah ini hanya untuk admin.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages"""
    user_id = update.effective_user.id
    photo = update.message.photo[-1]  # Get highest resolution
    
    # Store photo info for user
    user_files[user_id] = {
        'file_id': photo.file_id,
        'type': 'photo'
    }
    
    # Create conversion options
    keyboard = [
        [InlineKeyboardButton("📄 Convert to PNG", callback_data=f"convert_png_{user_id}")],
        [InlineKeyboardButton("🖼️ Convert to JPG", callback_data=f"convert_jpg_{user_id}")],
        [InlineKeyboardButton("🌐 Convert to WebP", callback_data=f"convert_webp_{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📸 **Foto diterima!**\n\nPilih format konversi:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document messages"""
    user_id = update.effective_user.id
    document = update.message.document
    
    # Check if it's an image file
    if document.mime_type and document.mime_type.startswith('image/'):
        user_files[user_id] = {
            'file_id': document.file_id,
            'type': 'document',
            'filename': document.file_name
        }
        
        keyboard = [
            [InlineKeyboardButton("📄 Convert to PNG", callback_data=f"convert_png_{user_id}")],
            [InlineKeyboardButton("🖼️ Convert to JPG", callback_data=f"convert_jpg_{user_id}")],
            [InlineKeyboardButton("🌐 Convert to WebP", callback_data=f"convert_webp_{user_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"📄 **File diterima:** `{document.file_name}`\n\nPilih format konversi:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("❌ Hanya file gambar yang didukung saat ini.")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "help":
        await help_command(update, context)
    elif query.data == "status":
        await query.edit_message_text(
            f"🤖 **Bot Status**\n\n✅ Online\n👥 Users: {len(user_files)}\n🔄 Ready for conversions",
            parse_mode='Markdown'
        )
    elif query.data.startswith("convert_"):
        await process_conversion(update, context)

async def process_conversion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process file conversion"""
    query = update.callback_query
    data_parts = query.data.split('_')
    target_format = data_parts[1]
    user_id = int(data_parts[2])
    
    if user_id not in user_files:
        await query.edit_message_text("❌ File tidak ditemukan. Silakan kirim ulang file.")
        return
    
    await query.edit_message_text(f"🔄 **Mengkonversi ke {target_format.upper()}...**\n\nMohon tunggu sebentar...")
    
    try:
        file_info = user_files[user_id]
        
        # Download file
        file = await context.bot.get_file(file_info['file_id'])
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.tmp', delete=False) as input_file:
            await file.download_to_drive(input_file.name)
            input_path = input_file.name
        
        output_path = f"{input_path}.{target_format}"
        
        # Convert image
        with Image.open(input_path) as img:
            # Handle transparency for PNG to JPG conversion
            if target_format.lower() == 'jpg' and img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            img.save(output_path, format=target_format.upper())
        
        # Send converted file
        with open(output_path, 'rb') as converted_file:
            original_name = file_info.get('filename', f'image.{target_format}')
            new_filename = f"{os.path.splitext(original_name)[0]}.{target_format}"
            
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=converted_file,
                filename=new_filename,
                caption=f"✅ **Konversi selesai!**\n📄 Format: {target_format.upper()}"
            )
        
        await query.edit_message_text(
            f"✅ **Konversi berhasil!**\n\n📄 File telah dikonversi ke {target_format.upper()}\n🎉 Silakan unduh file di atas."
        )
        
        # Clean up
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        
        # Remove from user files
        del user_files[user_id]
        
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        await query.edit_message_text(f"❌ **Error:** Gagal mengkonversi file.\n\nCoba lagi dengan file yang lain.")

def main():
    """Main function"""
    print("🤖 Starting Simple Telegram File Converter Bot...")
    print(f"🔑 Bot Token: {BOT_TOKEN[:10]}...")
    
    if ADMIN_USER_ID:
        print(f"👑 Admin ID: {ADMIN_USER_ID}")
    
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Please set BOT_TOKEN in .env file!")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_command))
    
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    print("🚀 Bot starting...")
    
    try:
        # Run the bot
        application.run_polling()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Bot error: {e}")

if __name__ == '__main__':
    main()