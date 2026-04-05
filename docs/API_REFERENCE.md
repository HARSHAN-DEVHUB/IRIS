# 📚 API Reference

Complete API documentation for all IRIS modules.

## Core Modules

### 1. VoiceProcessor (`voice/speech_to_text.py`)

Audio input/output handling with speech recognition.

```python
from voice.speech_to_text import VoiceProcessor

processor = VoiceProcessor(language="en-US", model="base")
```

#### Methods

**`listen(timeout=10) -> str`**
- Listen for voice input and return transcription
- Returns: Transcribed text
- Raises: `AudioTimeoutError` if no speech detected

**`speak(text, speed=1.0) -> None`**
- Convert text to speech and play through speakers
- Args: `text` (str), `speed` (float: 0.5-2.0)
- Returns: None

**`transcribe_file(path: str) -> str`**
- Transcribe audio file
- Args: `path` (str) - Path to audio file
- Returns: Transcribed text

**`get_available_voices() -> List[Dict]`**
- Get list of available TTS voices
- Returns: List of voice dictionaries with id and name

**`set_voice(voice_id: str) -> None`**
- Set TTS voice
- Args: `voice_id` (str) - Voice ID from available voices
- Returns: None

**`set_speech_rate(rate: float) -> None`**
- Set speech rate (0.5 = slow, 1.0 = normal, 2.0 = fast)
- Args: `rate` (float)
- Returns: None

**`close() -> None`**
- Cleanup and close resources
- Returns: None

---

### 2. LLMInterface (`brain/llm_interface.py`)

Large Language Model abstraction for multiple providers.

```python
from brain.llm_interface import LLMInterface

llm = LLMInterface(provider="ollama", model="llama2")
```

#### Methods

**`generate(prompt: str, temperature: float = 0.7, max_tokens: int = 200) -> str`**
- Generate text response
- Returns: Generated text

**`chat(messages: List[Dict]) -> Dict`**
- Multi-turn conversation
- Args: Messages list with role and content
- Returns: Response dictionary

**`parse_intent(text: str) -> Dict`**
- Extract intent from text
- Returns: Intent dictionary with action and confidence

**`extract_entities(text: str) -> List[Dict]`**
- Extract named entities
- Returns: List of entities with type and value

**`count_tokens(text: str) -> int`**
- Count tokens in text
- Returns: Token count

**`is_available() -> bool`**
- Check if LLM is available
- Returns: Boolean

---

### 3. CommandExecutor (`executor/command_handler.py`)

Command routing and execution engine.

```python
from executor.command_handler import CommandExecutor

executor = CommandExecutor()
```

#### Methods

**`execute(command: str, params: Dict) -> Dict`**
- Execute a command with parameters
- Returns: Result dictionary with status and data

**`get_available_commands() -> List[str]`**
- Get list of available commands
- Returns: List of command names

**`register_command(name: str, func: Callable) -> None`**
- Register a custom command
- Args: Command name and function
- Returns: None

**`list_running_apps() -> List[str]`**
- Get list of running applications
- Returns: List of app names

**`is_command_available(command: str) -> bool`**
- Check if command is available
- Returns: Boolean

---

### 4. MemoryManager (`brain/memory_manager.py`)

Storage and retrieval of conversation history and user data.

```python
from brain.memory_manager import MemoryManager

memory = MemoryManager()
```

#### Methods

**`store(key: str, value: Any, ttl: Optional[int] = None) -> None`**
- Store data in memory
- Args: key, value, optional TTL in seconds
- Returns: None

**`retrieve(key: str) -> Any`**
- Retrieve stored data
- Returns: Stored value or None

**`update(key: str, value: Any) -> None`**
- Update existing data
- Returns: None

**`delete(key: str) -> None`**
- Delete data from memory
- Returns: None

**`semantic_search(query: str, limit: int = 5) -> List[Dict]`**
- Search using vector embeddings
- Returns: List of results with scores

**`store_conversation(role: str, content: str, metadata: Dict = None) -> None`**
- Store conversation turn
- Args: role ("user"/"assistant"), content, metadata
- Returns: None

**`get_conversation_history(limit: int = 10) -> List[Dict]`**
- Get recent conversation turns
- Returns: List of conversation turns

**`export_data() -> Dict`**
- Export all stored data
- Returns: Dictionary with all data

**`clear_all() -> None`**
- Clear all memory
- Returns: None

---

### 5. Authenticator (`security/authenticator.py`)

User authentication and permission management.

```python
from security.authenticator import Authenticator

auth = Authenticator()
```

#### Methods

**`verify_voice() -> bool`**
- Verify user by voice biometrics
- Returns: Boolean

**`train_voice_profile(num_samples: int, phrases: List[str]) -> None`**
- Train voice authentication model
- Args: Number of samples, list of phrases to record
- Returns: None

**`get_auth_status() -> Dict`**
- Get current authentication status
- Returns: Status dictionary

**`set_permission(user: str, action: str, resource: str, allowed: bool) -> None`**
- Set permission for user
- Returns: None

**`check_permission(action: str, resource: str) -> bool`**
- Check if action is permitted
- Returns: Boolean

---

## Utility Functions

### Logger (`utils/logger.py`)

```python
from utils.logger import get_logger

logger = get_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Config Loader (`utils/config_loader.py`)

```python
from utils.config_loader import ConfigLoader

config = ConfigLoader.load_config()

voice_settings = config["voice"]
audio_settings = config["audio"]
llm_settings = config["llm"]
```

### Helpers (`utils/helpers.py`)

```python
from utils.helpers import *

# Parse time/date expressions
time = parse_time_expression("tomorrow at 2 PM")
date = parse_date_expression("next Monday")

# Get current time
now = get_current_time()

# Convert text
upper = convert_to_uppercase("hello")
lower = convert_to_lowercase("HELLO")

# Extract paths
paths = extract_file_paths("~/Documents/file.txt")

# Validate input
is_valid = validate_email("user@example.com")
```

---

## Exception Types

```python
# Audio Exceptions
class AudioError(Exception): pass
class MicrophoneError(AudioError): pass
class SpeakerError(AudioError): pass
class AudioTimeoutError(AudioError): pass

# LLM Exceptions
class LLMError(Exception): pass
class LLMConnectionError(LLMError): pass
class LLMTimeoutError(LLMError): pass

# Command Exceptions
class CommandError(Exception): pass
class CommandNotFoundError(CommandError): pass
class CommandExecutionError(CommandError): pass

# Security Exceptions
class AuthenticationError(Exception): pass
class PermissionDeniedError(AuthenticationError): pass
class EncryptionError(Exception): pass
```

---

## Configuration Objects

### VoiceConfig

```python
{
    "language": "en-US",
    "confidence_threshold": 0.7,
    "wake_words": ["iris", "hey iris"],
    "enable_wake_word": True,
    "timeout": 10
}
```

### AudioConfig

```python
{
    "sample_rate": 16000,
    "chunk_size": 1024,
    "input_device": 0,
    "output_device": 0,
    "noise_threshold": 0.3
}
```

### LLMConfig

```python
{
    "provider": "ollama",
    "model": "llama2",
    "temperature": 0.7,
    "max_tokens": 512,
    "timeout": 30
}
```

---

See [Commands Reference](COMMANDS.md) for available voice commands and [Configuration](CONFIGURATION.md) for setup details.
