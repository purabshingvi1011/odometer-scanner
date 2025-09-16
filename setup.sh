#!/bin/bash

# Setup script for Odometer Scanner App
echo "🚗 Setting up Odometer Scanner App..."

# Check if Homebrew is installed (macOS)
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Please install Homebrew first:"
    echo "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Install Tesseract OCR
echo "📦 Installing Tesseract OCR..."
brew install tesseract

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Create virtual environment (optional)
echo "🌍 Creating virtual environment..."
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To run the app:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the app: streamlit run app.py"
echo ""
echo "The app will open in your browser and is optimized for mobile devices."
