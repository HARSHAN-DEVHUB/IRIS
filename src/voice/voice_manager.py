"""High-level voice orchestration"""

import logging
import asyncio
from typing import Optional, Callable

from .wake_word import WakeWordDetector
from .transcriber import Transcriber
from .synthesis import TextToSpeech
from .audio_recorder import AudioRecorder

logger = logging.getLogger(__name__)

class VoiceManager:
    """Orchestrates all voice components: wake word -> listen -> transcribe -> TTS"""
    
    def __init__(
        self,
        porcupine_key: str,
        elevenlabs_key: str,
        elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM",
        wake_word: str = "hey friday",
        whisper_model: str = "base"
    ):
        """
        Initialize voice manager
        
        Args:
            porcupine_key: Porcupine API key
            elevenlabs_key: ElevenLabs API key
            elevenlabs_voice_id: Voice ID for TTS
            wake_word: Wake word phrase
            whisper_model: Whisper model size
        """
        self.wake_word_detector = WakeWordDetector(porcupine_key, wake_word)
        self.transcriber = Transcriber(whisper_model)
        self.synthesizer = TextToSpeech(elevenlabs_key, elevenlabs_voice_id)
        self.audio_recorder = AudioRecorder()
        
        self.is_active = False
        
        logger.info("Voice manager initialized")
    
    async def listen_for_wake_word(self, on_detected: Callable[[], None]) -> None:
        """
        Passively listen for wake word
        
        Args:
            on_detected: Callback when wake word detected
        """
        self.is_active = True
        await self.wake_word_detector.start_listening(on_detected)
    
    async def stop_listening(self) -> None:
        """Stop listening for wake word"""
        self.is_active = False
        await self.wake_word_detector.stop_listening()
    
    async def capture_audio_input(self) -> str:
        """
        Capture and transcribe spoken input
        
        Returns:
            Transcribed text
        """
        try:
            logger.info("Listening for input...")
            
            # Start recording
            await self.audio_recorder.start_recording()
            
            # Record until silence
            audio_bytes = await self.audio_recorder.record_until_silence(
                silence_threshold=500,
                silence_duration=0.5
            )
            
            # Stop recording
            await self.audio_recorder.stop_recording()
            
            if not audio_bytes:
                logger.warning("No audio captured")
                return ""
            
            # Transcribe
            logger.info("Transcribing audio...")
            text = await self.transcriber.transcribe_bytes(audio_bytes)
            logger.info(f"Transcribed: {text}")
            
            return text
        
        except Exception as e:
            logger.error(f"Audio capture failed: {e}")
            return ""
    
    async def speak_response(self, text: str) -> None:
        """
        Convert text to speech and play
        
        Args:
            text: Text to speak
        """
        try:
            logger.info(f"Speaking: {text[:50]}...")
            await self.synthesizer.speak_and_play(text)
        except Exception as e:
            logger.error(f"Speech output failed: {e}")
    
    async def full_voice_interaction(
        self,
        user_input_handler: Callable[[str], Callable]
    ) -> None:
        """
        Full voice interaction: listen -> process -> speak
        
        Args:
            user_input_handler: Async callable that takes text and returns response
        """
        try:
            # Capture user input
            user_text = await self.capture_audio_input()
            
            if not user_text:
                logger.warning("No input detected")
                return
            
            # Process through handler
            response = await user_input_handler(user_text)
            
            # Speak response
            await self.speak_response(response)
        
        except Exception as e:
            logger.error(f"Voice interaction failed: {e}")
            await self.speak_response("Sorry, I encountered an error.")
