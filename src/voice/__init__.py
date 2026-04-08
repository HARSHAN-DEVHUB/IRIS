"""Voice I/O components: wake word, STT, TTS"""

from .wake_word import WakeWordDetector
from .transcriber import Transcriber
from .synthesis import TextToSpeech
from .audio_recorder import AudioRecorder
from .voice_manager import VoiceManager

__all__ = [
    "WakeWordDetector",
    "Transcriber",
    "TextToSpeech",
    "AudioRecorder",
    "VoiceManager"
]
