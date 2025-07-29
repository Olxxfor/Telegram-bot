#!/usr/bin/env python3
import sys
import re

def split_vcf(input_format, txt_file):
    """Split VCF files based on input format OLXX-REXX-81-50"""
    
    # Parse input format
    parts = input_format.split('-')
    if len(parts) != 4:
        print("Format salah! Gunakan: OLXX-REXX-81-50")
        return
    
    contact_name = parts[0]  # OLXX
    file_name = parts[1]     # REXX  
    start_file = int(parts[2])  # 81
    contacts_per_file = int(parts[3])  # 50
    
    # Read phone numbers from txt file
    try:
        with open(txt_file, 'r') as f:
            numbers = [line.strip() for line in f if line.strip()]
    except:
        print(f"File {txt_file} tidak ditemukan!")
        return
    
    total_numbers = len(numbers)
    file_counter = start_file
    
    # Create VCF files
    for i in range(0, total_numbers, contacts_per_file):
        batch = numbers[i:i + contacts_per_file]
        vcf_filename = f"{contact_name}-{file_counter}.vcf"
        
        vcf_content = ""
        for j, phone in enumerate(batch):
            contact_num = i + j + 1
            vcf_content += f"""BEGIN:VCARD
VERSION:3.0
FN:{file_name}{contact_num}
TEL;TYPE=CELL:{phone}
END:VCARD

"""
        
        with open(vcf_filename, 'w') as f:
            f.write(vcf_content)
        
        print(f"✓ {vcf_filename} - {len(batch)} kontak")
        file_counter += 1
    
    print(f"\nSelesai! Total {total_numbers} kontak dibagi ke {file_counter - start_file} file")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Cara pakai: python vcf_splitter.py 'OLXX-REXX-81-50' file.txt")
        sys.exit(1)
    
    input_format = sys.argv[1]
    txt_file = sys.argv[2]
    
    split_vcf(input_format, txt_file)