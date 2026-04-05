# 📁 Project Structure

Directory layout and organization of IRIS codebase.

## Root Directory

```
IRIS/
├── 📄 README.md                          # Main documentation & quick start
├── 📄 LICENSE                            # MIT License
├── 📄 CHANGELOG.md                       # Version history
├── 📄 requirements.txt                   # Python dependencies
├── 📄 requirements-dev.txt               # Development dependencies
├── 📄 config.yaml                        # Configuration template
├── 📄 .env.example                       # Environment variables template
├── 📄 .gitignore                         # Git ignore rules
├── 📄 setup.py                           # Package installation
├── 📄 pyproject.toml                     # Project metadata
├── 📄 main.py                            # Application entry point
├── 📄 run.py                             # Alternative launcher
├── 📄 pytest.ini                         # Pytest configuration
├── 📄 .pre-commit-config.yaml           # Pre-commit hooks
├── 📄 tox.ini                            # Tox testing configuration
└── 📁 [subdirectories listed below]
```

## Core Application

### `voice/` - Voice Processing Module

Handles all audio input/output operations.

```
voice/
├── __init__.py
├── speech_to_text.py                     # Whisper STT integration
├── wake_word_detector.py                 # Vosk wake-word detection
├── text_to_speech.py                     # TTS output (pyttsx3)
├── audio_processor.py                    # Audio stream handling
├── audio_recorder.py                     # Recording utilities
└── voice_utils.py                        # Voice-related utilities
```

**Responsibilities**:
- Microphone input handling
- Speech-to-text conversion
- Wake-word detection
- Text-to-speech output
- Audio processing & filtering
- Volume/noise management

### `brain/` - AI Processing Module

Handles AI reasoning and NLP operations.

```
brain/
├── __init__.py
├── llm_interface.py                      # LLM abstraction layer
├── memory_manager.py                     # Vector DB + storage
├── intent_parser.py                      # NLP intent extraction
├── entity_extractor.py                   # Entity recognition
├── context_manager.py                    # Conversation context
├── response_generator.py                 # AI response generation
├── knowledge_base.py                     # Knowledge storage
└── prompt_templates.py                   # LLM prompt templates
```

**Responsibilities**:
- LLM inference (local & cloud)
- Intent/entity extraction
- Context management
- Response generation
- Memory & embeddings
- Conversation history

### `executor/` - Task Execution Module

Handles command execution and automation.

```
executor/
├── __init__.py
├── command_handler.py                    # Command router
├── command_registry.py                   # Command registration
├── app_launcher.py                       # Launch applications
├── file_operations.py                    # File system tasks
├── browser_control.py                    # Browser automation
├── calendar_email.py                     # Calendar & email APIs
├── system_commands.py                    # OS-level operations
├── web_browser.py                        # Web search
└── smart_home.py                         # Smart home integration
```

**Responsibilities**:
- Command routing & execution
- Application launching
- File operations
- Browser automation
- Calendar/email integration
- System operations
- External API integration

### `security/` - Authentication & Encryption Module

Handles security and authorization.

```
security/
├── __init__.py
├── authenticator.py                      # User authentication
├── voice_profile.py                      # Voice biometric training
├── encryption.py                         # Data encryption/decryption
├── permission_manager.py                 # RBAC system
├── audit_logger.py                       # Security audit trail
└── secure_storage.py                     # Secure credential storage
```

**Responsibilities**:
- User authentication
- Voice biometrics
- Data encryption
- Permission management
- Audit logging
- Secure credential storage

### `utils/` - Utility Functions

Common utilities and helpers.

```
utils/
├── __init__.py
├── logger.py                             # Logging configuration
├── config_loader.py                      # YAML/ENV config loading
├── helpers.py                            # General helper functions
├── constants.py                          # Constants & enums
├── decorators.py                         # Useful decorators
├── validators.py                         # Input validation
└── converters.py                         # Type conversion utilities
```

**Responsibilities**:
- Logging setup
- Configuration loading
- Input validation
- Helper functions
- Constants & enums

## Data & Storage

### `data/` - User Data Directory

```
data/
├── iris.db                               # SQLite database
├── user_profiles/                        # User profile data (encrypted)
│   ├── user_001.json
│   └── user_002.json
├── conversations/                        # Chat history
│   ├── 2026-04-05/
│   └── 2026-04-06/
├── models/                               # ML models cache
│   ├── whisper/
│   ├── spacy/
│   └── embeddings/
├── backups/                              # Backup files
│   ├── backup_2026-04-05.tar.gz
│   └── backup_2026-04-06.tar.gz
└── vector_store/                         # ChromaDB vector storage
```

**Security**: All encrypted with AES-256

### `logs/` - Application Logs

```
logs/
├── iris.log                              # Current log file
├── iris.log.1                            # Rotated logs
├── iris.log.2
└── debug_report.txt                      # Debug information
```

**Format**: Timestamps, levels, components

## Documentation

### `docs/` - Complete Documentation

