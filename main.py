"""FRIDAY Main Entry Point"""

import asyncio
import logging
from src.config import Config
from src.core import FridayAssistant
from src.voice import VoiceManager
from src.tools.examples import get_time_tool, get_date_tool, TIME_TOOL_DEFINITION, DATE_TOOL_DEFINITION

# Configure logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point"""
    try:
        logger.info("=" * 60)
        logger.info(f"Starting {Config.FRIDAY_NAME}...")
        logger.info("=" * 60)
        
        # Validate configuration
        if not Config.is_valid():
            missing = Config.validate()
            logger.error(f"Missing required configuration: {missing}")
            logger.error("Please check your .env file")
            return
        
        # Initialize FRIDAY brain
        friday = FridayAssistant()
        
        # Register example tools
        friday.register_tool("get_time", get_time_tool, TIME_TOOL_DEFINITION)
        friday.register_tool("get_date", get_date_tool, DATE_TOOL_DEFINITION)
        
        # Initialize voice components
        voice_manager = VoiceManager(
            porcupine_key=Config.PORCUPINE_ACCESS_KEY,
            elevenlabs_key=Config.ELEVENLABS_API_KEY,
            elevenlabs_voice_id=Config.ELEVENLABS_VOICE_ID,
            wake_word=Config.WAKE_WORD
        )
        
        logger.info(f"{Config.FRIDAY_NAME} is ready!")
        logger.info(f"Listening for wake word: '{Config.WAKE_WORD}'")
        
        # Main loop
        async def on_wake_word_detected():
            """Callback when wake word is detected"""
            logger.info(f"Wake word detected! Processing interaction...")
            
            # Capture user input and process
            user_text = await voice_manager.capture_audio_input()
            
            if user_text:
                # Get FRIDAY's response
                response = await friday.process_user_input(user_text)
                
                # Speak response
                await voice_manager.speak_response(response)
        
        # Start listening for wake word
        await voice_manager.listen_for_wake_word(on_wake_word_detected)
        
    except KeyboardInterrupt:
        logger.info("Shutting down FRIDAY...")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
