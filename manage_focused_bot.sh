#!/bin/bash

# Bot Management Script untuk TXT/VCF/XLS Converter Bot

BOT_NAME="focused_bot.py"
LOG_FILE="focused_bot.log"

case "$1" in
    start)
        echo "🚀 Starting TXT/VCF/XLS Converter Bot..."
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            echo "⚠️  Bot is already running!"
            echo "📊 PID: $(pgrep -f "$BOT_NAME")"
            exit 0
        fi
        
        source venv/bin/activate
        nohup python $BOT_NAME > $LOG_FILE 2>&1 &
        
        sleep 2
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            echo "✅ Bot started successfully!"
            echo "📊 PID: $(pgrep -f "$BOT_NAME")"
            echo "📋 Log: tail -f $LOG_FILE"
        else
            echo "❌ Failed to start bot"
            echo "🔍 Check log: cat $LOG_FILE"
        fi
        ;;
        
    stop)
        echo "🛑 Stopping TXT/VCF/XLS Converter Bot..."
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            pkill -f "$BOT_NAME"
            sleep 2
            
            if pgrep -f "$BOT_NAME" > /dev/null; then
                echo "⚠️  Force killing bot..."
                pkill -9 -f "$BOT_NAME"
            fi
            
            echo "✅ Bot stopped!"
        else
            echo "ℹ️  Bot is not running"
        fi
        ;;
        
    status)
        echo "📊 Bot Status:"
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            PID=$(pgrep -f "$BOT_NAME")
            echo "✅ Bot is running (PID: $PID)"
            echo "📝 Supported formats: TXT, VCF, XLS, XLSX, CSV"
            echo "🔧 Admin ID: $(grep ADMIN_USER_ID .env | cut -d'=' -f2)"
            echo "📋 Log file: $LOG_FILE"
            echo ""
            echo "📊 Recent log entries:"
            tail -5 $LOG_FILE 2>/dev/null || echo "No log entries"
        else
            echo "❌ Bot is not running"
        fi
        ;;
        
    restart)
        echo "🔄 Restarting bot..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    log)
        echo "📋 Bot Log (last 20 lines):"
        tail -20 $LOG_FILE 2>/dev/null || echo "No log file found"
        ;;
        
    *)
        echo "🤖 TXT/VCF/XLS Converter Bot Management"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|log}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the bot"
        echo "  stop    - Stop the bot"
        echo "  restart - Restart the bot"
        echo "  status  - Show bot status"
        echo "  log     - Show recent log entries"
        echo ""
        exit 1
        ;;
esac