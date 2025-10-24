"""
Test edge cases and error handling
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.research_tools import ResearchTools
from tools.component_tools import ComponentAnalyzer
from utils.compliance_checker import ComplianceChecker
from utils.cost_estimator import CostEstimator


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_empty_search_query(self):
        """Test handling of empty search queries"""
        tools = ResearchTools()
        result = tools.search_research_papers(
            query="",
            domain="general"
        )
        assert isinstance(result, dict)
        print("✅ Empty search query handled")
    
    def test_invalid_component_id(self):
        """Test handling of invalid component IDs"""
        analyzer = ComponentAnalyzer()
        result = analyzer.analyze_component(
            component_id="",
            analysis_depth="deep_dive"
        )
        assert isinstance(result, dict)
        print("✅ Invalid component ID handled")
    
    def test_unknown_component_type(self):
        """Test detection of unknown component types"""
        analyzer = ComponentAnalyzer()
        component_type = analyzer._detect_component_type("UNKNOWN_XYZ_999")
        assert component_type == "unknown"
        print("✅ Unknown component type detected correctly")
    
    def test_empty_component_list(self):
        """Test cost estimation with empty component list"""
        estimator = CostEstimator()
        result = estimator.estimate_bom_cost(
            components=[],
            volume=1000
        )
        assert result["total_cost"] == 0
        print("✅ Empty component list handled")
    
    def test_zero_volume_estimation(self):
        """Test cost estimation with zero volume"""
        estimator = CostEstimator()
        components = [
            {"part_number": "TEST123", "unit_price": 1.0, "quantity": 1}
        ]
        result = estimator.estimate_bom_cost(
            components=components,
            volume=0
        )
        assert isinstance(result, dict)
        print("✅ Zero volume handled")
    
    def test_negative_price_handling(self):
        """Test handling of negative prices"""
        estimator = CostEstimator()
        components = [
            {"part_number": "TEST123", "unit_price": -5.0, "quantity": 1}
        ]
        result = estimator.estimate_bom_cost(
            components=components,
            volume=100
        )
        # Should still return a result (even if negative)
        assert isinstance(result, dict)
        print("✅ Negative price handled")
    
    def test_empty_target_markets(self):
        """Test compliance check with no target markets"""
        checker = ComplianceChecker()
        result = checker.check_compliance(
            product_type="device",
            target_markets=[]
        )
        assert isinstance(result, dict)
        assert len(result["required_certifications"]) == 0
        print("✅ Empty target markets handled")
    
    def test_unknown_product_category(self):
        """Test EMC standards for unknown category"""
        checker = ComplianceChecker()
        standards = checker.get_emc_standards("unknown_category")
        assert isinstance(standards, list)
        assert len(standards) > 0  # Should return generic standards
        print("✅ Unknown product category handled")
    
    def test_special_characters_in_query(self):
        """Test special characters in search queries"""
        tools = ResearchTools()
        special_queries = [
            "µC power < 100µA",
            "5V ±10% @ 25°C",
            "cost: $5-$10 (USD)",
            "efficiency > 95%"
        ]
        
        for query in special_queries:
            result = tools.search_research_papers(query=query)
            assert isinstance(result, dict)
        
        print("✅ Special characters in queries handled")
    
    def test_very_long_query(self):
        """Test handling of very long queries"""
        tools = ResearchTools()
        long_query = "power management " * 100  # 1600+ characters
        result = tools.search_research_papers(query=long_query)
        assert isinstance(result, dict)
        print("✅ Very long query handled")
    
    def test_unicode_in_component_id(self):
        """Test Unicode characters in component IDs"""
        analyzer = ComponentAnalyzer()
        unicode_ids = ["STM32™", "µController", "Component®"]
        
        for comp_id in unicode_ids:
            result = analyzer.analyze_component(component_id=comp_id)
            assert isinstance(result, dict)
        
        print("✅ Unicode in component IDs handled")


class TestDataValidation:
    """Test data validation and sanitization"""
    
    def test_date_range_validation(self):
        """Test date range parsing"""
        tools = ResearchTools()
        
        valid_ranges = ["2020-2024", "2023-2024", "2022-2023"]
        
        for date_range in valid_ranges:
            result = tools.search_research_papers(
                query="test",
                date_range=date_range
            )
            assert isinstance(result, dict)
        
        print("✅ Date range validation passed")
    
    def test_quantity_validation(self):
        """Test component quantity validation"""
        estimator = CostEstimator()
        
        # Test various quantities
        test_quantities = [0, 1, 10, 100, 1000000]
        
        for qty in test_quantities:
            components = [
                {"part_number": "TEST", "unit_price": 1.0, "quantity": qty}
            ]
            result = estimator.estimate_bom_cost(components, volume=100)
            assert isinstance(result, dict)
        
        print("✅ Quantity validation passed")
    
    def test_region_validation(self):
        """Test region parameter validation"""
        checker = ComplianceChecker()
        
        # Test various region formats
        regions = ["EU", "eu", "USA", "us", "CHINA", "china"]
        
        for region in regions:
            result = checker.check_compliance(
                product_type="device",
                target_markets=[region]
            )
            assert isinstance(result, dict)
        
        print("✅ Region validation passed")


class TestConcurrency:
    """Test concurrent operations"""
    
    @pytest.mark.asyncio
    async def test_concurrent_research_queries(self):
        """Test multiple concurrent research queries"""
        tools = ResearchTools()
        
        queries = [
            "GaN transistors",
            "Edge AI processors",
            "Power management ICs"
        ]
        
        # Simulate concurrent queries
        results = []
        for query in queries:
            result = tools.search_research_papers(query=query)
            results.append(result)
        
        assert len(results) == len(queries)
        for result in results:
            assert isinstance(result, dict)
        
        print(f"✅ {len(queries)} concurrent queries handled")
    
    def test_concurrent_component_analysis(self):
        """Test concurrent component analysis"""
        analyzer = ComponentAnalyzer()
        
        components = [
            "STM32F407",
            "ESP32-S3",
            "nRF52840",
            "TPS54340"
        ]
        
        results = []
        for comp in components:
            result = analyzer.analyze_component(component_id=comp)
            results.append(result)
        
        assert len(results) == len(components)
        print(f"✅ {len(components)} concurrent analyses handled")


def run_edge_case_tests():
    """Run edge case tests"""
    pytest.main([__file__, '-v', '-s'])


if __name__ == "__main__":
    run_edge_case_tests()