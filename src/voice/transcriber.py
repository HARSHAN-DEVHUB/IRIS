"""Speech-to-text using faster-whisper"""

import logging
from typing import Optional
import numpy as np
from faster_whisper import WhisperModel
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class Transcriber:
    """Converts speech to text using faster-whisper"""
    
    def __init__(self, model_size: str = "base", device: str = "auto"):
        """
        Initialize transcriber
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: Device to use (auto, cpu, cuda)
        """
        self.model_size = model_size
        self.device = device
        self.executor = ThreadPoolExecutor(max_workers=1)
        
        try:
            # Load faster-whisper model
            self.model = WhisperModel(
                model_size,
                device=device,
                compute_type="float16" if device != "cpu" else "float32"
            )
            logger.info(f"Transcriber initialized with model: {model_size} on {device}")
        except Exception as e:
            logger.error(f"Failed to load whisper model: {e}")
            raise
    
    async def transcribe(self, audio_path: str, language: Optional[str] = None) -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Language code (auto-detect if None)
            
        Returns:
            Transcribed text
        """
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            segments, info = await loop.run_in_executor(
                self.executor,
                lambda: self.model.transcribe(
                    audio_path,
                    language=language,
                    beam_size=5,
                    best_of=5
                )
            )
            
            # Combine segments into full text
            text = " ".join([segment.text for segment in segments])
            logger.info(f"Transcribed: {text[:100]}...")
            return text
        
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    async def transcribe_bytes(
        self,
        audio_bytes: bytes,
        sample_rate: int = 16000,
        language: Optional[str] = None
    ) -> str:
        """
        Transcribe audio bytes to text
        
        Args:
            audio_bytes: Raw audio bytes
            sample_rate: Sample rate of audio
            language: Language code
            
        Returns:
            Transcribed text
        """
        try:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Run transcription in executor
            loop = asyncio.get_event_loop()
            segments, info = await loop.run_in_executor(
                self.executor,
                lambda: self.model.transcribe(
                    audio_data,
                    language=language,
                    beam_size=5
                )
            )
            
            text = " ".join([segment.text for segment in segments])
            return text
        
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    async def transcribe_stream(self, audio_frames: list[bytes]) -> str:
        """
        Transcribe streaming audio frames
        
        Args:
            audio_frames: List of audio frame bytes
            
        Returns:
            Transcribed text
        """
        try:
            # Combine frames into single audio bytes
            combined = b"".join(audio_frames)
            text = await self.transcribe_bytes(combined)
            return text
        
        except Exception as e:
            logger.error(f"Stream transcription failed: {e}")
            raise
