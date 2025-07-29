#!/usr/bin/env python3
"""
Final Enhanced Telegram Bot untuk Konversi TXT/VCF/XLS
Dengan format OLXX-83.vcf dan kontak REXX-83-1 serta opsi reset/lanjut
"""

import os
import logging
import asyncio
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

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
user_sessions = {}
user_stats = {}

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.files = []
        self.current_action = None
        self.current_step = None
        self.custom_settings = {}
        self.temp_data = {}
        
    def add_file(self, file_info):
        file_info['upload_time'] = datetime.now()
        self.files.append(file_info)
        
    def clear_files(self):
        for file_info in self.files:
            if os.path.exists(file_info.get('path', '')):
                os.remove(file_info['path'])
        self.files = []
        
    def reset_settings(self):
        self.custom_settings = {}
        self.current_step = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Initialize user session
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
        user_stats[user_id] = {'conversions': 0, 'last_activity': datetime.now()}
    
    welcome_text = f"""
🚀 **Selamat datang {user_name}!**

**Final Enhanced Bot TXT/VCF/XLS Converter**

🎯 **Fitur TXT → VCF Custom:**
• File: OLXX-83.vcf, OLXX-84.vcf
• Kontak: REXX-83-1, REXX-83-2
• Custom nomor mulai file
• Opsi reset/lanjut urutan

**Contoh:**
📝 Nama file: OLXX
🔢 Mulai dari file: 83
👤 Nama kontak: REXX
🔄 Reset/Lanjut urutan per ganti file

Pilih mode di bawah: 👇
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 TXT → VCF Custom", callback_data="action_txt_vcf_custom"),
            InlineKeyboardButton("📞 VCF → TXT", callback_data="action_vcf_txt")
        ],
        [
            InlineKeyboardButton("📊 XLS → VCF", callback_data="action_xls_vcf"),
            InlineKeyboardButton("🔄 Konversi Biasa", callback_data="action_convert_normal")
        ],
        [
            InlineKeyboardButton("📋 Info Format", callback_data="formats"),
            InlineKeyboardButton("📊 Statistik", callback_data="stats")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    session = user_sessions.get(user_id)
    
    if not session:
        session = UserSession(user_id)
        user_sessions[user_id] = session

    data = query.data
    
    if data == "action_txt_vcf_custom":
        await handle_txt_vcf_custom(query, session)
    elif data == "action_vcf_txt":
        await handle_vcf_txt_action(query, session)
    elif data == "action_xls_vcf":
        await handle_xls_vcf_action(query, session)
    elif data == "action_convert_normal":
        await handle_convert_normal(query, session)
    elif data == "formats":
        await show_formats(query)
    elif data == "stats":
        await show_stats(query, user_id)
    elif data.startswith("convert_"):
        await handle_conversion(query, session, data)
    elif data.startswith("reset_"):
        await handle_reset_continue_choice(query, session, data)
    elif data == "back_main":
        await start_from_callback(query)

async def handle_txt_vcf_custom(query, session):
    """Handle custom TXT to VCF conversion"""
    session.current_action = "txt_vcf_custom"
    session.current_step = "upload_file"
    session.reset_settings()
    
    text = """
🔄 **Mode TXT → VCF Custom**

📝 **Format Baru:**
• File: OLXX-83.vcf, OLXX-84.vcf, OLXX-85.vcf
• Kontak: REXX-83-1, REXX-83-2, REXX-83-3

**Yang bisa dicustom:**
🔢 Nomor file mulai dari mana (83, 84, dst)
🔄 Reset urutan kontak atau lanjut dari sebelumnya

**Langkah 1:** Upload file TXT Anda sekarang! 📎
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_vcf_txt_action(query, session):
    """Handle VCF to TXT conversion"""
    session.current_action = "vcf_txt"
    session.current_step = "upload_file"
    
    text = """
📞 **Mode VCF → TXT**

Upload file VCF yang ingin dikonversi ke TXT.

**Hasil:** Text list dengan format:
```
Nama - Phone - Email
Nama - Phone - Email
```

Upload file VCF sekarang! 📎
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_xls_vcf_action(query, session):
    """Handle XLS to VCF conversion"""
    session.current_action = "xls_vcf"
    session.current_step = "upload_file"
    
    text = """
