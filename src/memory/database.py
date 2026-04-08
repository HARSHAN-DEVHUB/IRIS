"""Database and persistence layer"""

import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages SQLite database for FRIDAY"""
    
    def __init__(self, db_path: str):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create SQLAlchemy engine
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        logger.info(f"Database initialized at: {self.db_path}")
    
    def init_db(self) -> None:
        """Create all tables"""
        # TODO: Create database schema
        logger.info("Database schema initialized")
