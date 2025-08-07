#!/usr/bin/env python3
"""
Advanced Telegram Bot untuk Konversi File TXT/VCF/XLS
Dengan fitur rename, merge, split, dan custom ordering
"""

import os
import logging
import asyncio
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import pandas as pd
import tempfile
from dotenv import load_dotenv
import json
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
        self.files = []  # List of uploaded files
        self.current_action = None
        self.temp_data = {}
        self.merge_files = []
        self.split_settings = {}
        
    def add_file(self, file_info):
        file_info['upload_time'] = datetime.now()
        self.files.append(file_info)
        
    def clear_files(self):
        # Cleanup temporary files
        for file_info in self.files:
            if os.path.exists(file_info.get('path', '')):
                os.remove(file_info['path'])
        self.files = []
        self.merge_files = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Initialize user session
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
        user_stats[user_id] = {'conversions': 0, 'last_activity': datetime.now()}
    
    welcome_text = f"""
🤖 **Selamat datang {user_name}!**

**Bot Konversi File Advanced TXT/VCF/XLS**

🔄 **Konversi Dasar:**
• TXT ↔ VCF 
• XLS → VCF
• Semua format saling mendukung

✨ **Fitur Advanced:**
📝 Rename File & Kontak
🔗 Gabungkan Multiple File  
✂️ Pecah File (Custom jumlah)
📋 Custom Urutan & Nama
🎯 Pengaturan Fleksibel

**Cara mulai:**
1. Upload file atau pilih aksi dari menu
2. Ikuti panduan step-by-step
3. Nikmati hasil yang sempurna!

Pilih aksi di bawah: 👇
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Konversi File", callback_data="action_convert"),
            InlineKeyboardButton("📝 Rename File", callback_data="action_rename")
        ],
        [
            InlineKeyboardButton("🔗 Gabung File", callback_data="action_merge"),
            InlineKeyboardButton("✂️ Pecah File", callback_data="action_split")
        ],
        [
            InlineKeyboardButton("📋 Format Info", callback_data="formats"),
            InlineKeyboardButton("📊 Statistik", callback_data="stats")
        ],
        [InlineKeyboardButton("ℹ️ Bantuan Lengkap", callback_data="help")]
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
    
    if data == "action_convert":
        await handle_convert_action(query, session)
    elif data == "action_rename":
        await handle_rename_action(query, session)
    elif data == "action_merge":
        await handle_merge_action(query, session)
    elif data == "action_split":
        await handle_split_action(query, session)
    elif data == "formats":
        await show_formats(query)
    elif data == "stats":
        await show_stats(query, user_id)
    elif data == "help":
        await show_help(query)
    elif data.startswith("convert_"):
        await handle_conversion(query, session, data)
    elif data.startswith("merge_"):
        await handle_merge_process(query, session, data)
    elif data.startswith("split_"):
        await handle_split_process(query, session, data)
    elif data.startswith("rename_"):
        await handle_rename_process(query, session, data)
    elif data == "back_main":
        await start_from_callback(query)

async def handle_convert_action(query, session):
    """Handle conversion action"""
    session.current_action = "convert"
    
    text = """
🔄 **Mode Konversi File**

**Format yang didukung:**
📝 TXT → VCF (Kontak)
📞 VCF → TXT (Text list)  
📊 XLS → VCF (Excel ke Kontak)

**Langkah:**
1. Upload file yang ingin dikonversi
2. Pilih format tujuan
3. Atur custom nama (opsional)
4. Download hasil

Silakan upload file sekarang! 📎
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_rename_action(query, session):
    """Handle rename action"""
    session.current_action = "rename"
    
    text = """
📝 **Mode Rename File & Kontak**

**Fitur Rename:**
📁 Rename nama file hasil
👤 Rename nama kontak di VCF
🔢 Tambah nomor urut otomatis
📋 Custom format nama

**Contoh:**
• File: `contacts_2024.vcf`
• Kontak: `Customer_001, Customer_002`
• Pattern: `Nama_[urut]`

Upload file untuk rename! 📎
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_merge_action(query, session):
    """Handle merge action"""
    session.current_action = "merge"
    session.merge_files = []
    
    text = """
🔗 **Mode Gabungkan File**

**Fitur Merge:**
📁 Gabung multiple TXT/VCF/XLS
🔢 Atur urutan penggabungan
📝 Custom nama file hasil
🎯 Remove duplikat otomatis

**Langkah:**
1. Upload file pertama
2. Upload file kedua, dst
3. Atur urutan & nama
4. Gabungkan!

