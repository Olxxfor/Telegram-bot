#!/bin/bash

# Enhanced Bot Management Script
# TXT/VCF/XLS Converter dengan Custom Settings

BOT_NAME="enhanced_bot.py"
LOG_FILE="enhanced_bot.log"

case "$1" in
    start)
        echo "🚀 Starting Enhanced TXT/VCF/XLS Converter Bot..."
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            echo "⚠️  Bot is already running!"
            echo "📊 PID: $(pgrep -f "$BOT_NAME")"
            exit 0
        fi
        
        source venv/bin/activate
        nohup python $BOT_NAME > $LOG_FILE 2>&1 &
        
        sleep 2
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            echo "✅ Enhanced Bot started successfully!"
            echo "📊 PID: $(pgrep -f "$BOT_NAME")"
            echo "🎯 Custom TXT → VCF Features:"
            echo "   📝 Custom nama file (OLXX)"
            echo "   👤 Custom nama kontak (REXX)" 
            echo "   📊 Custom jumlah per file (50)"
            echo "   🔢 Custom nomor urutan (2100)"
            echo "📋 Log: tail -f $LOG_FILE"
        else
            echo "❌ Failed to start bot"
            echo "🔍 Check log: cat $LOG_FILE"
        fi
        ;;
        
    stop)
        echo "🛑 Stopping Enhanced Bot..."
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            pkill -f "$BOT_NAME"
            sleep 2
            
            if pgrep -f "$BOT_NAME" > /dev/null; then
                echo "⚠️  Force killing bot..."
                pkill -9 -f "$BOT_NAME"
            fi
            
            echo "✅ Enhanced Bot stopped!"
        else
            echo "ℹ️  Bot is not running"
        fi
        ;;
        
    status)
        echo "📊 Enhanced Bot Status:"
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            PID=$(pgrep -f "$BOT_NAME")
            echo "✅ Bot is running (PID: $PID)"
            echo "🎯 Enhanced Features:"
            echo "   🔄 TXT → VCF Custom"
            echo "   📞 VCF → TXT"
            echo "   📊 XLS → VCF"
            echo "🔧 Custom Settings:"
            echo "   📝 Nama file: Sesuai input (OLXX)"
            echo "   👤 Nama kontak: Sesuai input (REXX)"
            echo "   📊 Per file: Sesuai input (50)"
            echo "   🔢 Nomor urutan: Sesuai input (2100)"
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
        echo "🔄 Restarting enhanced bot..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    log)
        echo "📋 Enhanced Bot Log (last 20 lines):"
        tail -20 $LOG_FILE 2>/dev/null || echo "No log file found"
        ;;
        
    demo)
        echo "🎯 Enhanced Bot Demo - Custom TXT → VCF:"
        echo ""
        echo "📝 Input TXT file:"
        echo "   John Doe - 081234567890 - john@email.com"
        echo "   Jane Smith - 087654321 - jane@email.com"
        echo ""
        echo "🛠️ Custom Settings:"
        echo "   📁 Nama file: OLXX"
        echo "   👤 Nama kontak: REXX" 
        echo "   📊 Per file: 50 kontak"
        echo "   🔢 Mulai dari: 2100"
        echo ""
        echo "📂 Output Files:"
        echo "   📁 OLXX_001.vcf"
        echo "   📁 OLXX_002.vcf (jika > 50 kontak)"
        echo ""
        echo "👥 VCF Content:"
        echo "   BEGIN:VCARD"
        echo "   VERSION:3.0"
        echo "   FN:REXX_2100"
        echo "   N:REXX_2100;;;;"
        echo "   TEL:081234567890"
        echo "   EMAIL:john@email.com"
        echo "   NOTE:Original: John Doe"
        echo "   END:VCARD"
        echo ""
        echo "   BEGIN:VCARD"
        echo "   VERSION:3.0"
        echo "   FN:REXX_2101"
        echo "   N:REXX_2101;;;;"
        echo "   TEL:087654321"
        echo "   EMAIL:jane@email.com"
        echo "   NOTE:Original: Jane Smith"
        echo "   END:VCARD"
        ;;
        
    test)
        echo "🧪 Testing Enhanced Bot Features:"
        
        if ! pgrep -f "$BOT_NAME" > /dev/null; then
            echo "❌ Bot is not running. Start it first with: $0 start"
            exit 1
        fi
        
        echo "✅ Bot is running"
        echo "📋 Testing enhanced functionality..."
        
        # Check bot token
        if grep -q "YOUR_BOT_TOKEN_HERE" .env 2>/dev/null; then
            echo "❌ Bot token not configured"
        else
            echo "✅ Bot token configured"
        fi
        
        # Check dependencies
        source venv/bin/activate
        python -c "import pandas, openpyxl, re; print('✅ Dependencies OK')" 2>/dev/null || echo "❌ Dependencies missing"
        
        echo "📊 Enhanced Bot ready for:"
        echo "   🔄 Custom TXT → VCF conversion"
        echo "   📝 Custom file naming"
        echo "   👤 Custom contact naming"
        echo "   📊 Custom file splitting"
        echo "   🔢 Custom number sequencing"
        ;;
        
    *)
        echo "🤖 Enhanced TXT/VCF/XLS Converter Bot Management"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|log|demo|test}"
        echo ""
        echo "Commands:"
        echo "  start     - Start the enhanced bot"
        echo "  stop      - Stop the enhanced bot"
        echo "  restart   - Restart the enhanced bot"
        echo "  status    - Show detailed bot status"
        echo "  log       - Show recent log entries"
        echo "  demo      - Show demo of custom features"
        echo "  test      - Test bot functionality"
        echo ""
        echo "🎯 Enhanced Features:"
        echo "  📝 Custom nama file hasil"
        echo "  👤 Custom nama kontak"
        echo "  📊 Custom jumlah per file"
        echo "  🔢 Custom nomor urutan mulai"
        echo "  ✂️ Auto split file"
        echo ""
        echo "📋 Contoh:"
        echo "  Input: OLXX, REXX, 50, 2100"
        echo "  Output: OLXX_001.vcf dengan kontak REXX_2100, REXX_2101..."
        echo ""
        exit 1
        ;;
esac