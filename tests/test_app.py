"""
Test main application module
"""

import pytest
import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import EEResearchScout, LLMProvider


class TestEEResearchScout:
    """Test main agent functionality"""
    
    def setup_method(self):
        self.agent = EEResearchScout(name="test-agent")
    
    def test_initialization(self):
        """Test agent initializes correctly"""
        assert self.agent is not None
        assert self.agent.name == "test-agent"
        assert self.agent.llm is not None
        assert self.agent.research_tools is not None
        assert self.agent.component_analyzer is not None
        assert self.agent.supply_chain is not None
        print("✅ Agent initialization test passed")
    
    def test_domain_priorities(self):
        """Test domain priorities are configured"""
        assert len(self.agent.domain_priorities) > 0
        assert "embedded_systems" in self.agent.domain_priorities
        assert "power_management" in self.agent.domain_priorities
        assert self.agent.domain_priorities["embedded_systems"] == 1.0
        print("✅ Domain priorities test passed")
    
    @pytest.mark.asyncio
    async def test_analyze_query(self):
        """Test query analysis"""
        queries = [
            "Find GaN power ICs",
            "Compare STM32 vs ESP32",
            "Check nRF52840 availability"
        ]
        
        for query in queries:
            result = await self.agent._analyze_query(query)
            assert isinstance(result, dict)
            assert "domains" in result
            assert "strategy" in result
            print(f"✅ Query analysis passed for: {query[:30]}...")
    
    @pytest.mark.asyncio
    async def test_search_research(self):
        """Test research search"""
        result = await self.agent._search_research(
            query="power management",
            domains=["power_management"]
        )
        
        assert isinstance(result, dict)
        assert "papers" in result
        assert "metadata" in result
        print(f"✅ Research search test passed")
    
    @pytest.mark.asyncio
    async def test_analyze_components(self):
        """Test component analysis"""
        components = ["STM32F407", "ESP32-S3"]
        result = await self.agent._analyze_components(components)
        
        assert isinstance(result, dict)
        assert len(result) > 0
        print(f"✅ Component analysis test passed")


class TestLLMProviderDetailed:
    """Additional LLM provider tests"""
    
    def test_provider_selection(self):
        """Test correct provider is selected"""
        import os
        expected_provider = os.getenv("LLM_PROVIDER", "anthropic")
        llm = LLMProvider()
        
        assert llm.provider == expected_provider
        print(f"✅ Provider correctly set to: {llm.provider}")
    
    def test_model_configuration(self):
        """Test model is properly configured"""
        llm = LLMProvider()
        
        assert llm.model is not None
        assert len(llm.model) > 0
        
        # Check model format based on provider
        if llm.provider == "anthropic":
            assert "claude" in llm.model.lower()
        elif llm.provider == "openai":
            assert "gpt" in llm.model.lower()
        
        print(f"✅ Model configured: {llm.model}")
    
    def test_api_key_validation(self):
        """Test API key is loaded"""
        llm = LLMProvider()
        
        assert llm.api_key is not None
        assert len(llm.api_key) > 10  # Basic validation
        print(f"✅ API key loaded (length: {len(llm.api_key)})")


def run_app_tests():
    """Run app tests"""
    pytest.main([__file__, '-v', '-s'])


if __name__ == "__main__":
    run_app_tests()