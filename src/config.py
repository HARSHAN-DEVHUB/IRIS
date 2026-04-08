"""Configuration management for FRIDAY"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """Central configuration object - COMPLETELY FREE & OPEN-SOURCE"""
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "friday.db"))
    
    # ===== LOCAL LLM (Ollama) =====
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    
    # ===== VOICE CONFIGURATION =====
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
    
    PIPER_VOICE = os.getenv("PIPER_VOICE", "en_US-amy-medium")
    PIPER_DATA_DIR = os.getenv("PIPER_DATA_DIR", str(PROJECT_ROOT / "piper_data"))
    
    USE_VAD = os.getenv("USE_VAD", "true").lower() == "true"
    
    # ===== OPTIONAL FREE SERVICES =====
    NEWS_SOURCES = os.getenv("NEWS_SOURCES", "bbc,cnn,techcrunch").split(",")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")  # Optional
    OPENWEATHER_CITY = os.getenv("OPENWEATHER_CITY", "New York")
    SEARCH_ENGINE = os.getenv("SEARCH_ENGINE", "duckduckgo")
    
    # ===== SYSTEM CONFIG =====
    FRIDAY_NAME = os.getenv("FRIDAY_NAME", "FRIDAY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> list[str]:
        """
        Validate minimum requirements.
        Ollama must be running locally.
        Returns list of issues found.
        """
        issues = []
        
        # Check Ollama connectivity
        try:
            import requests
            response = requests.get(f"{cls.OLLAMA_BASE_URL}/api/tags", timeout=2)
            if response.status_code != 200:
                issues.append(f"Ollama not responding at {cls.OLLAMA_BASE_URL}")
        except Exception as e:
            issues.append(f"Cannot connect to Ollama: {e}")
        
        return issues
    
    @classmethod
    def is_valid(cls) -> bool:
        """Check if Ollama is running"""
        return len(cls.validate()) == 0
    
    @classmethod
    def get_startup_instructions(cls) -> str:
        """Get instructions for first-time setup"""
        return """
FRIDAY is ready to run with FREE & OPEN-SOURCE components!

SETUP REQUIRED (first time only):

1. Install Ollama: https://ollama.ai
   
2. Pull a language model (choose one):
   ollama pull mistral           # Fast & powerful (recommended)
   ollama pull neural-chat       # Smaller, faster
   ollama pull llama2            # Larger, more capable
   
3. Start Ollama in background:
   ollama serve
   
4. Copy and configure .env:
   cp .env.example .env
   # Optional: edit .env to change model name or voice
   
5. Install Python dependencies:
   pip install -r requirements.txt
   
6. Run FRIDAY:
   python main.py

That's it! No paid API keys needed! 🎉
"""

# Create data directory if it doesn't exist
Config.DATA_DIR.mkdir(exist_ok=True)
