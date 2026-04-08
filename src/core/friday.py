"""Main FRIDAY Assistant orchestrator"""

import logging
from typing import Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
import asyncio

from src.config import Config
from .ollama_client import OllamaClient
from .tool_router import ToolRouter

logger = logging.getLogger(__name__)

@dataclass
class ConversationMessage:
    """Represents a single message in conversation"""
    timestamp: datetime
    speaker: str  # "user" or "friday"
    text: str
    tool_calls: Optional[list[dict]] = None

class FridayAssistant:
    """Main orchestrator for FRIDAY voice assistant"""
    
    def __init__(self):
        """Initialize FRIDAY assistant"""
        if not Config.is_valid():
            # Print startup instructions instead of failing
            print(Config.get_startup_instructions())
            raise RuntimeError("Ollama is not running. Please start Ollama first.")
        
        self.name = Config.FRIDAY_NAME
        self.conversation_history: list[ConversationMessage] = []
        self.tools_registry: dict[str, Callable] = {}
        
        # Initialize Ollama brain (free, local)
        self.ollama = OllamaClient(Config.OLLAMA_BASE_URL, Config.OLLAMA_MODEL)
        self.tool_router = ToolRouter()
        
        # System prompt
        self.system_prompt = self._build_system_prompt()
        
        logger.info(f"Initializing {self.name} (using Ollama locally)...")
    
    def _build_system_prompt(self) -> str:
        """Build FRIDAY's personality system prompt"""
        return f"""You are {self.name}, a female replacement intelligent digital assistant from the Marvel Cinematic Universe.

You are:
- Calm, collected, and professional
- Highly intelligent and capable
- Respectful but not obsequious
- Quick to assist with any request
- Able to execute various tools and access information
- Always honest about your capabilities and limitations

When responding:
1. Be concise but informative
2. Use a natural, conversational tone
3. Call tools when needed to get current information
4. Provide context when helpful
5. Ask clarifying questions if the request is ambiguous

You have access to various tools to help with tasks like checking news, weather, searching, managing calendar, email, music, smart home control, and more."""
    
    def register_tool(self, name: str, handler: Callable, definition: Optional[dict] = None) -> None:
        """
        Register a tool that FRIDAY can call
        
        Args:
            name: Tool name
            handler: Async function to handle tool execution
            definition: Claude tool definition (optional)
        """
        self.tools_registry[name] = handler
        self.tool_router.register(name, handler)
        
        # Register with Claude if definition provided
        if definition:
            self.claude.register_tool(definition, handler)
        
        logger.info(f"Registered tool: {name}")
    
    def add_message(self, speaker: str, text: str, tool_calls: Optional[list] = None) -> None:
        """Add a message to conversation history"""
        message = ConversationMessage(
            timestamp=datetime.now(),
            speaker=speaker,
            text=text,
            tool_calls=tool_calls
        )
        self.conversation_history.append(message)
    
    async def process_user_input(self, user_text: str) -> str:
        """
        Process user input and generate FRIDAY response
        
        Args:
            user_text: User's spoken/typed input
            
        Returns:
            FRIDAY's response text
        """
        self.add_message("user", user_text)
        
        # Build message history for Ollama
        messages = []
        for msg in self.conversation_history:
            messages.append({
                "role": "user" if msg.speaker == "user" else "assistant",
                "content": msg.text
            })
        
        try:
            # Get response from Ollama (local, free)
            response = await self.ollama.chat(
                messages=messages,
                system_prompt=self.system_prompt,
                max_tokens=512
            )
            
            response_text = response["text"]
            self.add_message("friday", response_text)
            
            logger.info(f"FRIDAY response generated")
            return response_text
        
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            error_response = f"Sorry, I encountered an error: {str(e)}"
            self.add_message("friday", error_response)
            return error_response
    
    async def process_user_input_stream(self, user_text: str):
        """
        Process user input and stream response
        
        Args:
            user_text: User's input
            
        Yields:
            Response text chunks
        """
        self.add_message("user", user_text)
        
        # Build message history for Ollama
        messages = []
        for msg in self.conversation_history:
            messages.append({
                "role": "user" if msg.speaker == "user" else "assistant",
                "content": msg.text
            })
        
        try:
            response_text = ""
            async for chunk in self.ollama.chat_stream(
                messages=messages,
                system_prompt=self.system_prompt
            ):
                response_text += chunk
                yield chunk
            
            self.add_message("friday", response_text)
            logger.info(f"FRIDAY response completed")
        
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            yield f"Sorry, I encountered an error: {str(e)}"
    
    def get_conversation_summary(self) -> list[dict]:
        """Get formatted conversation history"""
        return [
            {
                "timestamp": msg.timestamp.isoformat(),
                "speaker": msg.speaker,
                "text": msg.text,
                "tool_calls": msg.tool_calls
            }
            for msg in self.conversation_history
        ]
    
    def reset_conversation(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    async def listen_and_respond(self) -> None:
        """
        Main event loop: listen for wake word, capture audio, process input
        """
        # TODO: Implement wake word detection
        # TODO: Implement audio capture
        # TODO: Implement speech-to-text
        # TODO: Call process_user_input
        # TODO: Implement text-to-speech output
        pass
    
    def get_conversation_summary(self) -> list[dict]:
        """Get formatted conversation history"""
        return [
            {
                "timestamp": msg.timestamp.isoformat(),
                "speaker": msg.speaker,
                "text": msg.text,
                "tool_calls": msg.tool_calls
            }
            for msg in self.conversation_history
        ]
    
    def reset_conversation(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
