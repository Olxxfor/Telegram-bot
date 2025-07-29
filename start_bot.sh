#!/bin/bash

# Telegram Bot Starter Script
echo "🤖 Starting Telegram File Converter Bot..."

# Change to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Running setup..."
    bash setup.sh
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "💡 Please create .env file with BOT_TOKEN and ADMIN_USER_ID"
    exit 1
fi

# Check if bot is already running
if pgrep -f "simple_bot.py" > /dev/null; then
    echo "⚠️  Bot is already running!"
    echo "📊 Use 'python bot_status.py' to check status"
    exit 0
fi

# Start the bot
echo "🚀 Starting bot..."
nohup python simple_bot.py > bot.log 2>&1 &

sleep 2

# Check if bot started successfully
if pgrep -f "simple_bot.py" > /dev/null; then
    echo "✅ Bot started successfully!"
    echo "📱 Bot: @EliteConvertVip_bot"
    echo "📊 Check status: python bot_status.py"
    echo "📋 View logs: tail -f bot.log"
else
    echo "❌ Failed to start bot. Check bot.log for errors."
    tail -10 bot.log
fi