```
docs/
├── README.md                             # Documentation index
├── QUICK_START.md                        # 5-minute setup guide
├── INSTALLATION.md                       # Detailed installation
├── ARCHITECTURE.md                       # System architecture
├── PROJECT_STRUCTURE.md                  # This file
├── API_REFERENCE.md                      # API documentation
├── COMMANDS.md                           # Command reference
├── CONFIGURATION.md                      # Configuration guide
├── SECURITY.md                           # Security best practices
├── TESTING.md                            # Testing guide
├── TROUBLESHOOTING.md                    # Problem solutions
├── DEVELOPMENT.md                        # Development roadmap
├── CONTRIBUTING.md                       # Contribution guide
├── FAQ.md                                # Frequently asked questions
├── PERFORMANCE.md                        # Performance tuning
└── diagrams/                             # Architecture diagrams
    ├── system_architecture.png
    ├── data_flow.png
    └── component_interaction.png
```

## Testing

### `tests/` - Test Suite

```
tests/
├── __init__.py
├── conftest.py                           # Pytest configuration
├── test_voice.py                         # Voice module tests
├── test_brain.py                         # Brain/AI tests
├── test_executor.py                      # Executor tests
├── test_security.py                      # Security tests
├── test_integration.py                   # Integration tests
├── fixtures/                             # Test data
│   ├── sample_audio.wav
│   ├── test_commands.json
│   └── fixtures.py
└── mocks/                                # Mock objects
    └── mock_llm.py
```

## Scripts

### `scripts/` - Utility Scripts

```
scripts/
├── verify_setup.py                       # Installation verification
├── setup_models.py                       # Download models
├── train_voice_profile.py                # Voice authentication training
├── reset_config.py                       # Reset to defaults
├── generate_encryption_key.py            # Generate secure key
├── migrate_database.py                   # Database migrations
├── backup_data.py                        # Backup user data
├── performance_test.py                   # Performance benchmarking
├── export_audit_logs.py                  # Export audit logs
├── test_microphone.py                    # Test audio input
├── generate_debug_report.py              # Generate debug info
└── check_quality.sh                      # Code quality checks
```

## Docker & Deployment

### `docker/` - Container Configuration

```
docker/
├── Dockerfile                            # Docker image definition
├── docker-compose.yml                    # Multi-container setup
├── docker-entrypoint.sh                  # Container startup script
└── .dockerignore                         # Files to exclude
```

## Plugins & Extensions

### `plugins/` - Custom Plugins

```
plugins/
├── __init__.py
├── example_plugin.py                     # Example plugin template
└── plugin_manager.py                     # Plugin management system
```

Create custom plugins to extend IRIS!

## Configuration & Credentials

### `credentials/` - API Credentials

```
credentials/
├── .gitkeep                              # Keep directory tracked
├── google-credentials.json               # Google API credentials
└── .gitignore                            # Ignore all secrets
```

**Important**: Always add to .gitignore!

## .github/ - GitHub Configuration

```
.github/
├── workflows/                            # CI/CD workflows
│   ├── tests.yml                         # Run tests on push
│   ├── lint.yml                          # Linting checks
│   └── deploy.yml                        # Deployment automation
├── ISSUE_TEMPLATE/                       # Issue templates
│   ├── bug_report.md
│   └── feature_request.md
├── pull_request_template.md              # PR template
└── CODE_OF_CONDUCT.md                    # Community guidelines
```

---

## Module Dependencies

```
┌─ Voice ──────────────────────────────────────┐
│ ├─ speech_to_text.py                         │
│ ├─ wake_word_detector.py                     │
│ ├─ text_to_speech.py                         │
│ └─ audio_processor.py                        │
└──────────────┬───────────────────────────────┘
               │
         ┌─────▼──────┐
         │   Brain    │◄─────────── Utils (config, logger, validators)
         │ (Core AI)  │
         └─────┬──────┘
               │
         ┌─────┴──────────────────────┐
         │                            │
┌────────▼──────────┐    ┌───────────▼────────┐
│   Executor        │    │  Security         │
│ ├─ commands       │    │ ├─ auth           │
│ ├─ app_launcher   │    │ ├─ encryption     │
│ └─ file_ops       │    │ └─ permissions    │
└───────┬───────────┘    └──────────┬────────┘
        │                           │
        └───────────┬───────────────┘
                    │
            ┌───────▼────────┐
            │   Storage      │
            │ ├─ database    │
            │ ├─ memory      │
            │ └─ logs        │
            └────────────────┘
```

---

## File Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Module | lowercase_with_underscores | `speech_to_text.py` |
| Class | PascalCase | `VoiceProcessor` |
| Function | lowercase_with_underscores | `process_audio()` |
| Constant | UPPERCASE_WITH_UNDERSCORES | `SAMPLE_RATE = 16000` |
| Test | test_*.py | `test_voice.py` |
| Fixture | *_fixture | `audio_fixture` |

---

## Adding New Features

### 1. Add Module
```bash
mkdir iris/new_module
touch iris/new_module/__init__.py
touch iris/new_module/core.py
```

### 2. Add Tests
```bash
touch tests/test_new_module.py
```

### 3. Add Documentation
```bash
touch docs/NEW_FEATURE.md
# Add to docs/README.md index
```

### 4. Update Configuration
```yaml
# Add to config.yaml if needed
new_module:
  setting: value
```

---

See [Architecture](ARCHITECTURE.md) for design details and [Contributing](CONTRIBUTING.md) for development guidelines.
