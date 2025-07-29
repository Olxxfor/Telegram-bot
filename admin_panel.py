#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin Panel untuk Contact Manager System
Mengelola user premium dan pengaturan sistem
"""

import sqlite3
import json
import datetime
import hashlib
from contact_manager import ContactManager

class AdminPanel:
    def __init__(self):
        self.manager = ContactManager()
        self.db_path = "contact_manager.db"
    
    def add_premium_user(self, username: str, email: str, duration_days: int, features: list):
        """Add new premium user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=duration_days)
        features_json = json.dumps(features)
        
        try:
            cursor.execute('''
                INSERT INTO premium_users (username, email, premium_expiry, features, created_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, expiry_date.isoformat(), features_json, datetime.datetime.now().isoformat()))
            
            conn.commit()
            print(f"✓ Premium user {username} berhasil ditambahkan")
            print(f"  Expiry: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Features: {', '.join(features)}")
            
        except sqlite3.IntegrityError:
            print(f"✗ Username {username} sudah ada!")
        finally:
            conn.close()
    
    def extend_premium(self, username: str, additional_days: int):
        """Extend premium subscription"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT premium_expiry FROM premium_users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if result:
            current_expiry = datetime.datetime.fromisoformat(result[0])
            new_expiry = current_expiry + datetime.timedelta(days=additional_days)
            
            cursor.execute('UPDATE premium_users SET premium_expiry = ? WHERE username = ?', 
                         (new_expiry.isoformat(), username))
            conn.commit()
            
            print(f"✓ Premium {username} diperpanjang sampai {new_expiry.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"✗ User {username} tidak ditemukan!")
        
        conn.close()
    
    def revoke_premium(self, username: str):
        """Revoke premium status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM premium_users WHERE username = ?', (username,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"✓ Premium {username} berhasil dicabut")
        else:
            print(f"✗ User {username} tidak ditemukan!")
        
        conn.close()
    
    def list_premium_users(self):
        """List all premium users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, email, premium_expiry, features FROM premium_users')
        users = cursor.fetchall()
        
        print("\n=== Premium Users ===")
        if not users:
            print("Tidak ada user premium")
        else:
            for user in users:
                username, email, expiry, features = user
                expiry_date = datetime.datetime.fromisoformat(expiry)
                is_expired = datetime.datetime.now() > expiry_date
                status = "EXPIRED" if is_expired else "ACTIVE"
                
                print(f"\nUsername: {username}")
                print(f"Email: {email}")
                print(f"Expiry: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Status: {status}")
                print(f"Features: {features}")
        
        conn.close()
    
    def list_expired_users(self):
        """List expired premium users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, email, premium_expiry FROM premium_users')
        users = cursor.fetchall()
        
        expired_users = []
        for user in users:
            username, email, expiry = user
            expiry_date = datetime.datetime.fromisoformat(expiry)
            if datetime.datetime.now() > expiry_date:
                expired_users.append((username, email, expiry_date))
        
        print("\n=== Expired Premium Users ===")
        if not expired_users:
            print("Tidak ada user yang expired")
        else:
            for username, email, expiry_date in expired_users:
                print(f"\nUsername: {username}")
                print(f"Email: {email}")
                print(f"Expired: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        conn.close()
    
    def add_admin(self, username: str, password: str, role: str = "admin"):
        """Add new admin user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor.execute('''
                INSERT INTO admins (username, password_hash, role, created_date)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, role, datetime.datetime.now().isoformat()))
            
            conn.commit()
            print(f"✓ Admin {username} berhasil ditambahkan dengan role {role}")
            
        except sqlite3.IntegrityError:
            print(f"✗ Username {username} sudah ada!")
        finally:
            conn.close()
    
    def system_stats(self):
        """Show system statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count premium users
        cursor.execute('SELECT COUNT(*) FROM premium_users')
        total_premium = cursor.fetchone()[0]
        
        # Count active premium users
        cursor.execute('SELECT COUNT(*) FROM premium_users WHERE premium_expiry > ?', 
                      (datetime.datetime.now().isoformat(),))
        active_premium = cursor.fetchone()[0]
        
        # Count admins
        cursor.execute('SELECT COUNT(*) FROM admins')
        total_admins = cursor.fetchone()[0]
        
        conn.close()
        
        print("\n=== System Statistics ===")
        print(f"Total Premium Users: {total_premium}")
        print(f"Active Premium Users: {active_premium}")
        print(f"Expired Premium Users: {total_premium - active_premium}")
        print(f"Total Admins: {total_admins}")

def main():
    panel = AdminPanel()
    
    print("=== Admin Panel ===")
    print("1. Add Premium User")
    print("2. Extend Premium")
    print("3. Revoke Premium")
    print("4. List Premium Users")
    print("5. List Expired Users")
    print("6. Add Admin")
    print("7. System Stats")
    print("8. Exit")
    
    while True:
        choice = input("\nPilih menu (1-8): ").strip()
        
        if choice == "1":
            username = input("Username: ")
            email = input("Email: ")
            duration = int(input("Duration (days): "))
            features_input = input("Features (pisahkan dengan koma): ")
            features = [f.strip() for f in features_input.split(',')]
            
            panel.add_premium_user(username, email, duration, features)
        
        elif choice == "2":
            username = input("Username: ")
            days = int(input("Additional days: "))
            panel.extend_premium(username, days)
        
        elif choice == "3":
            username = input("Username: ")
            panel.revoke_premium(username)
        
        elif choice == "4":
            panel.list_premium_users()
        
        elif choice == "5":
            panel.list_expired_users()
        
        elif choice == "6":
            username = input("Username: ")
            password = input("Password: ")
            role = input("Role (admin/super_admin): ") or "admin"
            panel.add_admin(username, password, role)
        
        elif choice == "7":
            panel.system_stats()
        
        elif choice == "8":
            print("Terima kasih!")
            break
        
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()