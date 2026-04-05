# ❓ FAQ - Frequently Asked Questions

## General Questions

### What is IRIS?

IRIS is a **voice-activated personal AI assistant** for macOS and Linux. Unlike generic virtual assistants, IRIS:
- Runs locally on your machine (private & secure)
- Uses open-source AI models (customizable)
- Executes real tasks (open apps, manage files, send emails)
- Learns your preferences (personalized)

Think of it as a personal J.A.R.V.I.S. from Iron Man.

### Is IRIS really like Tony Stark's J.A.R.V.I.S.?

We're building towards it! Currently we're at Phase 1-2 (basic voice assistant with some AI reasoning). Full parity would require:
- Advanced contextual reasoning ✓ (In Phase 2-3)
- Enterprise automation ✓ (In Phase 4)
- Multi-device integration ✓ (Post-Phase 5)
- Quantum computing... maybe later 😄

### Can I use IRIS commercially?

Yes! IRIS is licensed under MIT License, which allows:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ❌ Just give attribution

### Is my data private?

Yes! When using local mode (Ollama):
- ✅ All processing happens on your machine
- ✅ No data sent to cloud
- ✅ All data encrypted locally
- ✅ Complete privacy

If using cloud AI (OpenAI/Claude):
- ⚠️ Encrypted transmission
- ⚠️ Follow provider's privacy policy
- You can disable cloud features

### Can I run this on Windows?

Partial support:
- ✅ Windows Subsystem for Linux (WSL2) - Full support
- ⚠️ Native Windows - Some features excluded
- Recommend WSL2 for best experience

### Does it require internet?

No! IRIS works completely offline with:
- Ollama (local LLM)
- Vosk (wake-word detection)
- pyttsx3 (text-to-speech)

Internet only needed for:
- Cloud AI (OpenAI, Claude)
- Google Calendar/Gmail
- Web search

---

## Technical Questions

### What's the difference: Ollama vs OpenAI?

| Aspect | Ollama | OpenAI |
|--------|--------|--------|
| **Cost** | Free | $0.03-0.06 per 1K tokens |
| **Speed** | 3-10s (local) | 1-3s (cloud) |
| **Privacy** | 100% private | Depends on policy |
| **Customization** | Full | Limited |
| **Quality** | Good | Excellent |
| **Requires Internet** | No | Yes |
| **GPU Needed** | Optional (faster) | No (cloud) |

**Use Ollama if**: You want privacy, free tier, full control
**Use OpenAI if**: You want best quality, faster responses, easier setup

### Can I train my own LLM?

Not yet, but it's on the roadmap:
- Phase 5+ will include fine-tuning
- Currently you can use pre-trained models:
  - Local: Llama 2, Mistral, etc.
  - Cloud: GPT-4, Claude, etc.

### How long does it take to respond?

Typical response times:
- Listening: 1-3 seconds
- AI processing: 3-10 seconds (local) or 1-3 seconds (cloud)
- Speaking: 1-2 seconds
- **Total**: 5-15 seconds

Factors affecting speed:
- ✅ GPU acceleration (faster)
- ❌ Large models (slower)
- ✅ Cloud providers (faster)
- ❌ Complex queries (slower)

### What LLMs are supported?

Local (Ollama):
- Llama 2 (default)
- Mistral (smaller, faster)
- Wyzard (math-focused)
- Custom GGML models

Cloud:
- OpenAI: GPT-4, GPT-3.5-turbo
- Claude: Claude 3
- Others coming soon

### How much RAM/Storage do I need?

| Component | Size |
|-----------|------|
| Base installation | ~800 MB |
| Llama 2 model | ~4 GB |
| Whisper model | ~1.5 GB |
| Spacy models | ~500 MB |
| **Total** | **~7 GB** |

**Minimum**: 8 GB RAM  
**Recommended**: 16+ GB RAM

---

## Feature Questions

### Can IRIS access my calendar?

Not yet (Phase 4):
- 📅 Will support Google Calendar
- 📅 Will support Outlook/Microsoft 365
- 📅 Will sync across devices

Currently supports:
- ✅ Creating reminders
- ✅ Setting timers
- 🔄 Local calendar (coming)

### Can IRIS send emails?

Not yet (Phase 4):
- 📅 Will support Gmail
- 📅 Will support Outlook
- 📅 Will compose and send emails

Currently supports:
- ✅ Voice command parsing for email actions
- 🔄 Email composition (coming)

### Can IRIS control smart home devices?

Not yet (Post-Phase 5):
- 📅 Smart home integration planned
- Will support: Alexa, HomeKit, Google Home, Philips Hue, etc.

Currently supports:
- ✅ System brightness/volume control
- 🔄 Smart home (coming)

### Can IRIS work offline?

Yes! Full offline support:
- ✅ Speech recognition (Whisper)
- ✅ Wake-word detection (Vosk)
- ✅ LLM (Ollama)
- ✅ Text-to-speech (pyttsx3)
- ✅ All local commands

No internet needed!

### Can I create custom commands?

Yes! Full extensibility:

```python
from executor.command_handler import CommandExecutor

executor = CommandExecutor()

def my_command(params):
    return f"Did something with {params}"

executor.register_command("my_command", my_command)
```

