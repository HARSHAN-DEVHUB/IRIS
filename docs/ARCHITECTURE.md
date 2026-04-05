# 🏗️ Architecture

Complete system architecture overview and design patterns.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     IRIS AI Assistant                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │  Voice Input     │         │  Voice Output    │              │
│  │  (Microphone)    │         │  (Speaker)       │              │
│  └────────┬────────└┘         └────────▲─────────┘              │
│           │                            │                        │
│  ┌────────▼──────────┐        ┌────────┴──────────┐             │
│  │ Speech-to-Text    │        │  Text-to-Speech  │             │
│  │ (Whisper)         │        │  (pyttsx3)       │             │
│  └────────┬──────────┘        └────────▲──────────┘             │
│           │                            │                        │
│  ┌────────▼─────────────────────────────┴──────┐               │
│  │   Wake-Word Detector (Vosk)                  │               │
│  └────────┬─────────────────────────────┬──────┘               │
│           │                              │                      │
│           ▼                              ▼                      │
│  ┌──────────────────────────────────────────────┐               │
│  │        Natural Language Processor             │               │
│  │  ┌──────────────┐  ┌─────────────────┐      │               │
│  │  │ Intent       │  │ Entity          │      │               │
│  │  │ Parser       │  │ Extractor       │      │               │
│  │  │ (spaCy/NLP)  │  │ (spaCy/NLTK)    │      │               │
│  │  └──────────────┘  └─────────────────┘      │               │
│  └────────┬──────────────────────────────┬─────┘               │
│           │                              │                      │
│           ▼                              ▼                      │
│  ┌──────────────────────────────────────────────┐               │
│  │     Context Manager                          │               │
│  │  (Maintains conversation state & memory)     │               │
│  └────────┬──────────────────────────────┬─────┘               │
│           │                              │                      │
│           ▼                              ▼                      │
│  ┌──────────────────────────────────────────────┐               │
│  │     AI Brain (LLM Interface)                 │               │
│  │  ┌────────────┐  ┌──────────────────┐       │               │
│  │  │ Local LLM  │  │ Cloud LLM        │       │               │
│  │  │ (Ollama)   │  │ (OpenAI/Claude)  │       │               │
│  │  └────────────┘  └──────────────────┘       │               │
│  └────────┬──────────────────────────────┬─────┘               │
│           │                              │                      │
│           ▼                              ▼                      │
│  ┌──────────────────────────────────────────────┐               │
│  │     Command Executor                         │               │
│  │  ┌──────────────┐  ┌──────────────────┐     │               │
│  │  │ App Launcher │  │ File Operations  │     │               │
│  │  │              │  │                  │     │               │
│  │  │ Browser      │  │ Calendar/Email   │     │               │
│  │  │ Control      │  │                  │     │               │
│  │  │              │  │ System Commands  │     │               │
│  │  └──────────────┘  └──────────────────┘     │               │
│  └────────┬──────────────────────────────┬─────┘               │
│           │                              │                      │
│           ▼                              ▼                      │
│  ┌──────────────────────────────────────────────┐               │
│  │     Memory & Storage                         │               │
│  │  ┌──────────────┐  ┌──────────────────┐     │               │
│  │  │ Vector DB    │  │ SQLite Database  │     │               │
│  │  │ (ChromaDB)   │  │                  │     │               │
│  │  │              │  │ Encrypted Data   │     │               │
│  │  └──────────────┘  └──────────────────┘     │               │
│  └────────┬──────────────────────────────┬─────┘               │
│           │                              │                      │
│           ▼                              ▼                      │
│  ┌──────────────────────────────────────────────┐               │
│  │     Security & Authentication                │               │
│  │  ┌──────────────┐  ┌──────────────────┐     │               │
│  │  │ Voice Auth   │  │ Encryption       │     │               │
│  │  │              │  │ (AES-256)        │     │               │
│  │  │ Biometric    │  │ Permissions      │     │               │
│  │  └──────────────┘  └──────────────────┘     │               │
│  └──────────────────────────────────────────────┘               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
User Voice Input → Microphone → Audio Processing → Wake-word Detection
    ↓
Whisper (STT) → Text Transcription → NLP Engine (Intent Parsing)
    ↓
Intent + Entities → Context Manager → Conversation History & Memory
    ↓
LLM (Brain) ← Local (Ollama) or Cloud (OpenAI) ← Generate Response
    ↓
Response + Action → Command Executor ← File Ops, App Launch, APIs
    ↓
Execution Result → Response Generator → Final Response → TTS (pyttsx3)
    ↓
Audio Stream → Speaker
    ↓
