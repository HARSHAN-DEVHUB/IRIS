# FRIDAY - 100% FREE Setup Guide

## No Paid API Keys Required! 🎉

This is a **completely free** voice assistant using:
- **Ollama** - Free local AI (like ChatGPT but runs on YOUR computer)
- **faster-whisper** - Free speech recognition
- **Piper TTS** - Free text-to-speech

---

## Installation (3 Steps)

### Step 1: Download Ollama

Visit https://ollama.ai and download for your OS.

### Step 2: Install Dependencies

```bash
# Run automated setup
bash setup.sh

# OR manually:
pip install -r requirements.txt
cp .env.example .env
```

### Step 3: Start the Brain

**Terminal 1 - Start Ollama:**
```bash
ollama serve
```

**Terminal 2 - Run FRIDAY:**
```bash
# Test it
python demo_claude.py

# Or full voice interface (if audio hardware available)
python main.py
```

---

## That's It!

No API keys, no credit card, completely free!

---

## How It Works

```
Your Voice
   ↓
[Local Mic Audio] (pyaudio)
   ↓
[Speech-to-Text] (faster-whisper - FREE)
   ↓
[AI Brain] (Ollama - FREE, runs on your computer)
   ↓
[Generate Response]
   ↓
[Text-to-Speech] (Piper - FREE)
   ↓
Your Speakers
```

Everything happens **offline on your machine**. No data sent to the internet!

---

## Available Models to Choose From

All completely free:

```bash
ollama pull mistral         # Recommended: Fast & smart
ollama pull neural-chat     # Smaller, faster
ollama pull llama2          # More capable, slower
ollama pull openhermes-2.5  # Good balance
ollama pull dolphin-mixtral # Powerful
```

Edit `.env` to change which model FRIDAY uses.

---

## Next Steps

1. **Test the brain:**
   ```bash
   python demo_claude.py
   ```

2. **Enable voice (optional):**
   - Set up microphone
   - Run: `python main.py`

3. **Add your own tools:**
   - See `src/tools/examples.py`
   - Build weather, news scraper, calculator, etc.

---

## FAQ

**Q: Why Ollama?**
A: It's the easiest way to run a real AI model locally for free. No API keys, no subscriptions.

**Q: What hardware do I need?**
A: Any computer. Faster CPU/GPU = faster responses. Minimum 4GB RAM.

**Q: Can I customize the voice?**
A: Yes! Edit `.env` to change `PIPER_VOICE`.

**Q: Can I add more tools?**
A: Absolutely! Check `src/tools/examples.py` for templates.

**Q: What about privacy?**
A: 100% private. Everything runs locally. No data leaves your computer!

---

**Enjoy your free AI assistant! 🚀**
