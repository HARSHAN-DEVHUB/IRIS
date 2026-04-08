"""Audio capture and management"""

import logging
import pyaudio
import numpy as np
import asyncio
from typing import Optional, Callable

logger = logging.getLogger(__name__)

class AudioRecorder:
    """Records audio from microphone"""
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024
    ):
        """
        Initialize audio recorder
        
        Args:
            sample_rate: Sample rate in Hz
            channels: Number of channels (1 = mono)
            chunk_size: Frames per buffer
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.is_recording = False
        self.audio_data = []
        
        self.pa = pyaudio.PyAudio()
        self.stream = None
    
    async def start_recording(self) -> None:
        """Start recording audio"""
        self.is_recording = True
        self.audio_data = []
        
        try:
            self.stream = self.pa.open(
                rate=self.sample_rate,
                channels=self.channels,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            logger.info("Audio recording started")
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            raise
    
    async def record_until_silence(
        self,
        silence_threshold: float = 500,
        silence_duration: float = 1.0
    ) -> bytes:
        """
        Record until silence is detected
        
        Args:
            silence_threshold: Audio level threshold for silence
            silence_duration: Duration of silence before stopping (seconds)
            
        Returns:
            Recorded audio bytes
        """
        silence_frames = int(self.sample_rate / self.chunk_size * silence_duration)
        silent_count = 0
        
        try:
            while self.is_recording:
                # Read audio chunk
                data = self.stream.read(self.chunk_size)
                self.audio_data.append(data)
                
                # Check for silence
                audio_level = np.frombuffer(data, dtype=np.int16).max()
                
                if audio_level < silence_threshold:
                    silent_count += 1
                    if silent_count > silence_frames:
                        logger.info("Silence detected, stopping recording")
                        break
                else:
                    silent_count = 0
                
                # Yield to event loop
                await asyncio.sleep(0.01)
            
            # Combine audio chunks
            audio_bytes = b"".join(self.audio_data)
            return audio_bytes
        
        except Exception as e:
            logger.error(f"Recording failed: {e}")
            raise
    
    async def stop_recording(self) -> bytes:
        """Stop recording and return audio"""
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        audio_bytes = b"".join(self.audio_data)
        logger.info(f"Recording stopped ({len(audio_bytes)} bytes)")
        return audio_bytes
    
    def __del__(self):
        """Cleanup resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.pa:
            self.pa.terminate()
