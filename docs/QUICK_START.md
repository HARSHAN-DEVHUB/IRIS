# 🚀 Quick Start Guide

Get IRIS up and running in 5 minutes!

## Prerequisites

- Python 3.9+
- Git
- Microphone
- 7+ GB free disk space
- macOS 10.13+ or Ubuntu 18.04+

## Installation (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/HARSHAN-DEVHUB/IRIS.git
cd IRIS
```

### 2. Setup Virtual Environment
```bash
python3 -m venv iris_env
source iris_env/bin/activate  # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys (or skip for local-only mode)
nano .env
```

### 5. Download Models
```bash
# For macOS
brew install ollama
ollama serve &
ollama pull llama2

# For Ubuntu/Linux
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull llama2
```

### 6. Verify Installation
```bash
python scripts/verify_setup.py
```

## First Launch

```bash
python main.py
```

You should see:
```
╔════════════════════════════════════╗
║  🤖 IRIS - AI Assistant           ║
║  Starting up... Please wait.      ║
╚════════════════════════════════════╝

🎤 IRIS Ready: Listening for wake word...
Say: "Hey IRIS" or "IRIS"
```

## Try These Commands

```
You: "Hey IRIS"
IRIS: ✓ Wake word detected

You: "Open Chrome"
IRIS: Opening Chrome for you

You: "What time is it?"
IRIS: The current time is 2:30 PM

You: "Set a reminder for tomorrow at 9 AM"
IRIS: Reminder set for tomorrow at 9:00 AM

You: "Goodbye"
IRIS: Goodbye! Have a great day!
```

## Next Steps

- **[Full Installation Guide](INSTALLATION.md)** - Detailed setup for all platforms
- **[Configuration](CONFIGURATION.md)** - Customize IRIS settings
- **[Command Reference](COMMANDS.md)** - Learn all available commands
- **[Troubleshooting](TROUBLESHOOTING.md)** - Fix common issues

## Troubleshooting Quick Fixes

**Microphone not working?**
```bash
# Check audio input
python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_device_count(), 'devices found')"
```

**Ollama won't connect?**
```bash
# Restart Ollama service
ollama serve
```

**Permission denied?**
```bash
# Fix file permissions
chmod -R 755 data/ logs/
```

---

**Need more help?** Check [Troubleshooting](TROUBLESHOOTING.md) or open an issue on [GitHub](https://github.com/HARSHAN-DEVHUB/IRIS/issues).
