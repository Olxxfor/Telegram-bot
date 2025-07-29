#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contact Manager System
Fitur lengkap untuk manajemen kontak dengan sistem admin dan premium
"""

import os
import sys
import re
import json
import hashlib
import datetime
import pandas as pd
from typing import List, Dict, Set, Tuple
import sqlite3
from pathlib import Path

class ContactManager:
    def __init__(self):
        self.db_path = "contact_manager.db"
        self.config_path = "config.json"
        self.init_database()
        self.load_config()
    
    def init_database(self):
        """Initialize database for admin and premium management"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Admin table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT,
                role TEXT,
                created_date TEXT
            )
        ''')
        
        # Premium users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS premium_users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT,
                premium_expiry TEXT,
                features TEXT,
                created_date TEXT
            )
        ''')
        
        # Default admin
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO admins (username, password_hash, role, created_date)
            VALUES (?, ?, ?, ?)
        ''', ("admin", admin_hash, "super_admin", datetime.datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def load_config(self):
        """Load configuration file"""
        default_config = {
            "max_file_size": 10485760,  # 10MB
            "allowed_extensions": [".txt", ".vcf", ".xls", ".xlsx"],
            "premium_features": ["duplicate_detection", "bulk_operations", "advanced_export"],
            "free_limits": {
                "max_contacts": 1000,
                "max_files": 5
            }
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
    
    def login(self, username: str, password: str) -> bool:
        """Admin login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('SELECT role FROM admins WHERE username = ? AND password_hash = ?', 
                      (username, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.current_user = username
            self.user_role = result[0]
            return True
        return False
    
    def check_premium_status(self, username: str) -> Dict:
        """Check premium status and features"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT premium_expiry, features FROM premium_users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            expiry_date = datetime.datetime.fromisoformat(result[0])
            is_expired = datetime.datetime.now() > expiry_date
            features = json.loads(result[1]) if result[1] else []
            
            return {
                "is_premium": not is_expired,
                "expiry_date": expiry_date,
                "features": features,
                "is_expired": is_expired
            }
        
        return {"is_premium": False, "features": [], "is_expired": False}
    
    def vcf_to_txt(self, vcf_file: str, output_file: str = None) -> str:
        """Convert VCF to TXT format"""
        if not output_file:
            output_file = vcf_file.replace('.vcf', '.txt')
        
        phone_numbers = []
        
        with open(vcf_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract phone numbers from VCF
        vcf_entries = content.split('BEGIN:VCARD')
        
        for entry in vcf_entries:
            if 'TEL;' in entry:
                tel_match = re.search(r'TEL[^:]*:(.+)', entry)
                if tel_match:
                    phone = tel_match.group(1).strip()
                    phone_numbers.append(phone)
        
        # Write to TXT file
        with open(output_file, 'w', encoding='utf-8') as f:
            for phone in phone_numbers:
                f.write(f"{phone}\n")
        
        return output_file
    
    def xls_to_vcf(self, xls_file: str, output_file: str = None) -> str:
        """Convert XLS/XLSX to VCF format"""
        if not output_file:
            output_file = xls_file.replace('.xlsx', '.vcf').replace('.xls', '.vcf')
        
        try:
            df = pd.read_excel(xls_file)
            vcf_content = ""
            
            # Assume first column is name, second is phone
            for index, row in df.iterrows():
                name = str(row.iloc[0]) if len(row) > 0 else f"Contact{index+1}"
                phone = str(row.iloc[1]) if len(row) > 1 else ""
                
                if phone and phone != "nan":
                    vcf_content += f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL;TYPE=CELL:{phone}
END:VCARD

"""
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(vcf_content)
            
            return output_file
        except Exception as e:
            print(f"Error converting XLS: {e}")
            return None
    
    def split_file(self, input_file: str, format_str: str) -> List[str]:
        """Split file based on format OLXX-REXX-81-50"""
        parts = format_str.split('-')
        if len(parts) != 4:
            raise ValueError("Format harus: OLXX-REXX-81-50")
        
        contact_name = parts[0]
        file_name = parts[1]
        start_file = int(parts[2])
        contacts_per_file = int(parts[3])
        
        # Read input file
        if input_file.endswith('.vcf'):
            phone_numbers = self.extract_phones_from_vcf(input_file)
        elif input_file.endswith('.txt'):
            with open(input_file, 'r') as f:
                phone_numbers = [line.strip() for line in f if line.strip()]
        elif input_file.endswith(('.xls', '.xlsx')):
            phone_numbers = self.extract_phones_from_xls(input_file)
        else:
            raise ValueError("Format file tidak didukung")
        
        created_files = []
        file_counter = start_file
        
        for i in range(0, len(phone_numbers), contacts_per_file):
            batch = phone_numbers[i:i + contacts_per_file]
            output_file = f"{contact_name}-{file_counter}.vcf"
            
            vcf_content = ""
            for j, phone in enumerate(batch):
                contact_num = i + j + 1
                vcf_content += f"""BEGIN:VCARD
VERSION:3.0
FN:{file_name}{contact_num}
TEL;TYPE=CELL:{phone}
END:VCARD

"""
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(vcf_content)
            
            created_files.append(output_file)
            file_counter += 1
        
        return created_files
    
    def merge_files(self, file_list: List[str], output_file: str) -> str:
        """Merge multiple VCF/TXT files into one"""
        all_contacts = []
        
        for file_path in file_list:
            if file_path.endswith('.vcf'):
                contacts = self.extract_phones_from_vcf(file_path)
            elif file_path.endswith('.txt'):
                with open(file_path, 'r') as f:
                    contacts = [line.strip() for line in f if line.strip()]
            else:
                continue
            
            all_contacts.extend(contacts)
        
        # Remove duplicates if premium
        if self.check_premium_status(self.current_user)["is_premium"]:
            all_contacts = list(set(all_contacts))
        
        # Write merged file
        if output_file.endswith('.vcf'):
            vcf_content = ""
            for i, phone in enumerate(all_contacts):
                vcf_content += f"""BEGIN:VCARD
VERSION:3.0
FN:Contact{i+1}
TEL;TYPE=CELL:{phone}
END:VCARD

"""
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(vcf_content)
        else:
            with open(output_file, 'w') as f:
                for phone in all_contacts:
                    f.write(f"{phone}\n")
        
        return output_file
    
    def rename_files_and_contacts(self, pattern: str, new_name: str, file_list: List[str]):
        """Rename files and contacts inside"""
        renamed_files = []
        
        for i, file_path in enumerate(file_list):
            if file_path.endswith('.vcf'):
                # Read and modify VCF content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace contact names
                new_content = re.sub(r'FN:[^\n]+', f'FN:{new_name}{i+1}', content)
                
                # Create new filename
                new_filename = f"{new_name}-{i+1}.vcf"
                
                with open(new_filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                renamed_files.append(new_filename)
        
        return renamed_files
    
    def detect_duplicates(self, file_path: str) -> Dict:
        """Detect duplicate contacts in file"""
        if not self.check_premium_status(self.current_user)["is_premium"]:
            return {"error": "Fitur ini memerlukan premium"}
        
        phone_numbers = []
        
        if file_path.endswith('.vcf'):
            phone_numbers = self.extract_phones_from_vcf(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                phone_numbers = [line.strip() for line in f if line.strip()]
        
        # Find duplicates
        seen = set()
        duplicates = set()
        
        for phone in phone_numbers:
            if phone in seen:
                duplicates.add(phone)
            else:
                seen.add(phone)
        
        return {
            "total_contacts": len(phone_numbers),
            "unique_contacts": len(seen),
            "duplicate_count": len(duplicates),
            "duplicates": list(duplicates)
        }
    
    def extract_phones_from_vcf(self, vcf_file: str) -> List[str]:
        """Extract phone numbers from VCF file"""
        with open(vcf_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        phone_numbers = []
        vcf_entries = content.split('BEGIN:VCARD')
        
        for entry in vcf_entries:
            if 'TEL;' in entry:
                tel_match = re.search(r'TEL[^:]*:(.+)', entry)
                if tel_match:
                    phone = tel_match.group(1).strip()
                    phone_numbers.append(phone)
        
        return phone_numbers
    
    def extract_phones_from_xls(self, xls_file: str) -> List[str]:
        """Extract phone numbers from XLS file"""
        df = pd.read_excel(xls_file)
        phone_numbers = []
        
        for index, row in df.iterrows():
            if len(row) > 1:
                phone = str(row.iloc[1])
                if phone and phone != "nan":
                    phone_numbers.append(phone)
        
        return phone_numbers

def main():
    manager = ContactManager()
    
    print("=== Contact Manager System ===")
    print("1. Login Admin")
    print("2. VCF to TXT")
    print("3. XLS to VCF")
    print("4. Split File")
    print("5. Merge Files")
    print("6. Rename Files & Contacts")
    print("7. Detect Duplicates")
    print("8. Check Premium Status")
    print("9. Exit")
    
    while True:
        choice = input("\nPilih menu (1-9): ").strip()
        
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if manager.login(username, password):
                print("✓ Login berhasil!")
            else:
                print("✗ Login gagal!")
        
        elif choice == "2":
            vcf_file = input("Masukkan file VCF: ")
            output = manager.vcf_to_txt(vcf_file)
            print(f"✓ File berhasil dikonversi: {output}")
        
        elif choice == "3":
            xls_file = input("Masukkan file XLS: ")
            output = manager.xls_to_vcf(xls_file)
            if output:
                print(f"✓ File berhasil dikonversi: {output}")
        
        elif choice == "4":
            input_file = input("Masukkan file input: ")
            format_str = input("Masukkan format (OLXX-REXX-81-50): ")
            try:
                files = manager.split_file(input_file, format_str)
                print(f"✓ Berhasil membuat {len(files)} file")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        elif choice == "5":
            file_list = input("Masukkan file (pisahkan dengan koma): ").split(',')
            output_file = input("Masukkan nama file output: ")
            output = manager.merge_files([f.strip() for f in file_list], output_file)
            print(f"✓ File berhasil digabung: {output}")
        
        elif choice == "6":
            file_list = input("Masukkan file (pisahkan dengan koma): ").split(',')
            new_name = input("Masukkan nama baru: ")
            files = manager.rename_files_and_contacts("", new_name, [f.strip() for f in file_list])
            print(f"✓ Berhasil rename {len(files)} file")
        
        elif choice == "7":
            file_path = input("Masukkan file: ")
            result = manager.detect_duplicates(file_path)
            if "error" in result:
                print(f"✗ {result['error']}")
            else:
                print(f"Total: {result['total_contacts']}")
                print(f"Unique: {result['unique_contacts']}")
                print(f"Duplicates: {result['duplicate_count']}")
        
        elif choice == "8":
            username = input("Masukkan username: ")
            status = manager.check_premium_status(username)
            print(f"Premium: {status['is_premium']}")
            if status['is_premium']:
                print(f"Expiry: {status['expiry_date']}")
                print(f"Features: {', '.join(status['features'])}")
        
        elif choice == "9":
            print("Terima kasih!")
            break
        
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()