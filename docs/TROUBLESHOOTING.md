# 🔧 Troubleshooting Guide

Common issues and their solutions.

## Audio Issues

### Microphone Not Detected

**Error**: "No audio input device found"

**Solutions**:

1. Check available devices:
```bash
python -c "
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}')
"
```

2. Set device in config.yaml:
```yaml
audio:
  input_device: 1  # Use device 1 instead of 0
```

3. **macOS**: Grant microphone permission:
   - System Preferences > Security & Privacy > Microphone > Terminal ✓

4. **Linux**: Check PulseAudio/ALSA:
```bash
# Try ALSA directly
ALSA_CARD=0 python main.py
```

5. Test with external microphone disconnected/reconnected

---

### No Sound Output

**Error**: Audio plays but no sound from speaker

**Solutions**:

1. Check volume:
```bash
# Increase system volume
amixer set Master 100%  # Linux
```

2. Test speaker:
```python
from voice.speech_to_text import VoiceProcessor
processor = VoiceProcessor()
processor.speak("Hello")  # Should hear sound
```

3. Set output device:
```yaml
audio:
  output_device: 1  # Try different device
```

4. Check speaker connection (external speakers)

---

### Background Noise Issues

**Problem**: Too many false wake-word detections

**Solutions**:

1. Increase confidence threshold:
```yaml
voice:
  confidence_threshold: 0.85  # Higher = stricter
```

2. Increase noise threshold:
```yaml
audio:
  noise_threshold: 0.5  # Higher = ignore more noise
```

3. Use external microphone (better noise isolation)

4. Record in quieter environment

---

## Speech Recognition Issues

### Speech Not Recognized

**Error**: "Could not understand audio"

**Solutions**:

1. Speak clearly and slowly

2. Increase confidence threshold:
```yaml
voice:
  confidence_threshold: 0.5  # Lower = more lenient
```

3. Check microphone quality:
```bash
python scripts/test_microphone.py
```

4. Use cloud recognition (more accurate):
```bash
LLM_PROVIDER=openai  # Use GPT-4 instead of local model
```

5. Check language setting:
```yaml
voice:
  language: "en-US"  # Or en-GB, etc.
```

---

### Accent Not Recognized

**Problem**: IRIS doesn't understand your accent

**Solutions**:

1. Adjust speech rate:
```python
processor = VoiceProcessor()
processor.set_speech_rate(0.8)  # Slower = clearer
```

2. Use different language:
```yaml
voice:
  language: "en-GB"  # British English
```

3. Train voice profile:
```bash
python scripts/train_voice_profile.py
```

4. Use higher confidence model

---

## AI & LLM Issues

### Ollama Connection Failed

**Error**: "Failed to connect to Ollama at localhost:11434"

**Solutions**:

1. Start Ollama:
```bash
ollama serve
```

2. Check if running:
```bash
curl http://localhost:11434/api/tags
```

3. Verify host/port:
```bash
# In .env or config.yaml
OLLAMA_HOST=http://localhost:11434
```

4. Try different port:
```bash
# Kill existing Ollama
pkill ollama

# Start on different port
ollama serve --port 11435

# Update config
OLLAMA_HOST=http://localhost:11435
```

5. Reinstall Ollama:
```bash
brew uninstall ollama
brew install ollama
ollama pull llama2
```

---

### OpenAI API Error

**Error**: "Invalid API key" or "Rate limit exceeded"

**Solutions**:

1. Verify API key:
```bash
echo $OPENAI_API_KEY  # Should show key
```

2. Check in .env:
```bash
cat .env | grep OPENAI
```

3. Get valid key from https://platform.openai.com/api-keys

4. Check rate limits:
```bash
# Check usage at platform.openai.com
```

5. Use different provider:
```bash
LLM_PROVIDER=ollama  # Use local model instead
```

---

### LLM Timeout

**Error**: "LLM request timeout"

**Solutions**:

1. Increase timeout:
```yaml
llm:
  timeout: 60  # Increased from 30
```

2. Use faster model:
```yaml
llm:
  model: "mistral"  # Faster than llama2
```

