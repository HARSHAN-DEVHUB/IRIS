#!/usr/bin/env python3
"""Test voice pipeline components individually"""

import asyncio
import logging
from src.config import Config
from src.voice import (
    WakeWordDetector,
    Transcriber,
    TextToSpeech,
    AudioRecorder,
    VoiceManager
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_transcriber():
    """Test speech-to-text"""
    logger.info("\n" + "="*60)
    logger.info("Testing Transcriber (Speech-to-Text)")
    logger.info("="*60)
    
    try:
        transcriber = Transcriber(model_size="base")
        
        # Create a simple test audio file
        import numpy as np
        import soundfile as sf
        
        # Generate a 2-second sine wave at 440Hz
        sample_rate = 16000
        duration = 2
        frequency = 440
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * frequency * t) * 0.3
        
        sf.write('/tmp/test_audio.wav', audio, sample_rate)
        
        # Transcribe
        text = await transcriber.transcribe('/tmp/test_audio.wav')
        logger.info(f"Transcription result: '{text}' (empty expected for sine wave)")
        
    except Exception as e:
        logger.error(f"Transcriber test failed: {e}")

async def test_audio_recorder():
    """Test audio recording"""
    logger.info("\n" + "="*60)
    logger.info("Testing Audio Recorder")
    logger.info("="*60)
    
    try:
        recorder = AudioRecorder()
        logger.info("Recording for 3 seconds...")
        
        await recorder.start_recording()
        
        # Record for 3 seconds
        for i in range(30):
            await asyncio.sleep(0.1)
        
        audio_bytes = await recorder.stop_recording()
        logger.info(f"Recorded {len(audio_bytes)} bytes")
        
    except Exception as e:
        logger.error(f"Audio recorder test failed: {e}")

async def test_tts():
    """Test text-to-speech"""
    logger.info("\n" + "="*60)
    logger.info("Testing Text-to-Speech")
    logger.info("="*60)
    
    if not Config.ELEVENLABS_API_KEY:
        logger.warning("ELEVENLABS_API_KEY not set, skipping TTS test")
        return
    
    try:
        tts = TextToSpeech(Config.ELEVENLABS_API_KEY)
        
        # Get available voices
        voices = tts.get_available_voices()
        logger.info(f"Available voices: {len(voices)}")
        
        # Test speaking (but don't actually play audio in test)
        logger.info("Testing TTS API...")
        
    except Exception as e:
        logger.error(f"TTS test failed: {e}")

async def test_voice_manager_transcribe():
    """Test voice manager with transcription"""
    logger.info("\n" + "="*60)
    logger.info("Testing Voice Manager (Transcription)")
    logger.info("="*60)
    
    try:
        voice_mgr = VoiceManager(
            porcupine_key=Config.PORCUPINE_ACCESS_KEY or "dummy",
            elevenlabs_key=Config.ELEVENLABS_API_KEY or "dummy"
        )
        
        logger.info("Voice manager initialized successfully")
        
    except Exception as e:
        logger.warning(f"Voice manager test had issues (expected if keys missing): {e}")

async def main():
    """Run all tests"""
    logger.info("Voice Pipeline Component Tests")
    
    # Only test transcriber if model can be loaded
    try:
        await test_transcriber()
    except Exception as e:
        logger.warning(f"Skipping transcriber test: {e}")
    
    # Test audio recorder
    try:
        await test_audio_recorder()
    except Exception as e:
        logger.warning(f"Skipping audio recorder test: {e}")
    
    # Test TTS if API key available
    await test_tts()
    
    # Test voice manager initialization
    await test_voice_manager_transcribe()
    
    logger.info("\n" + "="*60)
    logger.info("Voice pipeline tests completed!")
    logger.info("="*60)

if __name__ == "__main__":
    asyncio.run(main())