📊 **Mode XLS → VCF**

Upload file Excel yang ingin dikonversi ke VCF.

**Format Excel yang didukung:**
• Kolom 1: Nama
• Kolom 2: Phone (opsional)
• Kolom 3: Email (opsional)

Upload file Excel sekarang! 📎
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_convert_normal(query, session):
    """Handle normal conversion"""
    session.current_action = "convert_normal"
    session.current_step = "upload_file"
    
    text = """
🔄 **Mode Konversi Biasa**

Upload file untuk konversi standar:
• TXT ↔ VCF
• VCF ↔ TXT  
• XLS ↔ VCF
• Semua format saling mendukung

Upload file sekarang! 📎
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

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
    
    # Get session
    session = user_sessions.get(user_id)
    if not session:
        session = UserSession(user_id)
        user_sessions[user_id] = session
    
    # Get file extension
    file_name = document.file_name or "unknown"
    file_ext = file_name.split('.')[-1].lower() if '.' in file_name else ""
    
    # Check supported formats
    if file_ext not in ['txt', 'vcf', 'xls', 'xlsx', 'csv']:
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
        file_info = {
            'path': file_path,
            'name': file_name,
            'ext': file_ext,
            'size': document.file_size
        }
        session.add_file(file_info)
        
        # Handle based on current action
        if session.current_action == "txt_vcf_custom":
            await process_txt_vcf_custom(update, session, file_info)
        elif session.current_action == "vcf_txt":
            await process_vcf_txt(update, session, file_info)
        elif session.current_action == "xls_vcf":
            await process_xls_vcf(update, session, file_info)
        elif session.current_action == "convert_normal":
            await process_convert_normal(update, session, file_info)
        else:
            await process_convert_normal(update, session, file_info)
            
    except Exception as e:
        logger.error(f"File download error: {e}")
        await update.message.reply_text(f"❌ Gagal mengunduh file: {str(e)}")

async def process_txt_vcf_custom(update, session, file_info):
    """Process TXT to VCF with custom settings"""
    if file_info['ext'] != 'txt':
        await update.message.reply_text("❌ Untuk mode custom, hanya file TXT yang didukung.")
        return
        
    # Count data in file
    data_count = await get_txt_data_count(file_info['path'])
    
    text = f"""
📁 **File diterima:** `{file_info['name']}`
📊 **Total data:** {data_count} baris
📝 **Format:** TXT

**Langkah 2:** Masukkan nama file prefix

**Contoh:** `OLXX`
**Hasil:** OLXX-83.vcf, OLXX-84.vcf, OLXX-85.vcf

Ketik nama file prefix:
"""
    
    session.current_step = "input_filename"
    session.temp_data['file_info'] = file_info
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id)
    
    if not session or not session.current_step:
        return
        
    text = update.message.text.strip()
    
    if session.current_step == "input_filename":
        await handle_filename_input(update, session, text)
    elif session.current_step == "input_startfile":
        await handle_startfile_input(update, session, text)
    elif session.current_step == "input_contactname":
        await handle_contactname_input(update, session, text)

async def handle_filename_input(update, session, filename):
    """Handle filename input"""
    # Validate filename
    if not re.match(r'^[a-zA-Z0-9_-]+$', filename):
        await update.message.reply_text(
            "❌ Nama file tidak valid. Gunakan hanya huruf, angka, underscore (_), dan dash (-).\n"
            "Contoh: OLXX, DATA01, CUSTOMER_LIST"
        )
        return
        
    session.custom_settings['filename'] = filename
    session.current_step = "input_startfile"
    
    text = f"""
✅ **Nama file:** `{filename}-XX.vcf`

**Langkah 3:** Mulai dari nomor file berapa?

**Contoh:** `83`
**Hasil:** {filename}-83.vcf, {filename}-84.vcf, {filename}-85.vcf

Ketik nomor file mulai (1-9999):
"""
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_startfile_input(update, session, startfile_str):
    """Handle start file number input"""
    try:
        startfile = int(startfile_str)
        if startfile < 1 or startfile > 9999:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(
            "❌ Nomor file tidak valid. Masukkan angka antara 1-9999.\n"
            "Contoh: 83, 100, 1"
        )
        return
        
    session.custom_settings['startfile'] = startfile
    session.current_step = "input_contactname"
    
    text = f"""
