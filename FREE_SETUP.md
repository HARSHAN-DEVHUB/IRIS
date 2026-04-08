# FRIDAY - Completely Free Voice Assistant

**Build a movie-accurate voice assistant without paying a single dollar!**

All components are **open-source and free**:
- ✅ AI Brain: **Ollama** (local, runs on your machine)
- ✅ Speech-to-Text: **faster-whisper** (free, fast, accurate)
- ✅ Text-to-Speech: **Piper TTS** (free, offline)
- ✅ Voice Activity Detection: **pyannote-audio** (free alternative to wake word)
- ✅ Web Scraping: **BeautifulSoup** (for free news)
- ✅ Search: **DuckDuckGo** (free, no key needed)

---

## Quick Start (5 minutes)

### 1. Install Ollama (the free brain)

Go to https://ollama.ai and download Ollama for your OS.

**On Mac/Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

### 2. Pull a Model

Choose one:
```bash
# Recommended: Fast & powerful
ollama pull mistral

# Or: Smaller & faster
ollama pull neural-chat

# Or: Largest & most capable
ollama pull llama2
```

### 3. Start Ollama Server

```bash
ollama serve
# Keep this running in a terminal
```

### 4. Clone & Setup FRIDAY

```bash
# Install dependencies
pip install -r requirements.txt

# Copy config
cp .env.example .env

# Optional: Edit .env if you want to change model name
nano .env
```

### 5. Run FRIDAY

```bash
python demo_claude.py
```

That's it! No API keys, no subscriptions, completely free!

---

## What You Get

### Out of the Box (Works Now)
- ✅ Chat with a local AI (Ollama)
- ✅ Tools: Date, Time, Weather (free tier)
- ✅ Conversation memory
- ✅ Configuration system

### Ready to Build
- Voice input (Wake word detection or manual activation)
- Speech-to-text (faster-whisper)
- Text-to-speech (Piper)
- More tools (News scraper, Search, Calendar, etc.)

---

## Full Voice Pipeline (Next Steps)

### Voice Input
```bash
python test_voice_pipeline.py
```

### Full Assistant with Voice
```bash
python main.py
```
*Requires audio equipment (mic + speakers)*

---

## Architecture

```
YOU → Microphone
    ↓
[Local Speech-to-Text] (faster-whisper)
    ↓
[Ollama Brain] (runs locally, completely free)
    ↓
[Tools] (news, weather, time, calculator, etc.)
    ↓
[Local Text-to-Speech] (Piper TTS)
    ↓
Speakers → YOU
```

**Everything runs on your machine. No cloud dependency. No API keys. No monthly bills.**

---

## Customize

### Change AI Model

Edit `.env`:
```bash
OLLAMA_MODEL=neural-chat  # or llama2, openchat, etc.
```

Then run:
```bash
ollama pull neural-chat
```

### Change TTS Voice

Available Piper voices:
- `en_US-amy-medium` (female, default)
- `en_US-john-medium` (male)
- `en_US-lessac-high` (female, high pitch)
- `en_GB-jon-medium` (British accent)

Edit `.env`:
```bash
PIPER_VOICE=en_US-john-medium
```

---

## Performance Tips

### Faster Response Times
- Use smaller models: `neural-chat` > `mistral` > `llama2`
- Add more RAM (speeds up inference)
- Use GPU if available (set up CUDA with Ollama)

### Lower Latency
- Use `tiny` whisper model (less accurate but faster)
- Cache common responses
- Pre-load model in Ollama

---

## Troubleshooting

### "Cannot connect to Ollama"
- Is `ollama serve` running?
- Check port 11434 is accessible
- ```bash
  curl http://localhost:11434/api/tags
  ```

### Slow responses
- Use `neural-chat` instead of `mistral`
- Reduce `max_tokens` in messages
- Check CPU/RAM usage

### Bad transcription
- Ensure microphone volume is adequate
- Use `base` or `small` whisper model
- Use `medium` if you have enough RAM

---

## Next: Add More Tools

See [src/tools/examples.py](src/tools/examples.py) to add:
- Weather (OpenWeatherMap free tier)
- News scraper (RSS feeds)
- Calculator
- Wikipedia search
- And more!

---

**Questions?** Check the docs in `/docs` or the code comments.

**Happy building! 🎉**
