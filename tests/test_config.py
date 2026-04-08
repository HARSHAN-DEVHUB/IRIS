"""Tests for configuration"""

import pytest
from src.config import Config

def test_config_loads():
    """Test that configuration loads"""
    assert Config.PROJECT_ROOT.exists()
    assert Config.DATA_DIR.exists()

def test_config_validation():
    """Test configuration validation"""
    # Should have validation method
    missing = Config.validate()
    assert isinstance(missing, list)
