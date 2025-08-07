#!/bin/bash

# Telegram Bot Stop Script
echo "🛑 Stopping Telegram File Converter Bot..."

# Find and kill bot process
if pgrep -f "simple_bot.py" > /dev/null; then
    echo "🔍 Found running bot process..."
    pkill -f "simple_bot.py"
    
    sleep 2
    
    # Check if process was killed
    if pgrep -f "simple_bot.py" > /dev/null; then
        echo "⚠️  Force killing bot process..."
        pkill -9 -f "simple_bot.py"
    fi
    
    echo "✅ Bot stopped successfully!"
    echo "📊 Use './start_bot.sh' to restart the bot"
else
    echo "ℹ️  Bot is not running"
fi

# Show final status
echo ""
echo "📋 Final Status:"
if pgrep -f "simple_bot.py" > /dev/null; then
    echo "❌ Bot is still running"
else
    echo "✅ Bot is stopped"
fi