↓ Logging & Storage ↓
Database & Encryption: Conversation History, User Preferences, Habits & Patterns, Audit Trail
```

## Core Components

### 1. Voice Module (`voice/`)
Handles all audio input/output operations.

- **speech_to_text.py** - Converts audio to text using Whisper
- **wake_word_detector.py** - Detects wake words using Vosk
- **text_to_speech.py** - Converts text to audio using pyttsx3
- **audio_processor.py** - Processes audio streams
- **audio_recorder.py** - Records audio from microphone

### 2. Brain Module (`brain/`)
Handles AI reasoning and natural language understanding.

- **llm_interface.py** - LLM abstraction layer (Ollama/OpenAI)
- **memory_manager.py** - Manages conversation history and embeddings
- **intent_parser.py** - Extracts user intent from text
- **entity_extractor.py** - Extracts named entities
- **context_manager.py** - Manages conversation context
- **response_generator.py** - Generates AI responses

### 3. Executor Module (`executor/`)
Handles task execution and command handling.

- **command_handler.py** - Routes and executes commands
- **command_registry.py** - Registers available commands
- **app_launcher.py** - Launches applications
- **file_operations.py** - File system operations
- **browser_control.py** - Web browser automation
- **calendar_email.py** - Calendar and email integration
- **system_commands.py** - OS-level operations

### 4. Security Module (`security/`)
Handles authentication and encryption.

- **authenticator.py** - User authentication
- **voice_profile.py** - Voice biometric training
- **encryption.py** - AES-256 encryption
- **permission_manager.py** - Role-based access control
- **audit_logger.py** - Security audit trail

### 5. Utils Module (`utils/`)
Common utilities and helpers.

- **logger.py** - Logging configuration
- **config_loader.py** - YAML/ENV configuration
- **helpers.py** - Utility functions
- **constants.py** - Constants and enums
- **validators.py** - Input validation

## Component Interaction

```
┌─ Voice ──────────────────────────────────────┐
│ ├─ speech_to_text.py                         │
│ ├─ wake_word_detector.py                     │
│ ├─ text_to_speech.py                         │
│ └─ audio_processor.py                        │
└──────────────┬───────────────────────────────┘
               │
         ┌─────▼──────┐
         │   Brain    │
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

## Execution Flow

### Typical Request Lifecycle

1. **Audio Capture** (50-500ms)
   - Microphone captures voice input
   - Audio processor prepares stream

2. **Wake-Word Detection** (0-100ms)
   - Vosk detector checks for wake words
   - Triggers if "IRIS" or "Hey IRIS" detected

3. **Speech-to-Text** (2-5s)
   - Whisper converts audio to text
   - Returns transcribed command

4. **NLP Processing** (100-500ms)
   - Intent parser determines action
   - Entity extractor pulls relevant data
   - Context manager loads history

5. **AI Processing** (3-10s)
   - LLM receives prompt with context
   - Generates appropriate response
   - Determines if action needed

6. **Command Execution** (< 1s - ∞)
   - Command executor routes to handler
   - Executes requested action
   - Collects result/status

7. **Response Generation** (100-300ms)
   - Response formatted
   - Action result incorporated
   - Final message prepared

8. **Text-to-Speech** (< 2s)
   - pyttsx3 converts text to audio
   - Plays through speakers

9. **Storage & Logging** (100-500ms)
   - Conversation stored in database
   - Encryption applied to sensitive data
   - Audit log updated

**Total Time**: 5-20 seconds (depending on LLM and network)

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Audio** | PyAudio | Audio I/O |
| **Speech-to-Text** | OpenAI Whisper | Voice recognition |
| **Wake-Word** | Vosk | Wake word detection |
| **Text-to-Speech** | pyttsx3 | Voice output |
| **NLP** | spaCy, NLTK | Language processing |
| **LLM** | Ollama/Llama 2, OpenAI GPT | AI reasoning |
| **LLM Framework** | LangChain | LLM abstraction |
| **Database** | SQLite | Data storage |
| **Vector DB** | ChromaDB | Semantic search |
| **Encryption** | Cryptography (AES-256) | Data security |
| **Testing** | Pytest | Unit tests |
| **Logging** | Python logging | Application logs |

## Design Principles

1. **Modularity** - Each component has single responsibility
2. **Extensibility** - Easy to add new commands and integrations
3. **Privacy** - Local-first architecture with optional cloud features
4. **Reliability** - Error handling and graceful degradation
5. **Performance** - Optimized for low latency
6. **Security** - Encryption and permission-based execution

---

See [Project Structure](PROJECT_STRUCTURE.md) for detailed directory layout and [API Reference](API_REFERENCE.md) for component interfaces.
