#!/usr/bin/env python3
"""
Telegram Bot untuk Konversi File TXT/VCF/XLS
Bot sederhana yang fokus pada konversi antara TXT, VCF, dan XLS
"""

import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import tempfile
import pandas as pd
import openpyxl
from dotenv import load_dotenv
import csv
import io

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
user_stats = {}

# Supported formats
SUPPORTED_FORMATS = {
    'txt': ['vcf', 'xls', 'xlsx', 'csv'],
    'vcf': ['txt', 'xls', 'xlsx', 'csv'], 
    'xls': ['txt', 'vcf', 'csv', 'xlsx'],
    'xlsx': ['txt', 'vcf', 'csv', 'xls'],
    'csv': ['txt', 'vcf', 'xls', 'xlsx']
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Initialize user stats
    if user_id not in user_stats:
        user_stats[user_id] = {'conversions': 0, 'last_conversion': None}
    
    welcome_text = f"""
🤖 **Selamat datang {user_name}!**

Bot ini khusus untuk konversi file:
📝 **TXT** ↔ **VCF** ↔ **XLS**

**Format yang didukung:**
• TXT (Text files)
• VCF (Contact files) 
• XLS/XLSX (Excel files)
• CSV (Comma-separated values)

**Cara penggunaan:**
1. Kirim file yang ingin dikonversi
2. Pilih format tujuan dari menu
3. Download file hasil konversi

Kirimkan file untuk memulai! 📎
"""
    
    keyboard = [
        [InlineKeyboardButton("📋 Format Didukung", callback_data="formats")],
        [InlineKeyboardButton("ℹ️ Bantuan", callback_data="help")],
        [InlineKeyboardButton("📊 Statistik", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "formats":
        formats_text = """
📋 **Format File yang Didukung:**

**TXT (Text)**
• Plain text files
• Konversi ke: VCF, XLS, CSV

**VCF (vCard)**  
• Contact/kontak files
• Konversi ke: TXT, XLS, CSV

**XLS/XLSX (Excel)**
• Spreadsheet files
• Konversi ke: TXT, VCF, CSV

**CSV (Comma-Separated)**
• Data dalam format CSV
• Konversi ke: TXT, VCF, XLS

*Ukuran file maksimal: 20MB*
"""
        await query.edit_message_text(formats_text, parse_mode='Markdown')
        
    elif query.data == "help":
        help_text = """
ℹ️ **Panduan Penggunaan:**

**Langkah-langkah:**
1. Kirim file (TXT/VCF/XLS/CSV)
2. Bot akan mendeteksi format file
3. Pilih format tujuan konversi
4. Download file hasil

**Tips:**
• File TXT: satu baris = satu data
• File VCF: format standar vCard
• File XLS: data dalam kolom-kolom
• File CSV: gunakan koma sebagai pemisah

**Contoh konversi:**
• Kontak TXT → VCF
• Data Excel → TXT list
• VCF contacts → Excel spreadsheet
"""
        await query.edit_message_text(help_text, parse_mode='Markdown')
        
    elif query.data == "stats":
        user_id = query.from_user.id
        stats = user_stats.get(user_id, {'conversions': 0})
        
        stats_text = f"""
📊 **Statistik Anda:**

🔄 Total Konversi: {stats['conversions']}
📅 Konversi Terakhir: {stats.get('last_conversion', 'Belum ada')}

**Statistik Global:**
👥 Total Users: {len(user_stats)}
🔄 Total Konversi: {sum(s['conversions'] for s in user_stats.values())}
"""
        await query.edit_message_text(stats_text, parse_mode='Markdown')
        
    elif query.data.startswith("convert_"):
        # Handle conversion selection
        target_format = query.data.replace("convert_", "")
        user_id = query.from_user.id
        
        if user_id not in user_files:
            await query.edit_message_text("❌ File tidak ditemukan. Silakan upload file lagi.")
            return
            
        await query.edit_message_text(f"🔄 Mengkonversi ke format {target_format.upper()}...")
        
        try:
            # Perform conversion
            result_file = await convert_file(user_files[user_id], target_format)
            
            if result_file:
                # Send converted file
                with open(result_file, 'rb') as f:
                    filename = f"{user_files[user_id]['name'].split('.')[0]}.{target_format}"
                    await context.bot.send_document(
                        chat_id=query.message.chat_id,
                        document=f,
                        filename=filename,
                        caption=f"✅ Konversi berhasil! File: {filename}"
                    )
                
                # Update stats
                user_stats[user_id]['conversions'] += 1
                user_stats[user_id]['last_conversion'] = f"{target_format.upper()}"
                
                # Cleanup
                os.remove(result_file)
                del user_files[user_id]
                
                await query.edit_message_text(f"✅ Konversi ke {target_format.upper()} selesai!")
            else:
                await query.edit_message_text("❌ Gagal mengkonversi file. Coba lagi.")
                
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            await query.edit_message_text(f"❌ Error saat konversi: {str(e)}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file uploads"""
    user_id = update.effective_user.id
    document = update.message.document
    
    if not document:
        await update.message.reply_text("❌ Silakan kirim file yang valid.")
        return
    
    # Check file size (20MB limit)
    if document.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("❌ File terlalu besar! Maksimal 20MB.")
        return
    
    # Get file extension
    file_name = document.file_name or "unknown"
    file_ext = file_name.split('.')[-1].lower() if '.' in file_name else ""
    
    # Check if format is supported
    if file_ext not in SUPPORTED_FORMATS:
        await update.message.reply_text(
            f"❌ Format `.{file_ext}` tidak didukung.\n\n"
            "Format yang didukung: TXT, VCF, XLS, XLSX, CSV"
        )
        return
    
    # Download file
    await update.message.reply_text("📥 Mengunduh file...")
    
    try:
        file = await document.get_file()
        file_path = f"temp_{user_id}_{file_name}"
        await file.download_to_drive(file_path)
        
        # Store file info
        user_files[user_id] = {
            'path': file_path,
            'name': file_name,
            'ext': file_ext,
            'size': document.file_size
        }
        
        # Show conversion options
        available_formats = SUPPORTED_FORMATS[file_ext]
        
        keyboard = []
        for fmt in available_formats:
            keyboard.append([InlineKeyboardButton(
                f"Konversi ke {fmt.upper()}", 
                callback_data=f"convert_{fmt}"
            )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"📎 File diterima: `{file_name}`\n"
            f"📊 Ukuran: {document.file_size // 1024} KB\n"
            f"📝 Format: {file_ext.upper()}\n\n"
            "Pilih format tujuan konversi:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"File download error: {e}")
        await update.message.reply_text(f"❌ Gagal mengunduh file: {str(e)}")

async def convert_file(file_info, target_format):
    """Convert file to target format"""
    source_path = file_info['path']
    source_ext = file_info['ext']
    target_path = f"converted_{file_info['name'].split('.')[0]}.{target_format}"
    
    try:
        if source_ext == 'txt':
            await convert_from_txt(source_path, target_path, target_format)
        elif source_ext == 'vcf':
            await convert_from_vcf(source_path, target_path, target_format)
        elif source_ext in ['xls', 'xlsx']:
            await convert_from_excel(source_path, target_path, target_format)
        elif source_ext == 'csv':
            await convert_from_csv(source_path, target_path, target_format)
        
        # Cleanup source file
        if os.path.exists(source_path):
            os.remove(source_path)
            
        return target_path if os.path.exists(target_path) else None
        
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        return None

async def convert_from_txt(source_path, target_path, target_format):
    """Convert from TXT to other formats"""
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    if target_format == 'vcf':
        # Convert TXT lines to VCF contacts
        with open(target_path, 'w', encoding='utf-8') as f:
            for i, line in enumerate(lines):
                f.write(f"BEGIN:VCARD\n")
                f.write(f"VERSION:3.0\n") 
                f.write(f"FN:{line}\n")
                f.write(f"N:{line};;;;\n")
                f.write(f"END:VCARD\n")
                if i < len(lines) - 1:
                    f.write(f"\n")
                    
    elif target_format in ['xls', 'xlsx']:
        # Convert TXT to Excel
        df = pd.DataFrame(lines, columns=['Data'])
        df.to_excel(target_path, index=False)
        
    elif target_format == 'csv':
        # Convert TXT to CSV
        with open(target_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Data'])
            for line in lines:
                writer.writerow([line])

async def convert_from_vcf(source_path, target_path, target_format):
    """Convert from VCF to other formats"""
    contacts = []
    
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Parse VCF contacts
    vcards = content.split('BEGIN:VCARD')
    for vcard in vcards:
        if 'FN:' in vcard:
            name = ""
            phone = ""
            email = ""
            
            for line in vcard.split('\n'):
                if line.startswith('FN:'):
                    name = line.replace('FN:', '').strip()
                elif line.startswith('TEL'):
                    phone = line.split(':')[-1].strip()
                elif line.startswith('EMAIL'):
                    email = line.split(':')[-1].strip()
            
            if name:
                contacts.append({'Name': name, 'Phone': phone, 'Email': email})
    
    if target_format == 'txt':
        # Convert VCF to TXT
        with open(target_path, 'w', encoding='utf-8') as f:
            for contact in contacts:
                line = contact['Name']
                if contact['Phone']:
                    line += f" - {contact['Phone']}"
                if contact['Email']:
                    line += f" - {contact['Email']}"
                f.write(line + '\n')
                
    elif target_format in ['xls', 'xlsx']:
        # Convert VCF to Excel
        df = pd.DataFrame(contacts)
        df.to_excel(target_path, index=False)
        
    elif target_format == 'csv':
        # Convert VCF to CSV
        df = pd.DataFrame(contacts)
        df.to_csv(target_path, index=False)

async def convert_from_excel(source_path, target_path, target_format):
    """Convert from Excel to other formats"""
    df = pd.read_excel(source_path)
    
    if target_format == 'txt':
        # Convert Excel to TXT
        with open(target_path, 'w', encoding='utf-8') as f:
            for _, row in df.iterrows():
                line = ' - '.join([str(val) for val in row.values if pd.notna(val)])
                f.write(line + '\n')
                
    elif target_format == 'vcf':
        # Convert Excel to VCF (assume first column is name)
        with open(target_path, 'w', encoding='utf-8') as f:
            for i, (_, row) in enumerate(df.iterrows()):
                name = str(row.iloc[0]) if len(row) > 0 else f"Contact {i+1}"
                phone = str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else ""
                email = str(row.iloc[2]) if len(row) > 2 and pd.notna(row.iloc[2]) else ""
                
                f.write(f"BEGIN:VCARD\n")
                f.write(f"VERSION:3.0\n")
                f.write(f"FN:{name}\n")
                f.write(f"N:{name};;;;\n")
                if phone:
                    f.write(f"TEL:{phone}\n")
                if email:
                    f.write(f"EMAIL:{email}\n")
                f.write(f"END:VCARD\n")
                if i < len(df) - 1:
                    f.write(f"\n")
                    
    elif target_format == 'csv':
        # Convert Excel to CSV
        df.to_csv(target_path, index=False)

async def convert_from_csv(source_path, target_path, target_format):
    """Convert from CSV to other formats"""
    df = pd.read_csv(source_path)
    
    if target_format == 'txt':
        # Convert CSV to TXT
        with open(target_path, 'w', encoding='utf-8') as f:
            for _, row in df.iterrows():
                line = ' - '.join([str(val) for val in row.values if pd.notna(val)])
                f.write(line + '\n')
                
    elif target_format == 'vcf':
        # Convert CSV to VCF
        with open(target_path, 'w', encoding='utf-8') as f:
            for i, (_, row) in enumerate(df.iterrows()):
                name = str(row.iloc[0]) if len(row) > 0 else f"Contact {i+1}"
                phone = str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else ""
                email = str(row.iloc[2]) if len(row) > 2 and pd.notna(row.iloc[2]) else ""
                
                f.write(f"BEGIN:VCARD\n")
                f.write(f"VERSION:3.0\n")
                f.write(f"FN:{name}\n")
                f.write(f"N:{name};;;;\n")
                if phone:
                    f.write(f"TEL:{phone}\n")
                if email:
                    f.write(f"EMAIL:{email}\n")
                f.write(f"END:VCARD\n")
                if i < len(df) - 1:
                    f.write(f"\n")
                    
    elif target_format in ['xls', 'xlsx']:
        # Convert CSV to Excel
        df.to_excel(target_path, index=False)

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("❌ Perintah ini hanya untuk admin.")
        return
    
    total_users = len(user_stats)
    total_conversions = sum(s['conversions'] for s in user_stats.values())
    
    admin_text = f"""
🔧 **Panel Admin Bot**

📊 **Statistik:**
👥 Total Users: {total_users}
🔄 Total Conversions: {total_conversions}
💾 Active Sessions: {len(user_files)}

**Format yang didukung:**
📝 TXT ↔ VCF ↔ XLS ↔ CSV

**Commands:**
/admin - Panel admin
/stats - Statistik global
"""
    
    await update.message.reply_text(admin_text, parse_mode='Markdown')

def main():
    """Main function"""
    print("🤖 Starting TXT/VCF/XLS Converter Bot...")
    
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Please set BOT_TOKEN in .env file!")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    if ADMIN_USER_ID:
        application.add_handler(CommandHandler("admin", admin_command))
    
    print("✅ Bot started successfully!")
    print(f"👑 Admin ID: {ADMIN_USER_ID}")
    print("📝 Supported: TXT, VCF, XLS, XLSX, CSV")
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()