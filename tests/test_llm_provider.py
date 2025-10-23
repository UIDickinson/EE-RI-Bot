"""
Test LLM provider functionality
"""

import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import LLMProvider


class TestLLMProvider:
    """Test LLM provider initialization and functionality"""
    
    def test_provider_detection(self):
        """Test provider is correctly detected from environment"""
        provider = os.getenv("LLM_PROVIDER", "anthropic")
        llm = LLMProvider()
        
        assert llm.provider == provider
        print(f"✅ Detected provider: {llm.provider}")
    
    def test_api_key_loaded(self):
        """Test API key is loaded"""
        llm = LLMProvider()
        
        assert llm.api_key is not None
        assert len(llm.api_key) > 0
        print(f"✅ API key loaded (length: {len(llm.api_key)})")
    
    def test_model_selection(self):
        """Test model is correctly selected"""
        llm = LLMProvider()
        
        assert llm.model is not None
        assert len(llm.model) > 0
        print(f"✅ Model selected: {llm.model}")
    
    def test_client_initialization(self):
        """Test LLM client initializes"""
        llm = LLMProvider()
        
        assert llm.client is not None
        print(f"✅ Client initialized for {llm.provider}")
    
    @pytest.mark.slow
    def test_completion(self):
        """Test non-streaming completion (slow test)"""
        llm = LLMProvider()
        
        messages = [{"role": "user", "content": "Say 'Hello World' and nothing else."}]
        response = llm.create_completion(messages, max_tokens=50)
        
        assert response is not None
        assert len(response) > 0
        print(f"✅ Completion response: {response[:100]}")
    
    @pytest.mark.slow
    def test_streaming(self):
        """Test streaming completion (slow test)"""
        llm = LLMProvider()
        
        messages = [{"role": "user", "content": "Count from 1 to 5."}]
        chunks = []
        
        for chunk in llm.stream_completion(messages, max_tokens=100):
            chunks.append(chunk)
            if len(chunks) > 20:  # Limit chunks in test
                break
        
        assert len(chunks) > 0
        full_response = ''.join(chunks)
        print(f"✅ Streaming response ({len(chunks)} chunks): {full_response[:100]}")


def run_llm_tests():
    """Run LLM tests"""
    pytest.main([__file__, '-v', '-s', '-m', 'not slow'])


if __name__ == "__main__":
    run_llm_tests()