See [API Reference](API_REFERENCE.md) for details.

---

## Pricing Questions

### How much does IRIS cost?

IRIS itself: **Free** (MIT License)

Optional costs:
- **Cloud AI** (OpenAI): ~$0.03-0.06 per 1,000 tokens
- **Example**: 1,000 typical queries ≈ $0.30-0.60/month
- **Gmail API**: Free (included with Google account)
- **Hardware**: Your computer

You can use IRIS completely free with Ollama!

---

## Security Questions

### Is IRIS secure?

Security features:
- ✅ Local processing (no cloud by default)
- ✅ Data encryption (AES-256)
- ✅ Voice authentication (Phase 5)
- ✅ Permission controls
- ✅ Audit logging
- ✅ Secure credential storage

### How is my data encrypted?

- ✅ Conversation history: AES-256
- ✅ User profiles: AES-256
- ✅ Credentials: Platform keychain or encrypted storage
- ✅ Data in transit: HTTPS/TLS

See [Security Guide](SECURITY.md) for details.

### Can someone hack IRIS?

Security considerations:
- ✅ Local processing reduces attack surface
- ✅ Encryption protects data
- ⚠️ Voice authentication can be spoofed (but requires speaker/audio)
- ✅ Permission system prevents unauthorized actions

Recommendations:
- Keep IRIS updated
- Use voice authentication
- Restrict dangerous commands
- Regular backups
- Monitor audit logs

### What if I lose my encryption key?

**Important**: Encryption key is critical!

If lost:
- ❌ Cannot decrypt existing data
- ✅ Can create new data with new key
- ✅ Can restore from backup if you have old key

**Prevention**:
- Store key in secure location (password manager)
- Regular backups
- Test recovery procedures

---

## Troubleshooting Questions

### Why doesn't IRIS recognize my voice?

Common causes:
- Background noise (use quiet environment)
- Low microphone quality (try external mic)
- Accent not trained (record voice profile)
- Confidence threshold too high (lower it)
- Damaged audio hardware

See [Troubleshooting](TROUBLESHOOTING.md) for solutions.

### Why is IRIS so slow?

Possible reasons:
- Local LLM processing time (use GPU or cloud)
- Large model (use smaller model like Mistral)
- Network latency (for cloud)
- Audio encoding (normal for Whisper)
- System resources (close other apps)

See [Performance Tuning](PERFORMANCE.md) for optimization.

### Why does IRIS keep disconnecting?

Possible reasons:
- Network issues (if using cloud)
- Ollama crashed (restart with `ollama serve`)
- Database lock (restart IRIS)
- Memory issues (reduce workers/cache)
- Audio device disconnected

See [Troubleshooting](TROUBLESHOOTING.md) for solutions.

---

## Usage Questions

### How do I train IRIS to recognize my voice?

```bash
python scripts/train_voice_profile.py

# Follow instructions:
# 1. Record 5 voice samples
# 2. Say given phrases clearly
# 3. Process and save profile
# 4. Enable in config
```

### Can IRIS do multiple things at once?

Currently: **Sequential** processing (one command at a time)
- "Do X then Y" - Executes X, then Y
- Multiple wake words - Only processes one at a time

Planned (Phase 5+):
- Parallel command execution
- Background task support
- Multi-turn complex workflows

### How do I share IRIS between users?

Current limitations:
- Single-user per installation
- Voice profile per user
- Permissions per command

Planning (Phase 5):
- Multi-user support
- User profiles
- Separate databases

For now, separate installations work.

---

## Support Questions

### Where can I get help?

1. **Read Documentation** - [docs/](../docs/) folder
2. **Check FAQ** - This page
3. **Search Issues** - [GitHub Issues](https://github.com/HARSHAN-DEVHUB/IRIS/issues)
4. **Ask Community** - [GitHub Discussions](https://github.com/HARSHAN-DEVHUB/IRIS/discussions)
5. **Report Bug** - New issue with details

### How do I report bugs?

**Include**:
- Error message (full traceback)
- Steps to reproduce
- Your environment (OS, Python version)
- Debug output (from `debug_report.txt`)

**Don't**:
- Include API keys or passwords
- Open multiple issues for same bug
- Post in discussions (use Issues)

### Response times?

- **Security issues**: 24 hours (private)
- **Bugs**: 24-48 hours
- **Features**: 1 week
- **Questions**: 3-7 days
- **PRs**: 2-5 days

---

## Contributing Questions

### How do I contribute?

See [Contributing Guide](CONTRIBUTING.md):
1. Fork repository
2. Create feature branch
3. Make changes
4. Write tests
5. Submit PR

### What can I contribute?

- Bug fixes
- New features
- Documentation
- Tests
- Performance improvements
- Translations

### Will my contribution be accepted?

Acceptance criteria:
- ✅ Aligned with project vision
- ✅ Tests pass and coverage ≥ 80%
- ✅ Code follows style guide
- ✅ Documentation updated
- ✅ No breaking changes

---

**Didn't find answer?** [Open discussion](https://github.com/HARSHAN-DEVHUB/IRIS/discussions) or [contact support](mailto:support@iris-assistant.dev)

See [Full Documentation](README.md) for more information.
