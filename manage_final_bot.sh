#!/bin/bash

# Final Bot Management Script
# TXT/VCF/XLS Converter dengan Format OLXX-83.vcf dan REXX-83-1

BOT_NAME="final_bot.py"
LOG_FILE="final_bot.log"

case "$1" in
    start)
        echo "🚀 Starting Final Enhanced TXT/VCF/XLS Converter Bot..."
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            echo "⚠️  Bot is already running!"
            echo "📊 PID: $(pgrep -f "$BOT_NAME")"
            exit 0
        fi
        
        source venv/bin/activate
        nohup python $BOT_NAME > $LOG_FILE 2>&1 &
        
        sleep 2
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            echo "✅ Final Enhanced Bot started successfully!"
            echo "📊 PID: $(pgrep -f "$BOT_NAME")"
            echo "🎯 Final Features:"
            echo "   📁 File: OLXX-83.vcf, OLXX-84.vcf"
            echo "   👤 Kontak: REXX-83-1, REXX-83-2"
            echo "   🔄 Reset/Continue urutan"
            echo "📋 Log: tail -f $LOG_FILE"
        else
            echo "❌ Failed to start bot"
            echo "🔍 Check log: cat $LOG_FILE"
        fi
        ;;
        
    stop)
        echo "🛑 Stopping Final Enhanced Bot..."
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            pkill -f "$BOT_NAME"
            sleep 2
            
            if pgrep -f "$BOT_NAME" > /dev/null; then
                echo "⚠️  Force killing bot..."
                pkill -9 -f "$BOT_NAME"
            fi
            
            echo "✅ Final Enhanced Bot stopped!"
        else
            echo "ℹ️  Bot is not running"
        fi
        ;;
        
    status)
        echo "📊 Final Enhanced Bot Status:"
        
        if pgrep -f "$BOT_NAME" > /dev/null; then
            PID=$(pgrep -f "$BOT_NAME")
            echo "✅ Bot is running (PID: $PID)"
            echo "🎯 Final Features:"
            echo "   🔄 TXT → VCF Custom"
            echo "   📁 Format: OLXX-83.vcf, OLXX-84.vcf"
            echo "   👤 Kontak: REXX-83-1, REXX-83-2" 
            echo "   🔄 Reset/Continue per file"
            echo "🔧 Improvements:"
            echo "   📝 Hanya nomor file yang bisa dicustom"
            echo "   👥 Format kontak: PREFIX-FILENUM-CONTACTNUM"
            echo "   🔄 Opsi reset urutan atau lanjut"
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
        echo "🔄 Restarting final enhanced bot..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    log)
        echo "📋 Final Enhanced Bot Log (last 20 lines):"
        tail -20 $LOG_FILE 2>/dev/null || echo "No log file found"
        ;;
        
    demo)
        echo "🎯 Final Enhanced Bot Demo - Format Baru:"
        echo ""
        echo "📝 Input TXT file:"
        echo "   John Doe - 081234567890 - john@email.com"
        echo "   Jane Smith - 087654321 - jane@email.com"
        echo ""
        echo "🛠️ Custom Settings:"
        echo "   📁 Nama file: OLXX"
        echo "   🔢 Mulai dari file: 83"
        echo "   👤 Nama kontak: REXX"
        echo "   🔄 Mode: Reset per file"
        echo ""
        echo "📂 Output Files:"
        echo "   📁 OLXX-83.vcf"
        echo "   📁 OLXX-84.vcf (jika ada file kedua)"
        echo ""
        echo "👥 VCF Content (OLXX-83.vcf):"
        echo "   BEGIN:VCARD"
        echo "   VERSION:3.0"
        echo "   FN:REXX-83-1"
        echo "   N:REXX-83-1;;;;"
        echo "   TEL:081234567890"
        echo "   EMAIL:john@email.com"
        echo "   NOTE:Original: John Doe"
        echo "   END:VCARD"
        echo ""
        echo "   BEGIN:VCARD"
        echo "   VERSION:3.0"
        echo "   FN:REXX-83-2"
        echo "   N:REXX-83-2;;;;"
        echo "   TEL:087654321"
        echo "   EMAIL:jane@email.com"
        echo "   NOTE:Original: Jane Smith"
        echo "   END:VCARD"
        echo ""
        echo "🔄 Mode Reset: File kedua akan mulai REXX-84-1, REXX-84-2"
        echo "⚡ Mode Lanjut: File kedua akan mulai REXX-84-3, REXX-84-4"
        ;;
        
    features)
        echo "🎯 Final Enhanced Bot Features:"
        echo ""
        echo "📁 FILE NAMING:"
        echo "   • Input: OLXX, 83"
        echo "   • Output: OLXX-83.vcf, OLXX-84.vcf, OLXX-85.vcf"
        echo "   • Pattern: {prefix}-{number}.vcf"
        echo ""
        echo "👤 CONTACT NAMING:"
        echo "   • Input: REXX"
        echo "   • Output: REXX-83-1, REXX-83-2, REXX-83-3"
        echo "   • Pattern: {prefix}-{filenum}-{contactnum}"
        echo ""
        echo "🔄 RESET/CONTINUE OPTIONS:"
        echo "   • Reset: Setiap file baru, nomor kontak reset ke 1"
        echo "   • Continue: Nomor kontak lanjut berurutan antar file"
        echo ""
        echo "📝 CUSTOMIZABLE:"
        echo "   • Nama file prefix (OLXX)"
        echo "   • Nomor file mulai (83)"
        echo "   • Nama kontak prefix (REXX)"
        echo "   • Mode reset/continue"
        echo ""
        echo "✨ IMPROVEMENTS:"
        echo "   • Format sesuai permintaan: OLXX-83.vcf"
        echo "   • Kontak sesuai permintaan: REXX-83-1"
        echo "   • Opsi reset urutan per file"
        echo "   • Hanya nomor file yang bisa dicustom"
        ;;
        
    test)
        echo "🧪 Testing Final Enhanced Bot Features:"
        
        if ! pgrep -f "$BOT_NAME" > /dev/null; then
            echo "❌ Bot is not running. Start it first with: $0 start"
            exit 1
        fi
        
        echo "✅ Bot is running"
        echo "📋 Testing final functionality..."
        
        # Check bot token
        if grep -q "YOUR_BOT_TOKEN_HERE" .env 2>/dev/null; then
            echo "❌ Bot token not configured"
        else
            echo "✅ Bot token configured"
        fi
        
        # Check dependencies
        source venv/bin/activate
        python -c "import pandas, openpyxl, re; print('✅ Dependencies OK')" 2>/dev/null || echo "❌ Dependencies missing"
        
        echo "📊 Final Enhanced Bot ready for:"
        echo "   🔄 TXT → VCF dengan format OLXX-83.vcf"
        echo "   👤 Kontak dengan format REXX-83-1"
        echo "   🔄 Reset/Continue urutan"
        echo "   📝 Custom file numbering only"
        ;;
        
    *)
        echo "🤖 Final Enhanced TXT/VCF/XLS Converter Bot Management"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|log|demo|features|test}"
        echo ""
        echo "Commands:"
        echo "  start     - Start the final enhanced bot"
        echo "  stop      - Stop the final enhanced bot"
        echo "  restart   - Restart the final enhanced bot"
        echo "  status    - Show detailed bot status"
        echo "  log       - Show recent log entries"
        echo "  demo      - Show demo of final features"
        echo "  features  - Show all final features"
        echo "  test      - Test bot functionality"
        echo ""
        echo "🎯 Final Enhanced Features:"
        echo "  📁 File format: OLXX-83.vcf, OLXX-84.vcf"
        echo "  👤 Contact format: REXX-83-1, REXX-83-2"
        echo "  🔄 Reset/Continue urutan per file"
        echo "  📝 Custom nomor file mulai"
        echo ""
        echo "📋 Sesuai Permintaan:"
        echo "  ✅ File: OLXX-83.vcf dan seterusnya"
        echo "  ✅ Kontak: REXX-83-1 dan seterusnya"
        echo "  ✅ Hanya nomor file yang bisa dicustom"
        echo "  ✅ Opsi reset/lanjut urutan"
        echo ""
        exit 1
        ;;
esac