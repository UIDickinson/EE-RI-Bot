"""
Pytest configuration and shared fixtures
"""

import pytest
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


@pytest.fixture(scope="session")
def check_env_vars():
    """Check required environment variables are set"""
    required_vars = ["LLM_PROVIDER"]
    
    provider = os.getenv("LLM_PROVIDER", "anthropic")
    
    if provider == "anthropic":
        required_vars.append("ANTHROPIC_API_KEY")
    elif provider == "openai":
        required_vars.append("OPENAI_API_KEY")
    elif provider == "openrouter":
        required_vars.append("OPENROUTER_API_KEY")
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        pytest.skip(f"Missing environment variables: {', '.join(missing_vars)}")
    
    return True