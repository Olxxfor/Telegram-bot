#!/usr/bin/env python3
"""
Advanced Handlers untuk fitur rename, merge, split
"""

import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import pandas as pd

async def handle_rename_process(query, session, data):
    """Handle rename process"""
    parts = data.split('_')
    action_type = parts[1]  # file, data, both, auto
    file_index = int(parts[2])
    
    if file_index >= len(session.files):
        await query.edit_message_text("❌ File tidak ditemukan.")
        return
    
    file_info = session.files[file_index]
    
    if action_type == "file":
        await handle_file_rename_only(query, session, file_info)
    elif action_type == "data":
        await handle_data_rename_only(query, session, file_info)
    elif action_type == "both":
        await handle_both_rename(query, session, file_info)
    elif action_type == "auto":
        await handle_auto_numbering(query, session, file_info)

async def handle_file_rename_only(query, session, file_info):
    """Handle file rename only"""
    text = f"""
📁 **Rename File: {file_info['name']}**

Kirim nama file baru (tanpa ekstensi):

**Contoh:**
• `contacts_2024`
• `customer_list`
• `backup_kontak`

Format file akan tetap: `.{file_info['ext']}`
"""
    
    session.temp_data['rename_mode'] = 'file_only'
    session.temp_data['target_file'] = file_info
    
    await query.edit_message_text(text, parse_mode='Markdown')

