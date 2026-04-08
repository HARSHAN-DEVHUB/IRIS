"""Text-to-speech using ElevenLabs"""

import logging
from typing import Optional
import asyncio
from io import BytesIO
import pyaudio
import numpy as np

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Converts text to speech using ElevenLabs"""
    
    def __init__(self, api_key: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
        """
        Initialize text-to-speech engine
        
        Args:
            api_key: ElevenLabs API key
            voice_id: Voice ID to use (default: Rachel - female voice)
        """
        self.api_key = api_key
        self.voice_id = voice_id
        
        # Import here to avoid dependency issues
        try:
            from elevenlabs import client
            self.client = client.ElevenLabsClient(api_key=api_key)
            logger.info(f"Text-to-speech initialized with voice: {voice_id}")
        except ImportError:
            logger.error("ElevenLabs client not available")
            self.client = None
    
    async def speak(
        self,
        text: str,
        stream: bool = True,
        model_id: str = "eleven_monolingual_v1"
    ) -> Optional[bytes]:
        """
        Convert text to speech and play/return audio
        
        Args:
            text: Text to convert
            stream: Whether to stream playback
            model_id: ElevenLabs model ID
            
        Returns:
            Audio bytes if stream=False, None if stream=True
        """
        if not self.client:
            logger.warning("ElevenLabs client not initialized")
            return None
        
        try:
            logger.info(f"Speaking: {text[:50]}...")
            
            # Generate speech
            loop = asyncio.get_event_loop()
            audio = await loop.run_in_executor(
                None,
                lambda: self.client.text_to_speech.convert(
                    voice_id=self.voice_id,
                    text=text,
                    model_id=model_id
                )
            )
            
            if stream:
                # Play audio immediately
                await self._play_audio(audio)
                return None
            else:
                # Return audio bytes
                return audio
        
        except Exception as e:
            logger.error(f"Text-to-speech failed: {e}")
            return None
    
    async def speak_and_play(self, text: str) -> None:
        """Convert text to speech and play immediately"""
        await self.speak(text, stream=True)
    
    async def _play_audio(self, audio_bytes: bytes) -> None:
        """
        Play audio bytes using PyAudio
        
        Args:
            audio_bytes: Audio data in WAV format
        """
        try:
            # Parse WAV file
            import wave
            audio_io = BytesIO(audio_bytes)
            
            with wave.open(audio_io, 'rb') as wav_file:
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                
                # Initialize PyAudio
                pa = pyaudio.PyAudio()
                stream = pa.open(
                    format=pa.get_format_from_width(sample_width),
                    channels=channels,
                    rate=sample_rate,
                    output=True
                )
                
                # Play audio
                chunk_size = 4096
                while True:
                    data = wav_file.readframes(chunk_size)
                    if not data:
                        break
                    stream.write(data)
                
                stream.stop_stream()
                stream.close()
                pa.terminate()
            
            logger.info("Audio playback completed")
        
        except Exception as e:
            logger.error(f"Audio playback failed: {e}")
    
    def get_available_voices(self) -> dict:
        """Get list of available ElevenLabs voices"""
        try:
            if not self.client:
                return {}
            
            voices = self.client.voices.get_all()
            return {voice.voice_id: voice.name for voice in voices}
        except Exception as e:
            logger.error(f"Failed to get voices: {e}")
            return {}
