#!/bin/bash
# FRIDAY Free Stack - One-Command Setup

set -e

echo "=========================================="
echo "FRIDAY - Free Voice Assistant Setup"
echo "=========================================="
echo ""

# Check Python
echo "✓ Checking Python..."
python3 --version

# Check pip
echo "✓ Checking pip..."
pip3 --version

# Create .env from example
if [ ! -f .env ]; then
    echo "✓ Creating .env from .env.example..."
    cp .env.example .env
    echo "  → Edit .env to customize (optional)"
else
    echo "ℹ .env already exists, skipping"
fi

# Install Python dependencies
echo ""
echo "✓ Installing Python dependencies..."
pip3 install -r requirements.txt

# Create data directories
echo "✓ Creating data directories..."
mkdir -p data

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Install Ollama: https://ollama.ai"
echo ""
echo "2. Pull a model:"
echo "   ollama pull mistral"
echo ""
echo "3. Start Ollama in a new terminal:"
echo "   ollama serve"
echo ""
echo "4. Run FRIDAY demo:"
echo "   python demo_claude.py"
echo ""
echo "For full voice support, read FREE_SETUP.md"
echo ""
