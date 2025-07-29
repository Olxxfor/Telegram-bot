#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TXT to VCF File Splitter
Mengkonversi file txt ke vcf dengan pembagian file otomatis
Format: OLXX-REXX-81-50
- OLXX: nama kontak (bisa ditambah angka belakang)
- REXX: nama file (bisa ditambah angka belakang)
- 81: urutan file
- 50: jumlah kontak per file
"""

import os
import sys
import re
from typing import List, Tuple

def parse_input_format(input_str: str) -> Tuple[str, str, int, int]:
    """
    Parse input format: OLXX-REXX-81-50
    Returns: (contact_name, file_name, start_number, contacts_per_file)
    """
    try:
        parts = input_str.split('-')
        if len(parts) != 4:
            raise ValueError("Format harus: OLXX-REXX-81-50")
        
        contact_name = parts[0]
        file_name = parts[1]
        start_number = int(parts[2])
        contacts_per_file = int(parts[3])
        
        return contact_name, file_name, start_number, contacts_per_file
    except ValueError as e:
        print(f"Error parsing input: {e}")
        sys.exit(1)

def read_txt_file(filename: str) -> List[str]:
    """
    Membaca file txt dan mengembalikan list nomor telepon
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Bersihkan dan filter nomor telepon
        phone_numbers = []
        for line in lines:
            line = line.strip()
            if line:
                # Hapus karakter non-digit kecuali + dan -
                cleaned = re.sub(r'[^\d+\-]', '', line)
                if cleaned:
                    phone_numbers.append(cleaned)
        
        return phone_numbers
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan!")
        sys.exit(1)
    except Exception as e:
        print(f"Error membaca file: {e}")
        sys.exit(1)

def create_vcf_content(contact_name: str, phone_numbers: List[str], start_index: int) -> str:
    """
    Membuat konten VCF dari list nomor telepon
    """
    vcf_content = ""
    
    for i, phone in enumerate(phone_numbers):
        contact_number = start_index + i
        vcf_content += f"""BEGIN:VCARD
VERSION:3.0
FN:{contact_name}{contact_number}
TEL;TYPE=CELL:{phone}
END:VCARD

"""
    
    return vcf_content

def split_and_create_vcf_files(contact_name: str, file_name: str, start_number: int, 
                              contacts_per_file: int, phone_numbers: List[str]):
    """
    Membagi nomor telepon dan membuat file VCF terpisah
    """
    total_contacts = len(phone_numbers)
    file_counter = start_number
    
    for i in range(0, total_contacts, contacts_per_file):
        # Ambil batch nomor telepon
        batch_numbers = phone_numbers[i:i + contacts_per_file]
        
        # Buat nama file VCF
        vcf_filename = f"{contact_name}-{file_counter}.vcf"
        
        # Buat konten VCF
        vcf_content = create_vcf_content(file_name, batch_numbers, i + 1)
        
        # Tulis ke file
        try:
            with open(vcf_filename, 'w', encoding='utf-8') as f:
                f.write(vcf_content)
            print(f"✓ File {vcf_filename} berhasil dibuat dengan {len(batch_numbers)} kontak")
        except Exception as e:
            print(f"✗ Error membuat file {vcf_filename}: {e}")
        
        file_counter += 1

def main():
    print("=== TXT to VCF File Splitter ===")
    print("Format input: OLXX-REXX-81-50")
    print("Contoh: OLXX-REXX-81-50")
    print()
    
    # Input dari user
    input_format = input("Masukkan format (OLXX-REXX-81-50): ").strip()
    txt_filename = input("Masukkan nama file txt: ").strip()
    
    # Parse input format
    contact_name, file_name, start_number, contacts_per_file = parse_input_format(input_format)
    
    print(f"\nKonfigurasi:")
    print(f"- Nama kontak: {contact_name}")
    print(f"- Nama file: {file_name}")
    print(f"- Mulai dari file: {start_number}")
    print(f"- Kontak per file: {contacts_per_file}")
    print()
    
    # Baca file txt
    print("Membaca file txt...")
    phone_numbers = read_txt_file(txt_filename)
    print(f"✓ Ditemukan {len(phone_numbers)} nomor telepon")
    
    # Buat file VCF
    print("\nMembuat file VCF...")
    split_and_create_vcf_files(contact_name, file_name, start_number, contacts_per_file, phone_numbers)
    
    print(f"\n✓ Selesai! Total {len(phone_numbers)} kontak telah dibagi ke dalam file VCF")

if __name__ == "__main__":
    main()