✅ **Nomor file mulai:** `{startfile}`

**Langkah 4:** Masukkan nama kontak prefix

**Contoh:** `REXX`
**Hasil:** REXX-{startfile}-1, REXX-{startfile}-2, REXX-{startfile}-3

Ketik prefix nama kontak:
"""
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_contactname_input(update, session, contactname):
    """Handle contact name input"""
    # Validate contact name
    if not re.match(r'^[a-zA-Z0-9_-]+$', contactname):
        await update.message.reply_text(
            "❌ Nama kontak tidak valid. Gunakan hanya huruf, angka, underscore (_), dan dash (-).\n"
            "Contoh: REXX, CUSTOMER, CLIENT_A"
        )
        return
        
    session.custom_settings['contactname'] = contactname
    
    # Show reset/continue option
    await show_reset_continue_option(update, session)

async def show_reset_continue_option(update, session):
    """Show option to reset or continue contact numbering"""
    settings = session.custom_settings
    
    text = f"""
✅ **Nama kontak:** `{settings['contactname']}-{settings['startfile']}-X`

**Langkah 5:** Urutan nomor kontak

🔄 **Reset:** Setiap file baru, nomor kontak reset ke 1
   - File 1: {settings['contactname']}-{settings['startfile']}-1, {settings['contactname']}-{settings['startfile']}-2
   - File 2: {settings['contactname']}-{settings['startfile']+1}-1, {settings['contactname']}-{settings['startfile']+1}-2

⚡ **Lanjut:** Nomor kontak lanjut berurutan antar file
   - File 1: {settings['contactname']}-{settings['startfile']}-1, {settings['contactname']}-{settings['startfile']}-2
   - File 2: {settings['contactname']}-{settings['startfile']+1}-3, {settings['contactname']}-{settings['startfile']+1}-4

