"""
Integration tests for end-to-end functionality
"""

import pytest
import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import EEResearchScout


class TestIntegration:
    """Integration tests for complete workflows"""
    
    def setup_method(self):
        self.agent = EEResearchScout(name="test-agent")
    
    def test_agent_initialization(self):
        """Test agent initializes with all components"""
        assert self.agent is not None
        assert self.agent.llm is not None
        assert self.agent.research_tools is not None
        assert self.agent.component_analyzer is not None
        assert self.agent.supply_chain is not None
        print("✅ Agent initialized with all components")
    
    @pytest.mark.asyncio
    async def test_query_analysis(self):
        """Test query analysis pipeline"""
        test_queries = [
            "Find latest GaN power ICs for automotive",
            "Compare STM32H7 vs ESP32-S3",
            "Check availability of nRF52840 in EU"
        ]
        
        for query in test_queries:
            result = await self.agent._analyze_query(query)
            
            assert isinstance(result, dict)
            assert 'domains' in result
            assert 'strategy' in result
            print(f"✅ Analyzed query: '{query[:50]}...'")
            print(f"   Domains: {result['domains']}")
            print(f"   Strategy: {result['strategy']}")
    
    @pytest.mark.asyncio
    async def test_research_pipeline(self):
        """Test research search pipeline"""
        result = await self.agent._search_research(
            query="GaN transistors power management",
            domains=["power_management"]
        )
        
        assert isinstance(result, dict)
        assert 'papers' in result
        assert 'metadata' in result
        print(f"✅ Research pipeline completed")
        print(f"   Papers found: {len(result.get('papers', []))}")
    
    @pytest.mark.asyncio
    async def test_component_analysis_pipeline(self):
        """Test component analysis pipeline"""
        components = ["STM32H743", "ESP32-S3"]
        result = await self.agent._analyze_components(components)
        
        assert isinstance(result, dict)
        assert len(result) <= len(components)
        print(f"✅ Component analysis pipeline completed")
        print(f"   Analyzed: {list(result.keys())}")
    
    def test_domain_priorities(self):
        """Test domain priority configuration"""
        assert 'embedded_systems' in self.agent.domain_priorities
        assert 'power_management' in self.agent.domain_priorities
        assert self.agent.domain_priorities['embedded_systems'] == 1.0
        print(f"✅ Domain priorities configured: {len(self.agent.domain_priorities)} domains")


def run_integration_tests():
    """Run integration tests"""
    pytest.main([__file__, '-v', '-s'])


if __name__ == "__main__":
    run_integration_tests()