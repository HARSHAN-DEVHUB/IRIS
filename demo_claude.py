#!/usr/bin/env python3
"""Demo script to test FRIDAY with FREE local LLM (Ollama)"""

import asyncio
import logging
from src.config import Config
from src.core import FridayAssistant
from src.tools.examples import get_time_tool, get_date_tool, TIME_TOOL_DEFINITION, DATE_TOOL_DEFINITION

# Configure logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def demo():
    """Run demo"""
    logger.info("=" * 70)
    logger.info("Starting FRIDAY Demo with FREE Local LLM (Ollama)")
    logger.info("=" * 70)
    
    try:
        # Initialize FRIDAY
        friday = FridayAssistant()
        
        # Register example tools
        friday.register_tool("get_time", get_time_tool, TIME_TOOL_DEFINITION)
        friday.register_tool("get_date", get_date_tool, DATE_TOOL_DEFINITION)
        
        logger.info(f"✓ FRIDAY initialized with tools: get_time, get_date")
        logger.info(f"✓ Using model: {Config.OLLAMA_MODEL}")
        logger.info(f"✓ Ollama server: {Config.OLLAMA_BASE_URL}")
        
        # Demo conversation
        test_queries = [
            "What time is it?",
            "Tell me the current date please",
            "What's today's date and time?",
            "Hello, who are you?",
        ]
        
        for query in test_queries:
            logger.info(f"\n{'='*70}")
            logger.info(f"User: {query}")
            logger.info(f"{'='*70}")
            
            try:
                response = await friday.process_user_input(query)
                logger.info(f"FRIDAY: {response}")
            except Exception as e:
                logger.error(f"Error: {e}")
                break
        
        # Print conversation summary
        logger.info(f"\n{'='*70}")
        logger.info("Conversation Summary:")
        logger.info(f"{'='*70}")
        for msg in friday.get_conversation_summary():
            text_preview = msg['text'][:70] + "..." if len(msg['text']) > 70 else msg['text']
            logger.info(f"[{msg['speaker'].upper()}] {text_preview}")
    
    except RuntimeError as e:
        logger.error(f"\n✗ Setup Error: {e}")
        print(Config.get_startup_instructions())
    except Exception as e:
        logger.error(f"✗ Demo error: {e}")

if __name__ == "__main__":
    asyncio.run(demo())
