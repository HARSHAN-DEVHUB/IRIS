"""Claude AI client for FRIDAY"""

import logging
from typing import Optional, Callable, Any
import json
import anthropic

logger = logging.getLogger(__name__)

class ClaudeClient:
    """Wrapper for Anthropic Claude API with tool calling"""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize Claude client
        
        Args:
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.api_key = api_key
        self.model = model
        self.client = anthropic.Anthropic(api_key=api_key)
        self.tools: list[dict] = []
        self.tool_handlers: dict[str, Callable] = {}
        
        logger.info(f"Claude client initialized with model: {model}")
    
    def register_tool(self, definition: dict, handler: Callable) -> None:
        """
        Register a tool that Claude can call
        
        Args:
            definition: Tool definition (name, description, input_schema)
            handler: Async function to handle tool execution
        """
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
        Send message to Claude and get response with tool handling
        
        Args:
            messages: Conversation history
            system_prompt: System prompt for context
            temperature: Sampling temperature
            max_tokens: Max tokens for response
            
        Returns:
            Response with content and any tool calls
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        if self.tools:
            kwargs["tools"] = self.tools
        
        # Initial request
        response = self.client.messages.create(**kwargs)
        
        # Handle tool use in a loop
        while response.stop_reason == "tool_use":
            # Extract tool use blocks
            tool_results = []
            
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_use_id = block.id
                    
                    logger.info(f"Claude called tool: {tool_name}")
                    
                    # Execute tool
                    if tool_name in self.tool_handlers:
                        try:
                            result = await self.tool_handlers[tool_name](tool_input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": tool_use_id,
                                "content": str(result)
                            })
                        except Exception as e:
                            logger.error(f"Tool error: {e}")
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": tool_use_id,
                                "content": f"Error: {str(e)}",
                                "is_error": True
                            })
                    else:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": f"Unknown tool: {tool_name}",
                            "is_error": True
                        })
            
            # Add assistant response and tool results to messages
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            
            # Continue conversation
            kwargs["messages"] = messages
            response = self.client.messages.create(**kwargs)
        
        # Extract final text response
        final_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                final_text += block.text
        
        return {
            "text": final_text,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }
    
    async def chat_stream(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ):
        """
        Stream response from Claude
        
        Args:
            messages: Conversation history
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Max tokens
            
        Yields:
            Text chunks as they arrive
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        if self.tools:
            kwargs["tools"] = self.tools
        
        with self.client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text
