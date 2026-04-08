"""Ollama AI client (free alternative to Claude)"""

import logging
from typing import Optional, Callable
import json
import httpx
import asyncio

logger = logging.getLogger(__name__)

class OllamaClient:
    """Wrapper for Ollama API (free, local LLM)"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        """
        Initialize Ollama client
        
        Args:
            base_url: Ollama server URL
            model: Model name (mistral, llama2, neural-chat, etc.)
        """
        self.base_url = base_url
        self.model = model
        self.tools: list[dict] = []
        self.tool_handlers: dict[str, Callable] = {}
        
        logger.info(f"Ollama client initialized with model: {model}")
    
    def register_tool(self, definition: dict, handler: Callable) -> None:
        """Register a tool that the model can call"""
        self.tools.append(definition)
        self.tool_handlers[definition["name"]] = handler
        logger.info(f"Registered tool: {definition['name']}")
    
    async def chat(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> dict:
        """
        Send message to Ollama and get response
        
        Args:
            messages: Conversation history
            system_prompt: System prompt for context
            temperature: Sampling temperature
            max_tokens: Max tokens for response
            
        Returns:
            Response with content
        """
        # Build request
        request_data = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "temperature": temperature,
        }
        
        if system_prompt:
            # Add system message to start of conversation
            messages_with_system = [
                {"role": "system", "content": system_prompt},
                *messages
            ]
            request_data["messages"] = messages_with_system
        
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=request_data
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Extract response
                response_text = result.get("message", {}).get("content", "")
                
                return {
                    "text": response_text,
                    "model": result.get("model", self.model),
                    "done": result.get("done", True)
                }
        
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise
    
    async def chat_stream(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ):
        """
        Stream response from Ollama
        
        Args:
            messages: Conversation history
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Max tokens
            
        Yields:
            Text chunks as they arrive
        """
        request_data = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "temperature": temperature,
        }
        
        if system_prompt:
            messages_with_system = [
                {"role": "system", "content": system_prompt},
                *messages
            ]
            request_data["messages"] = messages_with_system
        
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json=request_data
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                if "message" in chunk and "content" in chunk["message"]:
                                    yield chunk["message"]["content"]
                            except json.JSONDecodeError:
                                pass
        
        except Exception as e:
            logger.error(f"Ollama streaming error: {e}")
            raise
