"""Wake word detection using Porcupine"""

import logging
from typing import Optional, Callable
import pvporcupine
import pyaudio
import struct
import asyncio

logger = logging.getLogger(__name__)

class WakeWordDetector:
    """Detects wake word using Porcupine"""
    
    def __init__(self, access_key: str, wake_word: str = "hey friday"):
        """
        Initialize wake word detector
        
        Args:
            access_key: Porcupine access key
            wake_word: Wake word phrase (default: "hey friday")
        """
        self.access_key = access_key
        self.wake_word = wake_word
        self.is_listening = False
        
        try:
            # Initialize Porcupine
            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=[wake_word]
            )
            self.frame_length = self.porcupine.frame_length
            self.sample_rate = self.porcupine.sample_rate
            
            logger.info(f"Wake word detector ready for: '{wake_word}'")
        except Exception as e:
            logger.error(f"Failed to initialize Porcupine: {e}")
            raise
    
    async def start_listening(self, on_detected: Callable[[], None]) -> None:
        """
        Start passively listening for wake word
        
        Args:
            on_detected: Callback when wake word is detected
        """
        self.is_listening = True
        logger.info("Started listening for wake word...")
        
        try:
            # Open audio stream
            pa = pyaudio.PyAudio()
            stream = pa.open(
                rate=self.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.frame_length
            )
            
            while self.is_listening:
                # Read audio frame
                pcm = stream.read(self.frame_length)
                pcm = struct.unpack_from("h" * self.frame_length, pcm)
                
                # Check for wake word
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    logger.info(f"Wake word detected: {self.wake_word}")
                    if on_detected:
                        on_detected()
                
                # Yield to event loop
                await asyncio.sleep(0.01)
            
            stream.stop_stream()
            stream.close()
            pa.terminate()
        
        except Exception as e:
            logger.error(f"Error listening for wake word: {e}")
            raise
    
    async def stop_listening(self) -> None:
        """Stop listening for wake word"""
        self.is_listening = False
        logger.info("Stopped listening for wake word")
    
    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'porcupine'):
            self.porcupine.delete()
