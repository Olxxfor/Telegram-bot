#!/usr/bin/env python3
"""
Bot Status Monitoring Script
Check if the Telegram bot is running and display status
"""

import os
import subprocess
import asyncio
from dotenv import load_dotenv
from datetime import datetime

def check_bot_process():
    """Check if bot process is running"""
    try:
        result = subprocess.run(['pgrep', '-f', 'simple_bot.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pid = result.stdout.strip()
            return True, pid
        return False, None
    except Exception as e:
        return False, str(e)

def get_bot_info():
    """Get bot configuration info"""
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN', 'Not configured')
    admin_id = os.getenv('ADMIN_USER_ID', 'Not configured')
    
    return {
        'token': bot_token[:10] + '...' if bot_token != 'Not configured' else 'Not configured',
        'admin_id': admin_id
    }

def get_log_tail():
    """Get last few lines of bot log"""
    try:
        if os.path.exists('bot.log'):
            result = subprocess.run(['tail', '-5', 'bot.log'], 
                                  capture_output=True, text=True)
            return result.stdout
        return "Log file not found"
    except Exception as e:
        return f"Error reading log: {e}"

def main():
    """Main status check function"""
    print("🤖 Telegram File Converter Bot - Status Check")
    print("=" * 50)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check bot process
    is_running, pid = check_bot_process()
    
    if is_running:
        print("✅ Bot Status: RUNNING")
        print(f"🆔 Process ID: {pid}")
    else:
        print("❌ Bot Status: NOT RUNNING")
        print("💡 Use 'bash start_bot.sh' to start the bot")
    
    print()
    
    # Show bot configuration
    info = get_bot_info()
    print("⚙️ Configuration:")
    print(f"🔑 Bot Token: {info['token']}")
    print(f"👑 Admin ID: {info['admin_id']}")
    print()
    
    # Show recent logs
    print("📋 Recent Logs:")
    print("-" * 30)
    print(get_log_tail())
    
    if is_running:
        print()
        print("🎉 Bot is ready to receive messages!")
        print("📱 Go to @EliteConvertVip_bot on Telegram to test")
        print()
        print("Commands to try:")
        print("• /start - Welcome message")
        print("• /help - Help information") 
        print("• /admin - Admin panel (admin only)")
        print("• Send a photo to test conversion")

if __name__ == '__main__':
    main()