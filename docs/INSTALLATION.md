# 📥 Installation Guide

Complete step-by-step installation instructions for all platforms.

## 💻 System Requirements

### Minimum Requirements

| Component | Specification |
|-----------|---------------|
| **Operating System** | macOS 10.13+ or Ubuntu 18.04+ |
| **Python Version** | 3.9 or higher |
| **RAM** | 8 GB (16 GB recommended) |
| **Storage** | 7 GB free (includes models) |
| **Processor** | Intel i5 / Apple Silicon / equivalent |
| **Microphone** | Built-in or external |
| **Internet** | Required for cloud features (optional) |

### Recommended Setup

- **OS**: macOS 12+ or Ubuntu 22.04 LTS
- **Python**: 3.11 or 3.12
- **RAM**: 16-32 GB
- **Storage**: SSD with 20 GB free
- **GPU**: NVIDIA RTX 3060+ (optional, for faster inference)
- **Microphone**: High-quality external USB mic

### Disk Space Breakdown

| Component | Size |
|-----------|------|
| Python packages | ~800 MB |
| Llama 2 model | ~4 GB |
| Whisper model | ~1.5 GB |
| Spacy models | ~500 MB |
| Database & logs | ~100 MB |
| **Total** | **~7 GB** |

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Git installed
- [ ] Access to microphone
- [ ] Terminal/Command prompt access
- [ ] 7+ GB free disk space
- [ ] (Optional) API keys ready (OpenAI, Google, etc.)

## Step-by-Step Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/HARSHAN-DEVHUB/IRIS.git
cd IRIS
git branch -a  # View all branches
```

### Step 2: Create & Activate Virtual Environment

```bash
# Create virtual environment
python3 -m venv iris_env

# Activate (macOS/Linux)
source iris_env/bin/activate

# Activate (Windows)
iris_env\Scripts\activate

# Verify activation
which python3
```

### Step 3: Upgrade pip and Install Python Dependencies

```bash
# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

# Verify core packages
python -c "import whisper; import vosk; print('✓ Core packages installed')"
```

### Step 4: Install System-Level Dependencies

#### For macOS

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install portaudio ffmpeg ollama

# Verify installation
brew list portaudio ffmpeg ollama

# Add to PATH
export PATH="/usr/local/bin:$PATH"
```

#### For Ubuntu/Debian Linux

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3-dev portaudio19-dev ffmpeg libssl-dev libffi-dev build-essential

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
which portaudio ffmpeg ollama
```

#### For Windows (WSL2 Recommended)

```powershell
# Install via Chocolatey (if available) or download manually
choco install python ffmpeg

# For WSL2, follow Ubuntu instructions above
```

### Step 5: Configure Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit with your settings
nano .env  # or use your favorite editor
```

**Sample .env Configuration:**

```bash
# AI Provider Configuration
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
OPENAI_MODEL=gpt-3.5-turbo
GOOGLE_API_KEY=xxxxxxxxxxxxx

# LLM Settings
LLM_PROVIDER=ollama
LLM_MODEL=llama2
OLLAMA_HOST=http://localhost:11434

# Security
ENCRYPTION_KEY=your-secure-32-character-key-here
VOICE_AUTH_ENABLED=false

# Logging
LOG_LEVEL=INFO
DEBUG_MODE=false

# Features
ENABLE_CALENDAR=true
ENABLE_EMAIL=true
ENABLE_BROWSER_AUTOMATION=true
```

### Step 6: Download & Set Up LLM Model

#### Option A: Using Ollama (Recommended - Local & Private)

```bash
# Install Ollama
brew install ollama  # macOS
# or
curl -fsSL https://ollama.ai/install.sh | sh  # Linux

# Start Ollama in background
ollama serve &

# Download Llama 2 model
ollama pull llama2

# Verify installation
ollama list
curl http://localhost:11434/api/tags
```

#### Option B: Using OpenAI (Cloud-based)

```bash
# Add API key to .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# Test connection
python -c "from openai import OpenAI; client = OpenAI(); print('✓ OpenAI connection successful')"
```

### Step 7: Download NLP Models

```bash
# Download spaCy model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Verify
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✓ spaCy model loaded successfully')"
```

### Step 8: Verify Complete Installation

```bash
python scripts/verify_setup.py
```

**Expected Output:**
```
✓ Python version: 3.11.x
✓ All required packages installed
✓ Microphone accessible
✓ Audio system working
✓ Ollama connection: Active
✓ spaCy model loaded
✓ Database initialized
✓ Encryption configured
✓ Setup complete! Ready to use IRIS.
```

### Step 9: (Optional) Set Up Voice Authentication

```bash
# Train voice profile for authentication
python scripts/train_voice_profile.py

# Follow prompts (takes 2-3 minutes)
# Then enable in config
VOICE_AUTH_ENABLED=true
```

### Step 10: Create Data Directories & Set Permissions

```bash
# Create necessary directories
mkdir -p data/user_profiles
mkdir -p data/conversations
mkdir -p data/models
mkdir -p data/backups
mkdir -p logs

# Set proper permissions
chmod -R 755 data/ logs/
ls -la data/  # Verify
```

## Post-Installation

### Generate Encryption Key (Security)

```bash
python scripts/generate_encryption_key.py
# Add to .env as ENCRYPTION_KEY
```

### Backup Initial Setup

```bash
# Create backup of clean database
python scripts/backup_data.py
```

### Test Microphone

```bash
python scripts/test_microphone.py
```

## Troubleshooting Installation

### Issue: Python not found
```bash
# Ensure Python 3.9+ is installed
python3 --version

# Update PATH if needed
export PATH="/usr/local/bin:$PATH"
```

### Issue: Permission denied on data directory
```bash
# Fix permissions
chmod -R 755 data/ logs/
sudo chown -R $(whoami) data/ logs/
```

### Issue: Ollama connection failed
```bash
# Start Ollama service
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### Issue: Microphone not detected
```bash
# List audio devices
python -c "
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}')
"
```

---

**Next Steps:** See [Configuration](CONFIGURATION.md) to customize your setup or [Quick Start](QUICK_START.md) to begin using IRIS.