Pilih mode:
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Reset per File", callback_data="reset_mode")],
        [InlineKeyboardButton("⚡ Lanjut Berurutan", callback_data="reset_continue")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_reset_continue_choice(query, session, data):
    """Handle reset/continue choice"""
    choice = data.replace("reset_", "")
    session.custom_settings['reset_mode'] = (choice == "mode")
    
    # Show summary and start processing
    await show_custom_summary(query, session)

async def show_custom_summary(query, session):
    """Show summary of custom settings and start processing"""
    settings = session.custom_settings
    file_info = session.temp_data['file_info']
    data_count = await get_txt_data_count(file_info['path'])
    
    reset_text = "Reset per file" if settings['reset_mode'] else "Lanjut berurutan"
    
    text = f"""
📋 **Ringkasan Pengaturan:**

📁 **File:** {settings['filename']}-{settings['startfile']}.vcf, {settings['filename']}-{settings['startfile']+1}.vcf, dst
👤 **Kontak:** {settings['contactname']}-{settings['startfile']}-1, {settings['contactname']}-{settings['startfile']}-2, dst
🔄 **Mode:** {reset_text}
📈 **Total data:** {data_count} kontak

⚡ **Memproses...**
"""
    
    await query.edit_message_text(text, parse_mode='Markdown')
    
    # Start processing
    await process_custom_txt_to_vcf(query, session, file_info)

async def process_custom_txt_to_vcf(query, session, file_info):
    """Process TXT to VCF with custom settings"""
    try:
        settings = session.custom_settings
        result_files = await convert_txt_to_vcf_custom_new(
            file_info['path'],
            settings['filename'],
            settings['startfile'],
            settings['contactname'],
            settings['reset_mode']
        )
        
        if result_files:
            await query.message.reply_text(f"✅ Berhasil! {len(result_files)} file VCF dibuat.")
            
            # Send all result files
            for i, result_file in enumerate(result_files):
                with open(result_file, 'rb') as f:
                    file_number = settings['startfile'] + i
                    filename = f"{settings['filename']}-{file_number}.vcf"
                    
                    # Count contacts in this file
                    with open(result_file, 'r', encoding='utf-8') as cf:
                        contact_count = cf.read().count('BEGIN:VCARD')
                    
                    caption = f"📁 {filename}\n👥 {contact_count} kontak"
                    
                    await query.message.reply_document(
                        document=f,
                        filename=filename,
                        caption=caption
                    )
                
                # Cleanup
                os.remove(result_file)
            
            # Update stats
            user_stats[session.user_id]['conversions'] += 1
            
            # Reset session
            session.clear_files()
            session.reset_settings()
            session.current_action = None
            session.current_step = None
            
        else:
            await query.message.reply_text("❌ Gagal memproses file.")
            
    except Exception as e:
        logger.error(f"Custom TXT to VCF error: {e}")
        await query.message.reply_text(f"❌ Error: {str(e)}")

async def convert_txt_to_vcf_custom_new(source_path, filename_prefix, start_file_num, contact_prefix, reset_mode):
    """Convert TXT to multiple VCF files with new custom format"""
    # Read TXT file
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    result_files = []
    contacts_per_file = 1000  # Default 1000 contacts per file
    global_contact_num = 1
    
    # Split into chunks
    for chunk_index in range(0, len(lines), contacts_per_file):
        chunk_lines = lines[chunk_index:chunk_index + contacts_per_file]
        file_number = start_file_num + (chunk_index // contacts_per_file)
        
        # Create VCF file
        vcf_filename = f"{filename_prefix}-{file_number}.vcf"
        
        with open(vcf_filename, 'w', encoding='utf-8') as f:
            for i, line in enumerate(chunk_lines):
                # Parse line for phone and email if available
                parts = line.split(' - ') if ' - ' in line else [line]
                original_name = parts[0].strip()
                phone = parts[1].strip() if len(parts) > 1 else ""
                email = parts[2].strip() if len(parts) > 2 else ""
                
                # Create custom contact name based on mode
                if reset_mode:
                    # Reset per file: REXX-83-1, REXX-83-2 for file 83
                    contact_num = i + 1
                else:
                    # Continue numbering: REXX-83-1, REXX-84-1001, etc
                    contact_num = global_contact_num
                
                contact_name = f"{contact_prefix}-{file_number}-{contact_num}"
                
                # Write vCard
                f.write(f"BEGIN:VCARD\n")
                f.write(f"VERSION:3.0\n")
                f.write(f"FN:{contact_name}\n")
                f.write(f"N:{contact_name};;;;\n")
                if phone:
                    f.write(f"TEL:{phone}\n")
                if email:
                    f.write(f"EMAIL:{email}\n")
                # Store original name in NOTE field
                f.write(f"NOTE:Original: {original_name}\n")
                f.write(f"END:VCARD\n")
                
                if i < len(chunk_lines) - 1:
                    f.write(f"\n")
                
                global_contact_num += 1
        
        result_files.append(vcf_filename)
    
    return result_files

async def process_vcf_txt(update, session, file_info):
    """Process VCF to TXT conversion"""
    if file_info['ext'] != 'vcf':
        await update.message.reply_text("❌ Untuk mode ini, hanya file VCF yang didukung.")
        return
        
    await update.message.reply_text("🔄 Mengkonversi VCF ke TXT...")
    
    try:
        result_file = await convert_vcf_to_txt_simple(file_info)
        
        if result_file:
            with open(result_file, 'rb') as f:
                filename = f"{file_info['name'].split('.')[0]}.txt"
                await update.message.reply_document(
                    document=f,
                    filename=filename,
                    caption="✅ Konversi VCF → TXT berhasil!"
                )
            
            os.remove(result_file)
            user_stats[session.user_id]['conversions'] += 1
            session.clear_files()
        else:
            await update.message.reply_text("❌ Gagal mengkonversi file.")
            
    except Exception as e:
        logger.error(f"VCF to TXT error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def process_xls_vcf(update, session, file_info):
    """Process XLS to VCF conversion"""
    if file_info['ext'] not in ['xls', 'xlsx']:
        await update.message.reply_text("❌ Untuk mode ini, hanya file Excel yang didukung.")
        return
        
    await update.message.reply_text("🔄 Mengkonversi Excel ke VCF...")
    
    try:
        result_file = await convert_xls_to_vcf_simple(file_info)
        
        if result_file:
            with open(result_file, 'rb') as f:
                filename = f"{file_info['name'].split('.')[0]}.vcf"
                await update.message.reply_document(
                    document=f,
                    filename=filename,
                    caption="✅ Konversi Excel → VCF berhasil!"
                )
            
            os.remove(result_file)
            user_stats[session.user_id]['conversions'] += 1
            session.clear_files()
        else:
            await update.message.reply_text("❌ Gagal mengkonversi file.")
            
    except Exception as e:
        logger.error(f"Excel to VCF error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def process_convert_normal(update, session, file_info):
    """Process normal conversion"""
    available_formats = get_conversion_options(file_info['ext'])
    
    keyboard = []
    for fmt in available_formats:
        keyboard.append([InlineKeyboardButton(
            f"Konversi ke {fmt.upper()}", 
            callback_data=f"convert_{fmt}_0"
        )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""
📎 **File diterima:** `{file_info['name']}`
📊 **Ukuran:** {file_info['size'] // 1024} KB
📝 **Format:** {file_info['ext'].upper()}

Pilih format tujuan konversi:
"""
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def get_txt_data_count(file_path):
    """Get count of lines in TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len([line for line in f.readlines() if line.strip()])
    except:
        return 0

async def convert_vcf_to_txt_simple(file_info):
    """Simple VCF to TXT conversion"""
    source_path = file_info['path']
    target_path = f"converted_{file_info['name'].split('.')[0]}.txt"
    
    try:
        contacts = await parse_vcf_file(source_path)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            for contact in contacts:
                line = contact['name']
                if contact['phone']:
                    line += f" - {contact['phone']}"
                if contact['email']:
                    line += f" - {contact['email']}"
                f.write(line + '\n')
        
        return target_path if os.path.exists(target_path) else None
        
    except Exception as e:
        logger.error(f"VCF to TXT conversion error: {e}")
        return None

async def convert_xls_to_vcf_simple(file_info):
    """Simple Excel to VCF conversion"""
    source_path = file_info['path']
    target_path = f"converted_{file_info['name'].split('.')[0]}.vcf"
    
    try:
        df = pd.read_excel(source_path)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            for i, (_, row) in enumerate(df.iterrows()):
                name = str(row.iloc[0]) if len(row) > 0 and pd.notna(row.iloc[0]) else f"Contact_{i+1}"
                phone = str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else ""
                email = str(row.iloc[2]) if len(row) > 2 and pd.notna(row.iloc[2]) else ""
                
                f.write(f"BEGIN:VCARD\n")
                f.write(f"VERSION:3.0\n")
                f.write(f"FN:{name}\n")
                f.write(f"N:{name};;;;\n")
                if phone and phone != "nan":
                    f.write(f"TEL:{phone}\n")
                if email and email != "nan":
                    f.write(f"EMAIL:{email}\n")
                f.write(f"END:VCARD\n")
                if i < len(df) - 1:
                    f.write(f"\n")
        
        return target_path if os.path.exists(target_path) else None
        
    except Exception as e:
        logger.error(f"Excel to VCF conversion error: {e}")
        return None

async def parse_vcf_file(file_path):
    """Parse VCF file and extract contacts"""
    contacts = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    vcards = content.split('BEGIN:VCARD')
    for vcard in vcards:
        if 'FN:' in vcard:
            name = ""
            phone = ""
            email = ""
            
            for line in vcard.split('\n'):
                line = line.strip()
                if line.startswith('FN:'):
                    name = line.replace('FN:', '').strip()
                elif line.startswith('TEL'):
                    phone = line.split(':')[-1].strip()
                elif line.startswith('EMAIL'):
                    email = line.split(':')[-1].strip()
            
            if name:
                contacts.append({
                    'name': name,
                    'phone': phone,
                    'email': email
                })
    
    return contacts

def get_conversion_options(source_ext):
    """Get available conversion options for source format"""
    options = {
        'txt': ['vcf'],
        'vcf': ['txt'],
        'xls': ['vcf'],
        'xlsx': ['vcf'],
    }
    return options.get(source_ext, [])

async def handle_conversion(query, session, data):
    """Handle simple conversion"""
    parts = data.split('_')
    target_format = parts[1]
    
    if not session.files:
        await query.edit_message_text("❌ File tidak ditemukan.")
        return
    
    file_info = session.files[0]
    
    await query.edit_message_text(f"🔄 Mengkonversi ke {target_format.upper()}...")
    
    try:
        if file_info['ext'] == 'vcf' and target_format == 'txt':
            result_file = await convert_vcf_to_txt_simple(file_info)
        elif file_info['ext'] in ['xls', 'xlsx'] and target_format == 'vcf':
            result_file = await convert_xls_to_vcf_simple(file_info)
        else:
            result_file = None
        
        if result_file:
            with open(result_file, 'rb') as f:
                filename = f"{file_info['name'].split('.')[0]}.{target_format}"
                await query.message.reply_document(
                    document=f,
                    filename=filename,
                    caption=f"✅ Konversi berhasil! File: `{filename}`",
                    parse_mode='Markdown'
                )
            
            os.remove(result_file)
            user_stats[session.user_id]['conversions'] += 1
            await query.edit_message_text(f"✅ Konversi ke {target_format.upper()} selesai!")
        else:
            await query.edit_message_text("❌ Gagal mengkonversi file.")
            
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        await query.edit_message_text(f"❌ Error: {str(e)}")

async def show_formats(query):
    """Show supported formats"""
    text = """
📋 **Format File yang Didukung:**

**TXT → VCF Custom:**
• File: OLXX-83.vcf, OLXX-84.vcf
• Kontak: REXX-83-1, REXX-83-2
• Custom nomor file mulai
• Opsi reset/lanjut urutan

**VCF → TXT:**
• Konversi kontak ke text list

**XLS → VCF:**
• Excel ke kontak vCard

**Format Input:**
```
TXT: Nama - Phone - Email (per baris)
VCF: Format vCard standar
XLS: Kolom 1=Nama, 2=Phone, 3=Email
```
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_stats(query, user_id):
    """Show user statistics"""
    stats = user_stats.get(user_id, {'conversions': 0})
    
    text = f"""
📊 **Statistik Anda:**

🔄 **Total Konversi:** {stats['conversions']}
⚡ **Mode Favorit:** TXT → VCF Custom

**Global Stats:**
👥 **Total Users:** {len(user_stats)}
🔄 **Total Konversi:** {sum(s['conversions'] for s in user_stats.values())}
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def start_from_callback(query):
    """Restart from callback"""
    user_id = query.from_user.id
    user_name = query.from_user.first_name
    
    welcome_text = f"""
🚀 **Final Enhanced Bot TXT/VCF/XLS**

Halo {user_name}! Pilih mode:

🔄 **TXT → VCF Custom** - Format baru
📞 **VCF → TXT** - Konversi standar
📊 **XLS → VCF** - Excel ke kontak
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 TXT → VCF Custom", callback_data="action_txt_vcf_custom"),
            InlineKeyboardButton("📞 VCF → TXT", callback_data="action_vcf_txt")
        ],
        [
            InlineKeyboardButton("📊 XLS → VCF", callback_data="action_xls_vcf"),
            InlineKeyboardButton("🔄 Konversi Biasa", callback_data="action_convert_normal")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("❌ Perintah admin only.")
        return
    
    total_users = len(user_stats)
    total_conversions = sum(s['conversions'] for s in user_stats.values())
    
    admin_text = f"""
🔧 **Admin Panel - Final Enhanced Bot**

📊 **Statistik:**
👥 Total Users: {total_users}
🔄 Total Konversi: {total_conversions}

**Final Features:**
🔄 TXT → VCF format baru (OLXX-83.vcf)
👤 Kontak format baru (REXX-83-1)
🔄 Opsi reset/lanjut urutan
"""
    
    await update.message.reply_text(admin_text, parse_mode='Markdown')

def main():
    """Main function"""
    print("🚀 Starting Final Enhanced TXT/VCF/XLS Converter Bot...")
    
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Please set BOT_TOKEN in .env file!")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    if ADMIN_USER_ID:
        application.add_handler(CommandHandler("admin", admin_command))
    
    print("✅ Final Enhanced Bot started!")
    print(f"👑 Admin ID: {ADMIN_USER_ID}")
    print("🎯 New Features:")
    print("   📁 File format: OLXX-83.vcf, OLXX-84.vcf")
    print("   👤 Contact format: REXX-83-1, REXX-83-2")
    print("   🔄 Reset/Continue options")
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()