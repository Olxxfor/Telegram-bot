#!/bin/bash

# Advanced Bot Management Script untuk TXT/VCF/XLS Converter Bot
# Dengan fitur Rename, Merge, Split, Custom ordering

BOT_NAME="advanced_bot.py"
LOG_FILE="advanced_bot.log"

case "$1" in
    start)
        echo "🚀 Starting Advanced TXT/VCF/XLS Converter Bot..."
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            echo "⚠️  Bot is already running!"
            echo "📊 PID: $(pgrep -f "$BOT_NAME")"
            exit 0
        fi
        
        source venv/bin/activate
        nohup python $BOT_NAME > $LOG_FILE 2>&1 &
        
        sleep 2
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            echo "✅ Advanced Bot started successfully!"
            echo "📊 PID: $(pgrep -f "$BOT_NAME")"
            echo "🎯 Features: Convert, Rename, Merge, Split"
            echo "📋 Log: tail -f $LOG_FILE"
        else
            echo "❌ Failed to start bot"
            echo "🔍 Check log: cat $LOG_FILE"
        fi
        ;;
        
    stop)
        echo "🛑 Stopping Advanced TXT/VCF/XLS Converter Bot..."
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            pkill -f "$BOT_NAME"
            sleep 2
            
            if pgrep -f "$BOT_NAME" > /dev/null; then
                echo "⚠️  Force killing bot..."
                pkill -9 -f "$BOT_NAME"
            fi
            
            echo "✅ Advanced Bot stopped!"
        else
            echo "ℹ️  Bot is not running"
        fi
        ;;
        
    status)
        echo "📊 Advanced Bot Status:"
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            PID=$(pgrep -f "$BOT_NAME")
            echo "✅ Bot is running (PID: $PID)"
            echo "🎯 Features:"
            echo "   🔄 Konversi: TXT ↔ VCF ↔ XLS"
            echo "   📝 Rename: File & kontak"
            echo "   🔗 Merge: Gabung multiple files"
            echo "   ✂️ Split: Pecah file custom"
            echo "   🎯 Custom ordering & naming"
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
        echo "🔄 Restarting advanced bot..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    log)
        echo "📋 Advanced Bot Log (last 20 lines):"
        tail -20 $LOG_FILE 2>/dev/null || echo "No log file found"
        ;;
        
    features)
        echo "🎯 Advanced Bot Features:"
        echo ""
        echo "🔄 KONVERSI DASAR:"
        echo "   • TXT → VCF (kontak)"
        echo "   • VCF → TXT (text list)"
        echo "   • XLS → VCF (excel ke kontak)"
        echo "   • Semua format saling mendukung"
        echo ""
        echo "📝 RENAME:"
        echo "   • Rename file hasil"
        echo "   • Rename nama kontak"
        echo "   • Auto numbering (Customer_001, 002...)"
        echo "   • Custom pattern nama"
        echo ""
        echo "🔗 MERGE:"
        echo "   • Gabung multiple file TXT/VCF/XLS"
        echo "   • Atur urutan penggabungan"
        echo "   • Custom nama file hasil"
        echo "   • Remove duplikat otomatis"
        echo ""
        echo "✂️ SPLIT:"
        echo "   • Pecah file berdasarkan jumlah data"
        echo "   • Custom berapa data per file"
        echo "   • Auto numbering file hasil"
        echo "   • Pertahankan struktur data"
        echo ""
        echo "🎯 CUSTOM SETTINGS:"
        echo "   • Custom urutan file"
        echo "   • Custom nama kontak"
        echo "   • Flexible file splitting"
        echo "   • Sequential numbering"
        ;;
        
    test)
        echo "🧪 Testing Bot Features:"
        
        if ! pgrep -f "$BOT_NAME" > /dev/null; then
            echo "❌ Bot is not running. Start it first with: $0 start"
            exit 1
        fi
        
        echo "✅ Bot is running"
        echo "📋 Testing basic functionality..."
        
        # Check bot token
        if grep -q "YOUR_BOT_TOKEN_HERE" .env 2>/dev/null; then
            echo "❌ Bot token not configured"
        else
            echo "✅ Bot token configured"
        fi
        
        # Check dependencies
        source venv/bin/activate
        python -c "import pandas, openpyxl; print('✅ Dependencies OK')" 2>/dev/null || echo "❌ Dependencies missing"
        
        echo "📊 Bot ready for:"
        echo "   🔄 File conversion"
        echo "   📝 Rename operations"
        echo "   🔗 Merge operations"
        echo "   ✂️ Split operations"
        ;;
        
    *)
        echo "🤖 Advanced TXT/VCF/XLS Converter Bot Management"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|log|features|test}"
        echo ""
        echo "Commands:"
        echo "  start     - Start the advanced bot"
        echo "  stop      - Stop the advanced bot"
        echo "  restart   - Restart the advanced bot"
        echo "  status    - Show detailed bot status"
        echo "  log       - Show recent log entries"
        echo "  features  - Show all bot features"
        echo "  test      - Test bot functionality"
        echo ""
        echo "🎯 Bot Features:"
        echo "  🔄 Convert: TXT ↔ VCF ↔ XLS"
        echo "  📝 Rename: Files & contacts"
        echo "  🔗 Merge: Multiple files"
        echo "  ✂️ Split: Custom file splitting"
        echo ""
        exit 1
        ;;
esac