async def handle_data_rename_only(query, session, file_info):
    """Handle data/contact rename only"""
    data_count = await get_file_data_count(file_info)
    
    text = f"""
👤 **Rename Data/Kontak: {file_info['name']}**
📊 **Total data:** {data_count} items

**Pilih pattern nama:**
"""
    
    keyboard = [
        [InlineKeyboardButton("🔢 Customer_001, 002...", callback_data=f"pattern_customer_{file_info['index']}")],
        [InlineKeyboardButton("👥 Contact_001, 002...", callback_data=f"pattern_contact_{file_info['index']}")],
        [InlineKeyboardButton("🏢 Client_001, 002...", callback_data=f"pattern_client_{file_info['index']}")],
        [InlineKeyboardButton("📝 Custom Pattern", callback_data=f"pattern_custom_{file_info['index']}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_auto_numbering(query, session, file_info):
    """Handle auto numbering"""
    data_count = await get_file_data_count(file_info)
    
    await query.edit_message_text("🔢 Melakukan auto numbering...")
    
    try:
        result_file = await apply_auto_numbering(file_info, "Contact")
        
        if result_file:
            with open(result_file, 'rb') as f:
                filename = f"numbered_{file_info['name']}"
                await query.message.reply_document(
                    document=f,
                    filename=filename,
                    caption=f"✅ Auto numbering berhasil!\n📊 {data_count} data dinomori otomatis"
                )
            
            os.remove(result_file)
            await query.edit_message_text(f"✅ Auto numbering selesai! {data_count} data berhasil dinomori.")
        else:
            await query.edit_message_text("❌ Gagal melakukan auto numbering.")
            
    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)}")

async def apply_auto_numbering(file_info, prefix="Contact"):
    """Apply auto numbering to file data"""
    source_path = file_info['path']
    target_path = f"numbered_{file_info['name']}"
    
    try:
        if file_info['ext'] == 'txt':
            await number_txt_file(source_path, target_path, prefix)
        elif file_info['ext'] == 'vcf':
            await number_vcf_file(source_path, target_path, prefix)
        elif file_info['ext'] in ['xls', 'xlsx']:
            await number_excel_file(source_path, target_path, prefix)
            
        return target_path if os.path.exists(target_path) else None
        
    except Exception as e:
        return None

async def number_txt_file(source_path, target_path, prefix):
    """Add numbering to TXT file"""
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    with open(target_path, 'w', encoding='utf-8') as f:
        for i, line in enumerate(lines):
            # If line has format "Name - Phone - Email", replace name
            parts = line.split(' - ') if ' - ' in line else [line]
            new_name = f"{prefix}_{i+1:03d}"
            
            if len(parts) > 1:
                f.write(f"{new_name} - {' - '.join(parts[1:])}\n")
            else:
                f.write(f"{new_name}\n")

async def number_vcf_file(source_path, target_path, prefix):
    """Add numbering to VCF file"""
    from advanced_bot import parse_vcf_file
    
    contacts = await parse_vcf_file(source_path)
    
    with open(target_path, 'w', encoding='utf-8') as f:
        for i, contact in enumerate(contacts):
            new_name = f"{prefix}_{i+1:03d}"
            
            f.write(f"BEGIN:VCARD\n")
            f.write(f"VERSION:3.0\n")
            f.write(f"FN:{new_name}\n")
            f.write(f"N:{new_name};;;;\n")
            if contact['phone']:
                f.write(f"TEL:{contact['phone']}\n")
            if contact['email']:
                f.write(f"EMAIL:{contact['email']}\n")
            f.write(f"END:VCARD\n")
            if i < len(contacts) - 1:
                f.write(f"\n")

async def number_excel_file(source_path, target_path, prefix):
    """Add numbering to Excel file"""
    df = pd.read_excel(source_path)
    
    # Replace first column (assumed to be names) with numbered names
    for i in range(len(df)):
        df.iloc[i, 0] = f"{prefix}_{i+1:03d}"
    
    df.to_excel(target_path, index=False)

async def handle_merge_process(query, session, data):
    """Handle merge process"""
    action = data.replace('merge_', '')
    
    if action == "start":
        await start_merge_process(query, session)
    elif action == "order":
        await handle_merge_order(query, session)
    elif action == "add":
        await query.edit_message_text("📎 Upload file berikutnya untuk merge...")
    elif action == "reset":
        session.merge_files = []
        await query.edit_message_text("🗑️ File list direset. Upload file pertama untuk merge.")

async def start_merge_process(query, session):
    """Start the actual merge process"""
    if len(session.merge_files) < 2:
        await query.edit_message_text("❌ Minimal 2 file untuk merge.")
        return
    
    text = f"""
🔗 **Mulai Merge {len(session.merge_files)} Files**

**Files:**
"""
    
    for i, f in enumerate(session.merge_files):
        text += f"\n{i+1}. {f['name']} ({f['ext'].upper()})"
    
    text += f"\n\n**Nama file hasil:**"
    
    keyboard = [
        [InlineKeyboardButton("📝 Custom Nama", callback_data="merge_custom_name")],
        [InlineKeyboardButton("⚡ Auto Generate", callback_data="merge_auto_name")],
        [InlineKeyboardButton("🔄 Proses Langsung", callback_data="merge_process_now")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_split_process(query, session, data):
    """Handle split process"""
    parts = data.split('_')
    action = parts[1]  # equal, custom, quick
    file_index = int(parts[2])
    
    if file_index >= len(session.files):
        await query.edit_message_text("❌ File tidak ditemukan.")
        return
    
    file_info = session.files[file_index]
    data_count = await get_file_data_count(file_info)
    
    if action == "equal":
        await handle_equal_split(query, session, file_info, data_count)
    elif action == "custom":
        await handle_custom_split(query, session, file_info, data_count)
    elif action == "quick":
        await handle_quick_split(query, session, file_info, data_count)

async def handle_equal_split(query, session, file_info, data_count):
    """Handle equal split"""
    text = f"""
🔢 **Split Equal: {file_info['name']}**
📊 **Total data:** {data_count}

**Pilih jumlah file hasil:**
"""
    
    suggested_splits = []
    for split_count in [2, 3, 4, 5, 10]:
        per_file = data_count // split_count
        if per_file > 0:
            suggested_splits.append(f"{split_count} file ({per_file} data/file)")
    
    keyboard = []
    for i, split_info in enumerate(suggested_splits[:4]):
        split_count = [2, 3, 4, 5, 10][i]
        keyboard.append([InlineKeyboardButton(
            split_info, 
            callback_data=f"split_execute_equal_{file_info['index']}_{split_count}"
        )])
    
    keyboard.append([InlineKeyboardButton("📝 Custom Jumlah", callback_data=f"split_equal_custom_{file_info['index']}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_custom_split(query, session, file_info, data_count):
    """Handle custom split"""
    text = f"""
📝 **Split Custom: {file_info['name']}**
📊 **Total data:** {data_count}

**Pilih cara custom split:**
"""
    
    keyboard = [
        [InlineKeyboardButton("🔢 Per jumlah data (ex: 10,20,30)", callback_data=f"split_custom_count_{file_info['index']}")],
        [InlineKeyboardButton("📋 Per list range", callback_data=f"split_custom_range_{file_info['index']}")],
        [InlineKeyboardButton("⚡ Quick preset", callback_data=f"split_custom_preset_{file_info['index']}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_quick_split(query, session, file_info, data_count):
    """Handle quick split with presets"""
    await query.edit_message_text("⚡ Melakukan quick split...")
    
    # Quick split into chunks of 100 or data_count/5, whichever is smaller
    chunk_size = min(100, max(1, data_count // 5))
    
    try:
        result_files = await split_file_by_size(file_info, chunk_size)
        
        if result_files:
            await query.edit_message_text(f"✅ Quick split berhasil! {len(result_files)} file dibuat.")
            
            # Send all result files
            for i, result_file in enumerate(result_files):
                with open(result_file, 'rb') as f:
                    filename = f"split_{i+1:02d}_{file_info['name']}"
                    await query.message.reply_document(
                        document=f,
                        filename=filename,
                        caption=f"📁 File {i+1}/{len(result_files)}"
                    )
                os.remove(result_file)
        else:
            await query.edit_message_text("❌ Gagal melakukan split.")
            
    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)}")

async def split_file_by_size(file_info, chunk_size):
    """Split file by chunk size"""
    source_path = file_info['path']
    result_files = []
    
    try:
        if file_info['ext'] == 'txt':
            result_files = await split_txt_file(source_path, chunk_size, file_info)
        elif file_info['ext'] == 'vcf':
            result_files = await split_vcf_file(source_path, chunk_size, file_info)
        elif file_info['ext'] in ['xls', 'xlsx']:
            result_files = await split_excel_file(source_path, chunk_size, file_info)
            
        return result_files
        
    except Exception as e:
        return []

async def split_txt_file(source_path, chunk_size, file_info):
    """Split TXT file into chunks"""
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    result_files = []
    
    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i + chunk_size]
        chunk_file = f"split_{i//chunk_size + 1:02d}_{file_info['name']}"
        
        with open(chunk_file, 'w', encoding='utf-8') as f:
            for line in chunk_lines:
                f.write(line + '\n')
                
        result_files.append(chunk_file)
    
    return result_files

async def split_vcf_file(source_path, chunk_size, file_info):
    """Split VCF file into chunks"""
    from advanced_bot import parse_vcf_file
    
    contacts = await parse_vcf_file(source_path)
    result_files = []
    
    for i in range(0, len(contacts), chunk_size):
        chunk_contacts = contacts[i:i + chunk_size]
        chunk_file = f"split_{i//chunk_size + 1:02d}_{file_info['name']}"
        
        with open(chunk_file, 'w', encoding='utf-8') as f:
            for j, contact in enumerate(chunk_contacts):
                f.write(f"BEGIN:VCARD\n")
                f.write(f"VERSION:3.0\n")
                f.write(f"FN:{contact['name']}\n")
                f.write(f"N:{contact['name']};;;;\n")
                if contact['phone']:
                    f.write(f"TEL:{contact['phone']}\n")
                if contact['email']:
                    f.write(f"EMAIL:{contact['email']}\n")
                f.write(f"END:VCARD\n")
                if j < len(chunk_contacts) - 1:
                    f.write(f"\n")
                    
        result_files.append(chunk_file)
    
    return result_files

async def split_excel_file(source_path, chunk_size, file_info):
    """Split Excel file into chunks"""
    df = pd.read_excel(source_path)
    result_files = []
    
    for i in range(0, len(df), chunk_size):
        chunk_df = df.iloc[i:i + chunk_size]
        chunk_file = f"split_{i//chunk_size + 1:02d}_{file_info['name']}"
        
        chunk_df.to_excel(chunk_file, index=False)
        result_files.append(chunk_file)
    
    return result_files

# Import get_file_data_count from advanced_bot if needed
from advanced_bot import get_file_data_count