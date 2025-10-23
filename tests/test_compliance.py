"""
Test compliance and utility modules
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.compliance_checker import ComplianceChecker
from utils.cost_estimator import CostEstimator


class TestComplianceChecker:
    """Test compliance checking functionality"""
    
    def setup_method(self):
        self.checker = ComplianceChecker()
    
    def test_initialization(self):
        """Test ComplianceChecker initializes"""
        assert self.checker is not None
        assert hasattr(self.checker, 'standards')
        assert 'CE' in self.checker.standards
        assert 'FCC' in self.checker.standards
        assert 'CCC' in self.checker.standards
    
    def test_check_compliance_eu(self):
        """Test EU compliance requirements"""
        result = self.checker.check_compliance(
            product_type="embedded_device",
            target_markets=["EU"]
        )
        
        assert isinstance(result, dict)
        assert 'required_certifications' in result
        assert 'CE Mark' in result['required_certifications']
        assert 'RoHS' in result['required_certifications']
        print(f"✅ EU compliance check: {result['required_certifications']}")
    
    def test_check_compliance_usa(self):
        """Test USA compliance requirements"""
        result = self.checker.check_compliance(
            product_type="wireless_device",
            target_markets=["USA"]
        )
        
        assert 'FCC Part 15' in result['required_certifications']
        print(f"✅ USA compliance check: {result['required_certifications']}")
    
    def test_check_compliance_china(self):
        """Test China compliance requirements"""
        result = self.checker.check_compliance(
            product_type="consumer_electronics",
            target_markets=["China"]
        )
        
        assert 'CCC' in result['required_certifications']
        print(f"✅ China compliance check: {result['required_certifications']}")
    
    def test_check_compliance_multiple_markets(self):
        """Test multiple market compliance"""
        result = self.checker.check_compliance(
            product_type="iot_device",
            target_markets=["EU", "USA", "China"]
        )
        
        assert len(result['required_certifications']) >= 3
        assert 'estimated_timeline' in result
        assert 'estimated_costs' in result
        print(f"✅ Multi-market compliance: {len(result['required_certifications'])} certifications required")
    
    def test_get_emc_standards(self):
        """Test EMC standards retrieval"""
        standards = self.checker.get_emc_standards("consumer_electronics")
        
        assert isinstance(standards, list)
        assert len(standards) > 0
        assert any("EN 55032" in s for s in standards)
        print(f"✅ EMC standards for consumer electronics: {standards}")


class TestCostEstimator:
    """Test cost estimation functionality"""
    
    def setup_method(self):
        self.estimator = CostEstimator()
    
    def test_initialization(self):
        """Test CostEstimator initializes"""
        assert self.estimator is not None
        assert hasattr(self.estimator, 'volume_discounts')
    
    def test_volume_discount_calculation(self):
        """Test volume discount factors"""
        test_cases = [
            (50, 1.0),
            (100, 1.0),
            (1000, 0.75),
            (10000, 0.55),
            (100000, 0.40)
        ]
        
        for volume, expected_discount in test_cases:
            discount = self.estimator._get_volume_discount(volume)
            assert discount == expected_discount
            print(f"✅ Volume {volume}: {discount}x discount")
    
    def test_estimate_bom_cost(self):
        """Test BOM cost estimation"""
        components = [
            {"part_number": "STM32H743", "unit_price": 8.50, "quantity": 1},
            {"part_number": "nRF52840", "unit_price": 3.20, "quantity": 1},
            {"part_number": "TPS54340", "unit_price": 1.80, "quantity": 2},
            {"part_number": "Resistor_0805", "unit_price": 0.01, "quantity": 20}
        ]
        
        result = self.estimator.estimate_bom_cost(
            components=components,
            volume=1000,
            region="EU"
        )
        
        assert isinstance(result, dict)
        assert 'total_cost' in result
        assert 'cost_per_unit' in result
        assert result['volume'] == 1000
        assert result['total_cost'] > 0
        print(f"✅ BOM cost for 1000 units: {result['currency']} {result['total_cost']}")
    
    def test_compare_alternatives(self):
        """Test alternative comparison"""
        alternative1 = [
            {"part_number": "STM32H743", "unit_price": 8.50, "quantity": 1},
            {"part_number": "Component_A", "unit_price": 2.00, "quantity": 1}
        ]
        
        alternative2 = [
            {"part_number": "ESP32-S3", "unit_price": 2.50, "quantity": 1},
            {"part_number": "Component_B", "unit_price": 1.50, "quantity": 1}
        ]
        
        result = self.estimator.compare_alternatives(
            component_alternatives=[alternative1, alternative2],
            volume=1000
        )
        
        assert isinstance(result, dict)
        assert 'alternatives' in result
        assert 'best_option' in result
        assert len(result['alternatives']) == 2
        print(f"✅ Cost comparison: Best option saves ${result['savings']}")


def run_compliance_tests():
    """Run compliance and utility tests"""
    pytest.main([__file__, '-v', '-s'])


if __name__ == "__main__":
    run_compliance_tests()