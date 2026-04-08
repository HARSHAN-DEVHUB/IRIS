"""Base tool class for all FRIDAY tools"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel

class ToolInput(BaseModel):
    """Base input schema for tools"""
    pass

class BaseTool(ABC):
    """Abstract base class for all FRIDAY tools"""
    
    name: str
    description: str
    input_schema: type[ToolInput]
    
    @abstractmethod
    async def execute(self, input_data: ToolInput) -> Any:
        """
        Execute the tool
        
        Args:
            input_data: Validated input data
            
        Returns:
            Tool execution result
        """
        pass
    
    def get_definition(self) -> dict:
        """Get Claude tool definition"""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": self.input_schema.model_json_schema()
            }
        }