Upload file pertama! 📎
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_split_action(query, session):
    """Handle split action"""
    session.current_action = "split"
    
    text = """
✂️ **Mode Pecah File**

**Fitur Split:**
📊 Pecah berdasarkan jumlah data
🔢 Custom berapa data per file
📝 Auto numbering file hasil
📋 Pertahankan struktur

**Contoh:**
• File 1000 kontak → 10 file @ 100 kontak
• Custom: 1,2,3 atau 5,10,15 data per file

Upload file untuk dipecah! 📎
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
        file_path = f"temp_{user_id}_{len(session.files)}_{file_name}"
        await file.download_to_drive(file_path)
        
        # Store file info
        file_info = {
            'path': file_path,
            'name': file_name,
            'ext': file_ext,
            'size': document.file_size,
            'index': len(session.files)
        }
        session.add_file(file_info)
        
        # Handle based on current action
        if session.current_action == "convert":
            await handle_file_conversion(update, session, file_info)
        elif session.current_action == "rename":
            await handle_file_rename(update, session, file_info)
        elif session.current_action == "merge":
            await handle_file_merge(update, session, file_info)
        elif session.current_action == "split":
            await handle_file_split(update, session, file_info)
        else:
            # Default conversion
            await handle_file_conversion(update, session, file_info)
            
    except Exception as e:
        logger.error(f"File download error: {e}")
        await update.message.reply_text(f"❌ Gagal mengunduh file: {str(e)}")

async def handle_file_conversion(update, session, file_info):
    """Handle single file conversion"""
    available_formats = get_conversion_options(file_info['ext'])
    
    keyboard = []
    for fmt in available_formats:
        keyboard.append([InlineKeyboardButton(
            f"Konversi ke {fmt.upper()}", 
            callback_data=f"convert_{fmt}_{file_info['index']}"
        )])
    
    keyboard.append([InlineKeyboardButton("📝 Custom Nama", callback_data=f"convert_custom_{file_info['index']}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""
📎 **File diterima:** `{file_info['name']}`
📊 **Ukuran:** {file_info['size'] // 1024} KB
📝 **Format:** {file_info['ext'].upper()}

Pilih format tujuan konversi:
"""
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_file_rename(update, session, file_info):
    """Handle file rename"""
    data_count = await get_file_data_count(file_info)
    
    text = f"""
📝 **Rename: {file_info['name']}**
📊 **Data Count:** {data_count} items
📝 **Format:** {file_info['ext'].upper()}

**Pilih mode rename:**
"""
    
    keyboard = [
        [InlineKeyboardButton("📁 Rename File Saja", callback_data=f"rename_file_{file_info['index']}")],
        [InlineKeyboardButton("👤 Rename Kontak/Data", callback_data=f"rename_data_{file_info['index']}")],
        [InlineKeyboardButton("🔄 Rename File + Data", callback_data=f"rename_both_{file_info['index']}")],
        [InlineKeyboardButton("🔢 Auto Numbering", callback_data=f"rename_auto_{file_info['index']}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_file_merge(update, session, file_info):
    """Handle merge process"""
    merge_count = len(session.merge_files)
    session.merge_files.append(file_info)
    
    text = f"""
🔗 **File #{merge_count + 1} ditambahkan**

📁 **File:** {file_info['name']}
📊 **Total files:** {len(session.merge_files)}

**File list:**
"""
    
    for i, f in enumerate(session.merge_files):
        text += f"\n{i+1}. {f['name']} ({f['ext'].upper()})"
    
    keyboard = []
    if len(session.merge_files) >= 2:
        keyboard.extend([
            [InlineKeyboardButton("🔗 Mulai Merge", callback_data="merge_start")],
            [InlineKeyboardButton("📋 Atur Urutan", callback_data="merge_order")]
        ])
    
    keyboard.extend([
        [InlineKeyboardButton("➕ Tambah File Lagi", callback_data="merge_add")],
        [InlineKeyboardButton("🗑️ Reset", callback_data="merge_reset")]
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_file_split(update, session, file_info):
    """Handle split process"""
    data_count = await get_file_data_count(file_info)
    
    text = f"""
✂️ **Split File: {file_info['name']}**
📊 **Total Data:** {data_count} items
📝 **Format:** {file_info['ext'].upper()}

**Pilih cara split:**
"""
    
    keyboard = [
        [InlineKeyboardButton("🔢 Split Equal (Sama rata)", callback_data=f"split_equal_{file_info['index']}")],
        [InlineKeyboardButton("📝 Split Custom", callback_data=f"split_custom_{file_info['index']}")],
        [InlineKeyboardButton("⚡ Split Cepat", callback_data=f"split_quick_{file_info['index']}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_conversion(query, session, data):
    """Handle actual conversion"""
    parts = data.split('_')
    target_format = parts[1]
    file_index = int(parts[2]) if len(parts) > 2 else 0
    
    if file_index >= len(session.files):
        await query.edit_message_text("❌ File tidak ditemukan.")
        return
    
    file_info = session.files[file_index]
    
    await query.edit_message_text(f"🔄 Mengkonversi ke {target_format.upper()}...")
    
    try:
        result_file = await convert_file(file_info, target_format)
        
        if result_file:
            # Send converted file
            with open(result_file, 'rb') as f:
                filename = f"{file_info['name'].split('.')[0]}.{target_format}"
                await query.message.reply_document(
                    document=f,
                    filename=filename,
                    caption=f"✅ Konversi berhasil!\n📁 File: `{filename}`",
                    parse_mode='Markdown'
                )
            
            # Update stats
            user_stats[session.user_id]['conversions'] += 1
            
            # Cleanup
            os.remove(result_file)
            
            await query.edit_message_text(f"✅ Konversi ke {target_format.upper()} selesai!")
        else:
            await query.edit_message_text("❌ Gagal mengkonversi file.")
            
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        await query.edit_message_text(f"❌ Error: {str(e)}")

async def convert_file(file_info, target_format):
    """Convert file to target format"""
    source_path = file_info['path']
    source_ext = file_info['ext']
    target_path = f"converted_{file_info['name'].split('.')[0]}.{target_format}"
    
    try:
        if source_ext == 'txt' and target_format == 'vcf':
            await convert_txt_to_vcf(source_path, target_path)
        elif source_ext == 'vcf' and target_format == 'txt':
            await convert_vcf_to_txt(source_path, target_path)
        elif source_ext in ['xls', 'xlsx'] and target_format == 'vcf':
            await convert_xls_to_vcf(source_path, target_path)
        elif source_ext == 'vcf' and target_format in ['xls', 'xlsx']:
            await convert_vcf_to_xls(source_path, target_path)
        elif source_ext == 'txt' and target_format in ['xls', 'xlsx']:
            await convert_txt_to_xls(source_path, target_path)
        elif source_ext in ['xls', 'xlsx'] and target_format == 'txt':
            await convert_xls_to_txt(source_path, target_path)
        else:
            return None
            
        return target_path if os.path.exists(target_path) else None
        
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        return None

async def convert_txt_to_vcf(source_path, target_path):
    """Convert TXT to VCF with enhanced formatting"""
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    with open(target_path, 'w', encoding='utf-8') as f:
        for i, line in enumerate(lines):
            # Parse if line contains phone/email
            parts = line.split(' - ') if ' - ' in line else [line]
            name = parts[0].strip()
            phone = parts[1].strip() if len(parts) > 1 else ""
            email = parts[2].strip() if len(parts) > 2 else ""
            
            f.write(f"BEGIN:VCARD\n")
            f.write(f"VERSION:3.0\n")
            f.write(f"FN:{name}\n")
            f.write(f"N:{name};;;;\n")
            if phone:
                f.write(f"TEL:{phone}\n")
            if email:
                f.write(f"EMAIL:{email}\n")
            f.write(f"END:VCARD\n")
            if i < len(lines) - 1:
                f.write(f"\n")

async def convert_vcf_to_txt(source_path, target_path):
    """Convert VCF to TXT with enhanced parsing"""
    contacts = await parse_vcf_file(source_path)
    
    with open(target_path, 'w', encoding='utf-8') as f:
        for contact in contacts:
            line = contact['name']
            if contact['phone']:
                line += f" - {contact['phone']}"
            if contact['email']:
                line += f" - {contact['email']}"
            f.write(line + '\n')

async def convert_xls_to_vcf(source_path, target_path):
    """Convert Excel to VCF"""
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

async def convert_vcf_to_xls(source_path, target_path):
    """Convert VCF to Excel"""
    contacts = await parse_vcf_file(source_path)
    
    df = pd.DataFrame([
        {
            'Name': contact['name'],
            'Phone': contact['phone'],
            'Email': contact['email']
        }
        for contact in contacts
    ])
    
    df.to_excel(target_path, index=False)

async def convert_txt_to_xls(source_path, target_path):
    """Convert TXT to Excel"""
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    df = pd.DataFrame(lines, columns=['Data'])
    df.to_excel(target_path, index=False)

async def convert_xls_to_txt(source_path, target_path):
    """Convert Excel to TXT"""
    df = pd.read_excel(source_path)
    
    with open(target_path, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            line = ' - '.join([str(val) for val in row.values if pd.notna(val)])
            f.write(line + '\n')

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

async def get_file_data_count(file_info):
    """Get count of data items in file"""
    try:
        if file_info['ext'] == 'txt':
            with open(file_info['path'], 'r', encoding='utf-8') as f:
                return len([line for line in f.readlines() if line.strip()])
        elif file_info['ext'] == 'vcf':
            contacts = await parse_vcf_file(file_info['path'])
            return len(contacts)
        elif file_info['ext'] in ['xls', 'xlsx']:
            df = pd.read_excel(file_info['path'])
            return len(df)
        return 0
    except:
        return 0

def get_conversion_options(source_ext):
    """Get available conversion options for source format"""
    options = {
        'txt': ['vcf', 'xls', 'xlsx'],
        'vcf': ['txt', 'xls', 'xlsx'],
        'xls': ['txt', 'vcf'],
        'xlsx': ['txt', 'vcf'],
        'csv': ['txt', 'vcf', 'xls', 'xlsx']
    }
    return options.get(source_ext, [])

async def show_formats(query):
    """Show supported formats"""
    text = """
📋 **Format File yang Didukung:**

**TXT (Text Files)**
• Plain text dengan satu data per baris
• Konversi ke: VCF, XLS, XLSX

**VCF (vCard Contact)**
• Format standar kontak
• Konversi ke: TXT, XLS, XLSX

**XLS/XLSX (Excel)**
• Spreadsheet dengan data terstruktur
• Konversi ke: TXT, VCF

**Contoh Format:**
```
TXT: John Doe - 081234567890 - john@email.com
VCF: BEGIN:VCARD...END:VCARD
XLS: Name | Phone | Email (kolom)
```

*File maksimal: 20MB*
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_stats(query, user_id):
    """Show user statistics"""
    stats = user_stats.get(user_id, {'conversions': 0})
    session = user_sessions.get(user_id)
    
    text = f"""
📊 **Statistik Anda:**

🔄 **Konversi:** {stats['conversions']}
📁 **File Aktif:** {len(session.files) if session else 0}
🎯 **Mode:** {session.current_action if session else 'None'}

**Global Stats:**
👥 **Total Users:** {len(user_stats)}
🔄 **Total Konversi:** {sum(s['conversions'] for s in user_stats.values())}
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_help(query):
    """Show comprehensive help"""
    text = """
ℹ️ **Panduan Lengkap Bot**

**🔄 Konversi Dasar:**
• Upload file → Pilih format → Download

**📝 Rename:**
• Ubah nama file hasil
• Rename kontak dalam VCF
• Auto numbering: Customer_001, 002...

**🔗 Merge (Gabung):**
• Upload multiple file
• Atur urutan penggabungan
• Remove duplikat otomatis

**✂️ Split (Pecah):**
• Bagi file jadi beberapa bagian
• Custom berapa data per file
• Auto numbering hasil

**Tips:**
💡 Gunakan format TXT: Nama - Phone - Email
💡 File VCF harus format standar vCard
💡 Excel: kolom pertama = nama kontak
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def start_from_callback(query):
    """Restart from callback"""
    user_id = query.from_user.id
    user_name = query.from_user.first_name
    
    welcome_text = f"""
🤖 **Bot Konversi File Advanced**

Halo {user_name}! Pilih aksi:

🔄 **Konversi** - TXT ↔ VCF ↔ XLS
📝 **Rename** - File & kontak
🔗 **Merge** - Gabung multiple file  
✂️ **Split** - Pecah file custom
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Konversi", callback_data="action_convert"),
            InlineKeyboardButton("📝 Rename", callback_data="action_rename")
        ],
        [
            InlineKeyboardButton("🔗 Gabung", callback_data="action_merge"),
            InlineKeyboardButton("✂️ Pecah", callback_data="action_split")
        ],
        [
            InlineKeyboardButton("📋 Format", callback_data="formats"),
            InlineKeyboardButton("📊 Stats", callback_data="stats")
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
    active_sessions = len([s for s in user_sessions.values() if s.files])
    
    admin_text = f"""
🔧 **Admin Panel - Advanced Bot**

📊 **Statistik:**
👥 Total Users: {total_users}
🔄 Total Konversi: {total_conversions}
💾 Active Sessions: {active_sessions}

**Fitur Bot:**
🔄 TXT ↔ VCF ↔ XLS konversi
📝 Rename file & kontak
🔗 Merge multiple files
✂️ Split files custom
🎯 Custom naming & ordering
"""
    
    await update.message.reply_text(admin_text, parse_mode='Markdown')

def main():
    """Main function"""
    print("🤖 Starting Advanced TXT/VCF/XLS Converter Bot...")
    
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
    
    print("✅ Advanced Bot started!")
    print(f"👑 Admin ID: {ADMIN_USER_ID}")
    print("🔄 Features: Convert, Rename, Merge, Split")
    print("📝 Supported: TXT, VCF, XLS, XLSX")
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()