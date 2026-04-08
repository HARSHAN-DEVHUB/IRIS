"""Example/demo tools for FRIDAY"""

import logging
from typing import Any
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class GetTimeInput(BaseModel):
    """Input for get_time tool"""
    timezone: str = "UTC"

async def get_time_tool(input_data: dict) -> str:
    """Get current time"""
    timezone = input_data.get("timezone", "UTC")
    return f"Current time: {datetime.now().isoformat()} (requested timezone: {timezone})"

class GetDateInput(BaseModel):
    """Input for get_date tool"""
    pass

async def get_date_tool(input_data: dict) -> str:
    """Get current date"""
    return f"Current date: {datetime.now().strftime('%Y-%m-%d')}"

# Tool definitions for Claude
TIME_TOOL_DEFINITION = {
    "name": "get_time",
    "description": "Get the current time. Can optionally specify a timezone.",
    "input_schema": {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "Timezone (e.g., UTC, EST, PST). Defaults to UTC."
            }
        },
        "required": []
    }
}

DATE_TOOL_DEFINITION = {
    "name": "get_date",
    "description": "Get the current date",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
}
