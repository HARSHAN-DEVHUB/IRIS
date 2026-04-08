"""Tool router and execution system"""

import logging
from typing import Any, Callable, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class ToolRouter:
    """Manages tool execution and result handling"""
    
    def __init__(self):
        """Initialize tool router"""
        self.tools: Dict[str, Callable] = {}
        self.execution_history: list[dict] = []
    
    def register(self, name: str, handler: Callable) -> None:
        """
        Register a tool
        
        Args:
            name: Tool name
            handler: Async handler function
        """
        self.tools[name] = handler
        logger.info(f"Tool registered: {name}")
    
    async def execute(self, tool_name: str, tool_input: dict) -> Any:
        """
        Execute a tool
        
        Args:
            tool_name: Name of tool to execute
            tool_input: Input parameters for tool
            
        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        try:
            logger.info(f"Executing tool: {tool_name} with input: {tool_input}")
            result = await self.tools[tool_name](tool_input)
            
            # Log execution
            self.execution_history.append({
                "timestamp": datetime.now().isoformat(),
                "tool": tool_name,
                "input": tool_input,
                "result": str(result)[:200],  # Truncate for logging
                "status": "success"
            })
            
            return result
        
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            
            self.execution_history.append({
                "timestamp": datetime.now().isoformat(),
                "tool": tool_name,
                "input": tool_input,
                "error": str(e),
                "status": "failed"
            })
            
            raise
    
    def get_history(self, limit: int = 10) -> list[dict]:
        """Get recent tool executions"""
        return self.execution_history[-limit:]
