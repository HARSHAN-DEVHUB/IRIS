# ⚙️ Configuration Guide

Complete configuration options for customizing IRIS.

## Configuration Files

IRIS uses two configuration systems:

1. **config.yaml** - Application settings
2. **.env** - Environment variables (secrets)

## Main Configuration: `config.yaml`

### Voice Recognition

```yaml
voice:
  wake_words:
    - "iris"
    - "hey iris"
    - "i.r.i.s"
  language: "en-US"
  confidence_threshold: 0.7      # 0.0-1.0, lower = more lenient
  enable_wake_word: true
  vosk_model: "en-us"
  timeout: 10                     # Seconds to listen
```

### Audio Settings

```yaml
audio:
  sample_rate: 16000              # Hz
  chunk_size: 1024                # Samples per chunk
  input_device: 0                 # Microphone device ID
  output_device: 0                # Speaker device ID
  timeout: 10                     # Seconds
  noise_threshold: 0.3            # 0.0-1.0
```

### Large Language Model

```yaml
llm:
  provider: "ollama"              # ollama, openai, anthropic
  model: "llama2"                 # Model name
  temperature: 0.7                # 0.0-1.0 (lower = deterministic)
  max_tokens: 512                 # Maximum response length
  timeout: 30                     # Seconds
  
  # Ollama settings
  ollama:
    host: "http://localhost"
    port: 11434
    num_gpu: 1                    # 0 = CPU only
```

### Natural Language Processing

```yaml
nlp:
  spacy_model: "en_core_web_sm"
  enable_entity_extraction: true
  enable_intent_classification: true
```

### Storage & Database

```yaml
storage:
  database_type: "sqlite"
  sqlite_path: "./data/iris.db"
  encryption_enabled: true
  backup:
    enabled: true
    frequency: "daily"            # hourly, daily, weekly
    retention_days: 30
```

### Feature Flags

```yaml
features:
  enable_calendar: true
  enable_email: true
  enable_browser_automation: true
  enable_file_operations: true
  enable_web_search: false
  enable_smart_home: false
  enable_cloud_sync: false
  enable_analytics: false
```

### Security Settings

```yaml
security:
  voice_auth_enabled: false
  voice_auth_threshold: 0.85      # 0.0-1.0
  biometric_auth_enabled: false
  encryption_algorithm: "AES-256"
  session_timeout: 60             # Minutes
  max_auth_attempts: 3
```

### Logging Configuration

```yaml
logging:
  level: "INFO"                   # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file: "./logs/iris.log"
  max_size: 50                    # MB
  backup_count: 5
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  console_output: true
```

### Performance Tuning

```yaml
performance:
  num_workers: 4                  # CPU cores to use
  cache_size: 100                 # Responses to cache
  enable_request_queue: true
  queue_size: 50                  # Max queued requests
```

### Advanced Settings

```yaml
advanced:
  debug_mode: false
  developer_mode: false
  enable_profiling: false
  test_mode: false
  rate_limit: 60                  # Requests per minute
  plugins_dir: "./plugins"
```

---

## Environment Variables: `.env`

### AI Provider Credentials

```bash
# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
OPENAI_ORG_ID=org-xxxxxxxxxxxxx
OPENAI_MODEL=gpt-3.5-turbo

# Google
GOOGLE_API_KEY=xxxxxxxxxxxxx
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_CLIENT_SECRET=xxxxxxxxxxxxx
GOOGLE_APPLICATION_CREDENTIALS=./credentials/google-credentials.json

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

### Database Configuration

```bash
DATABASE_URL=sqlite:///./data/iris.db
DATABASE_TYPE=sqlite
```

### Security Configuration

```bash
ENCRYPTION_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # 32 chars minimum
VOICE_AUTH_ENABLED=false
VOICE_AUTH_THRESHOLD=0.85
SESSION_TIMEOUT=60
```

### Logging Configuration

```bash
LOG_LEVEL=INFO
LOG_FILE=./logs/iris.log
DEBUG_MODE=false
```

### Feature Flags

```bash
ENABLE_CLOUD_SYNC=false
ENABLE_ANALYTICS=false
ENABLE_CALENDAR=true
ENABLE_EMAIL=true
ENABLE_BROWSER_AUTOMATION=true
ENABLE_SMART_HOME=false
ENABLE_WEB_SEARCH=false
```

### LLM Settings

```bash
LLM_PROVIDER=ollama
LLM_MODEL=llama2
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=512
OLLAMA_HOST=http://localhost:11434
```

### Voice Settings

```bash
WAKE_WORD=iris
VOICE_LANGUAGE=en-US
SPEECH_CONFIDENCE=0.7
```

### Development

```bash
DEVELOPER_MODE=false
TEST_MODE=false
ENABLE_PROFILING=false
```

### Miscellaneous

```bash
PROJECT_NAME=IRIS
PROJECT_VERSION=0.1.0
PROJECT_URL=https://github.com/HARSHAN-DEVHUB/IRIS
SUPPORT_EMAIL=support@iris-assistant.dev
```

---

## Configuration Tips

### Performance Optimization

```yaml
# For slower machines
llm:
  model: "mistral"  # Smaller, faster model
  max_tokens: 256   # Shorter responses

performance:
  num_workers: 2    # Fewer parallel tasks
  cache_size: 50    # Smaller cache
```

### GPU Acceleration

```yaml
llm:
  ollama:
    num_gpu: 1      # Enable GPU

# Set environment variable
export OLLAMA_NUM_GPU=1
```

### Production Settings

```yaml
security:
  voice_auth_enabled: true
  voice_auth_threshold: 0.9
  encryption_enabled: true
  session_timeout: 30

logging:
  level: "WARNING"  # Less verbose in production
  console_output: false

debug_mode: false
developer_mode: false
```

### Development Settings

```yaml
logging:
  level: "DEBUG"    # Detailed logging

debug_mode: true
developer_mode: true
enable_profiling: true
test_mode: true
```

---

## Changing Configuration at Runtime

```python
from utils.config_loader import ConfigLoader

# Load config
config = ConfigLoader.load_config()

# Modify settings
config["llm"]["temperature"] = 0.5
config["audio"]["noise_threshold"] = 0.2

# Changes take effect immediately
```

---

## Configuration Validation

```bash
# Verify configuration is valid
python scripts/verify_setup.py
```

---

See [Installation](INSTALLATION.md) for setup instructions and [Security](SECURITY.md) for encryption setup.
