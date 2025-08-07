#!/bin/bash

# Telegram File Converter Bot Setup Script
echo "🤖 Setting up Telegram File Converter Bot..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if Python 3.8+ is installed
print_header "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python $PYTHON_VERSION found"
    
    # Check if version is 3.8 or higher
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
        print_status "Python version is compatible"
    else
        print_error "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
print_header "Checking pip..."
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 is not installed. Installing pip..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Install system dependencies
print_header "Installing system dependencies..."
sudo apt-get update

# Install ffmpeg for video/audio conversion
if command -v ffmpeg &> /dev/null; then
    print_status "ffmpeg already installed"
else
    print_status "Installing ffmpeg..."
    sudo apt-get install -y ffmpeg
fi

# Install other useful tools
sudo apt-get install -y \
    libmagic1 \
    file \
    unrar \
    p7zip-full \
    imagemagick

# Create virtual environment
print_header "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_header "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
print_header "Creating directories..."
mkdir -p logs
mkdir -p temp
mkdir -p data

# Create environment file template
print_header "Creating environment configuration..."
if [ ! -f ".env" ]; then
    cat > .env << EOL
# Telegram Bot Configuration
BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Optional: Admin user ID for admin commands
ADMIN_USER_ID=

# Optional: Database configuration
DATABASE_URL=sqlite:///bot.db

# Optional: Redis for caching (if using Redis)
REDIS_URL=redis://localhost:6379

# Optional: File storage settings
MAX_FILE_SIZE=52428800
TEMP_DIR=./temp

# Optional: Logging level
LOG_LEVEL=INFO
EOL
    print_status "Created .env file template"
    print_warning "Please edit .env file and add your BOT_TOKEN"
else
    print_status ".env file already exists"
fi

# Create systemd service file (optional)
print_header "Creating systemd service file..."
cat > telegram-bot.service << EOL
[Unit]
Description=Telegram File Converter Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

print_status "Created telegram-bot.service file"
print_warning "To install as system service, run: sudo cp telegram-bot.service /etc/systemd/system/"

# Create startup script
print_header "Creating startup script..."
cat > start_bot.sh << EOL
#!/bin/bash
cd "\$(dirname "\$0")"
source venv/bin/activate
python bot.py
EOL

chmod +x start_bot.sh
print_status "Created start_bot.sh script"

# Create requirements check script
cat > check_requirements.py << EOL
#!/usr/bin/env python3
"""
Check if all required dependencies are installed
"""

import sys
import importlib

required_packages = [
    'telegram',
    'PIL',
    'PyPDF2', 
    'docx',
    'reportlab',
    'rarfile'
]

optional_packages = [
    'ffmpeg'
]

def check_package(package_name):
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

print("Checking required packages...")
all_good = True

for package in required_packages:
    if check_package(package):
        print(f"✅ {package}")
    else:
        print(f"❌ {package} - NOT FOUND")
        all_good = False

print("\nChecking optional packages...")
for package in optional_packages:
    if check_package(package):
        print(f"✅ {package}")
    else:
        print(f"⚠️  {package} - NOT FOUND (optional)")

if all_good:
    print("\n🎉 All required packages are installed!")
    sys.exit(0)
else:
    print("\n❌ Some required packages are missing!")
    sys.exit(1)
EOL

chmod +x check_requirements.py

# Final instructions
print_header "Setup completed!"
echo ""
print_status "Next steps:"
echo "1. Edit .env file and add your Telegram bot token"
echo "2. Get your bot token from @BotFather on Telegram"
echo "3. Run: source venv/bin/activate"
echo "4. Run: python check_requirements.py"
echo "5. Run: python bot.py"
echo ""
print_status "Or simply run: ./start_bot.sh"
echo ""
print_warning "Make sure to keep your bot token secure!"

# Test installation
print_header "Testing installation..."
source venv/bin/activate
python check_requirements.py

echo ""
print_status "Setup script completed successfully! 🚀"