3. Enable GPU acceleration:
```yaml
llm:
  ollama:
    num_gpu: 1
```

4. Reduce max tokens:
```yaml
llm:
  max_tokens: 256  # Shorter responses
```

---

## Database Issues

### Database Lock Error

**Error**: "database is locked"

**Solutions**:

1. Restart IRIS (closes connections):
```bash
# Kill existing process
pkill -f "python main.py"

# Restart
python main.py
```

2. Clear lock file:
```bash
rm data/iris.db-journal
```

3. Check for stuck processes:
```bash
lsof data/iris.db  # Show processes accessing DB
```

4. Enable WAL mode (automatic for SQLite 3.x):
   - Already enabled in modern SQLite

---

### Database Corruption

**Error**: "database disk image is malformed"

**Solutions**:

1. Restore backup:
```bash
# Stop IRIS
pkill -f "python main.py"

# Restore
tar -xzf backups/backup_2026-04-05.tar.gz -C ./

# Restart
python main.py
```

2. Reset database:
```bash
# WARNING: This deletes all data!
rm data/iris.db
python main.py  # Recreates database
```

3. Export and reimport:
```bash
python scripts/export_user_data.py --output backup.json
rm data/iris.db
python main.py
python scripts/import_user_data.py --input backup.json
```

---

## Permission Issues

### Permission Denied Error

**Error**: "PermissionError: [Errno 13] Permission denied"

**Solutions**:

1. Fix file permissions:
```bash
chmod -R 755 data/ logs/
```

2. Change ownership:
```bash
sudo chown -R $(whoami) data/ logs/
```

3. Create directories:
```bash
mkdir -p data/user_profiles
mkdir -p data/conversations
mkdir -p logs/
```

---

## Performance Issues

### High CPU Usage

**Problem**: IRIS using 80-100% CPU

**Solutions**:

1. Reduce workers:
```yaml
performance:
  num_workers: 2  # Reduced from 4
```

2. Use smaller model:
```yaml
llm:
  model: "mistral"  # Lighter than llama2
```

3. Disable profiling:
```yaml
advanced:
  enable_profiling: false
```

4. Check for infinite loops:
```bash
# Monitor processes
top -p $(pgrep -f "python main.py")
```

---

### High Memory Usage

**Error**: "MemoryError: Unable to allocate X GiB"

**Solutions**:

1. Use GPU instead of CPU:
```yaml
llm:
  ollama:
    num_gpu: 1
```

2. Reduce cache size:
```yaml
performance:
  cache_size: 50  # Reduced from 100
```

3. Reduce model size:
```yaml
llm:
  model: "mistral"  # Smaller footprint
```

4. Monitor memory:
```bash
ps aux | grep python  # Check RSS column
```

---

### Slow Response Time

**Problem**: IRIS takes 20+ seconds to respond

**Solutions**:

1. Use GPU acceleration:
```bash
export OLLAMA_NUM_GPU=1
```

2. Use cloud provider:
```bash
LLM_PROVIDER=openai  # Faster cloud models
```

3. Reduce max tokens:
```yaml
llm:
  max_tokens: 256  # Shorter responses
```

4. Check network:
```bash
ping 8.8.8.8  # Check internet speed
```

---

## Debugging

### Enable Debug Mode

```bash
export LOG_LEVEL=DEBUG
export DEBUG_MODE=true
python main.py
```

### View Logs

```bash
# Real-time log viewing
tail -f logs/iris.log

# Search for errors
grep "ERROR" logs/iris.log

# View specific time window
grep "2026-04-05" logs/iris.log
```

### Generate Debug Report

```bash
python scripts/generate_debug_report.py
# Creates: debug_report_2026-04-05.txt
```

---

## Getting Help

1. **Check Documentation** - [docs/](../docs/) directory
2. **Search Issues** - GitHub Issues
3. **Read FAQ** - [FAQ.md](FAQ.md)
4. **Ask Community** - GitHub Discussions
5. **Report Bug** - Include debug report

---

See [Installation](INSTALLATION.md) for setup issues and [Security](SECURITY.md) for security-related problems.
