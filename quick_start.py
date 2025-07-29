#!/usr/bin/env python3
"""
Quick Start Script for Telegram File Converter Bot
Test bot configuration and basic functionality
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    # Load .env file
    load_dotenv()
    
    # Check bot token
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token or bot_token == 'YOUR_BOT_TOKEN_HERE':
        print("❌ BOT_TOKEN not configured in .env file")
        return False
    else:
        print(f"✅ BOT_TOKEN configured: {bot_token[:10]}...")
    
    # Check admin ID
    admin_id = os.getenv('ADMIN_USER_ID')
    if admin_id:
        print(f"✅ ADMIN_USER_ID configured: {admin_id}")
    else:
        print("⚠️  ADMIN_USER_ID not configured")
    
    # Check directories
    temp_dir = os.getenv('TEMP_DIR', './temp')
    if os.path.exists(temp_dir):
        print(f"✅ Temp directory exists: {temp_dir}")
    else:
        print(f"⚠️  Creating temp directory: {temp_dir}")
        os.makedirs(temp_dir, exist_ok=True)
    
    print("✅ Environment check completed")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking Python dependencies...")
    
    required_packages = {
        'telegram': 'python-telegram-bot',
        'PIL': 'Pillow',
        'PyPDF2': 'PyPDF2',
        'docx': 'python-docx',
        'reportlab': 'reportlab',
        'rarfile': 'rarfile',
        'dotenv': 'python-dotenv'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name} - NOT FOUND")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def check_system_tools():
    """Check if system tools are available"""
    print("\n🔍 Checking system tools...")
    
    tools = ['ffmpeg', 'unrar']
    
    for tool in tools:
        if os.system(f"which {tool} > /dev/null 2>&1") == 0:
            print(f"✅ {tool} available")
        else:
            print(f"⚠️  {tool} not found (optional for video/audio/archive conversion)")
    
    print("✅ System tools check completed")
    return True

def test_bot_connection():
    """Test bot connection to Telegram API"""
    print("\n🔍 Testing bot connection...")
    
    try:
        import asyncio
        from telegram import Bot
        from dotenv import load_dotenv
        
        load_dotenv()
        bot_token = os.getenv('BOT_TOKEN')
        
        async def test_connection():
            bot = Bot(token=bot_token)
            try:
                me = await bot.get_me()
                print(f"✅ Bot connected successfully!")
                print(f"🤖 Bot name: {me.first_name}")
                print(f"📝 Username: @{me.username}")
                print(f"🆔 Bot ID: {me.id}")
                return True
            finally:
                await bot.close()
        
        # Run async function
        return asyncio.run(test_connection())
        
    except Exception as e:
        print(f"❌ Bot connection failed: {e}")
        print("💡 Check your BOT_TOKEN in .env file")
        return False

def show_bot_info():
    """Show bot information and usage instructions"""
    print("""
🚀 Bot is ready to start!

📋 Usage Instructions:
1. Start the bot: python bot.py
2. Or use quick start: ./start_bot.sh
3. Send the bot any file to test conversion

👑 Admin Commands (if configured):
/admin - Admin panel
/users - List active users  
/broadcast <message> - Send message to all users

🔧 Configuration:
- Edit .env file to modify settings
- Edit config.py for advanced configuration
- Check logs/ directory for error logs

📞 Support:
- Check README.md for detailed documentation
- Review FEATURES_SUMMARY.md for complete feature list
    """)

def main():
    """Main function"""
    print("🤖 Telegram File Converter Bot - Quick Start")
    print("=" * 50)
    
    # Run all checks
    env_ok = check_environment()
    deps_ok = check_dependencies()
    tools_ok = check_system_tools()
    
    if env_ok and deps_ok:
        conn_ok = test_bot_connection()
        
        if conn_ok:
            show_bot_info()
            print("\n✅ All checks passed! Bot is ready to run.")
            
            # Ask if user wants to start the bot
            response = input("\n🚀 Start the bot now? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                print("Starting bot...")
                try:
                    from bot import main as bot_main
                    bot_main()
                except KeyboardInterrupt:
                    print("\n👋 Bot stopped by user")
                except Exception as e:
                    print(f"❌ Error starting bot: {e}")
            else:
                print("👋 Run 'python bot.py' when ready to start the bot")
        else:
            print("\n❌ Bot connection failed. Please fix the issues above.")
            sys.exit(1)
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()