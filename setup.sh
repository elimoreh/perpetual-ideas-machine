#!/bin/bash
# Setup script for Perpetual Ideas Machine
# Run with: bash setup.sh

set -e  # Exit on error

echo "🚀 Perpetual Ideas Machine - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Found Python $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ Dependencies installed"

# Check for .env file
echo ""
echo "🔑 Checking environment configuration..."
if [ -f ".env" ]; then
    echo "✅ .env file found"
else
    echo "⚠️  .env file not found. Creating from example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
        echo "   - Get OpenAI key: https://platform.openai.com/api-keys"
        echo "   - Or get Anthropic key: https://console.anthropic.com/"
    else
        echo "❌ env.example not found"
    fi
fi

# Check if API key is set
if [ -f ".env" ]; then
    if grep -q "your-openai-api-key-here" .env || grep -q "your-anthropic-api-key-here" .env; then
        echo ""
        echo "⚠️  WARNING: API keys not configured!"
        echo "   Please edit .env and add your actual API keys before running."
    fi
fi

# Verify publications directory
echo ""
echo "📁 Checking publications directory..."
if [ -d "publications" ]; then
    echo "✅ Publications directory exists"
else
    echo "⚠️  Publications directory not found. Creating..."
    mkdir -p publications
    echo '{"inventions": []}' > publications/index.json
    echo "✅ Publications directory created"
fi

# Create domain directories
echo ""
echo "📂 Setting up domain directories..."
DOMAINS=(
    "mechanical-engineering"
    "materials-science"
    "chemical-engineering"
    "pharmaceutical-chemistry"
    "electrical-engineering"
    "software-algorithms"
    "biotechnology"
    "environmental-technology"
    "medical-devices"
    "agricultural-technology"
)

for domain in "${DOMAINS[@]}"; do
    mkdir -p "publications/$domain"
done
echo "✅ Domain directories created"

# Summary
echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env and add your API keys:"
echo "   nano .env"
echo ""
echo "2. Run the application:"
echo "   python app.py"
echo ""
echo "3. Open in browser:"
echo "   http://localhost:5000"
echo ""
echo "4. Generate your first invention!"
echo ""
echo "📖 For more help, see:"
echo "   - QUICKSTART.md (quick setup guide)"
echo "   - README.md (full documentation)"
echo "   - DEPLOYMENT.md (deploy to Heroku)"
echo ""
echo "Happy inventing! 🎉"

