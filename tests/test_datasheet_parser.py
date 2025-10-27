"""
Test datasheet parser functionality
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.datasheet_parser import DatasheetParser


class TestDatasheetParser:
    """Test datasheet parsing"""
    
    def setup_method(self):
        self.parser = DatasheetParser()
    
    def test_initialization(self):
        """Test parser initializes"""
        assert self.parser is not None
        assert hasattr(self.parser, 'spec_patterns')
        print("✅ DatasheetParser initialized")
    
    def test_extract_voltage_specs(self):
        """Test voltage extraction"""
        text = """
        Operating Voltage: 3.3V to 5.5V
        Supply Voltage: 12V DC
        Output: 24V
        """
        
        specs = self.parser._extract_specifications(text)
        
        assert 'voltage' in specs
        assert len(specs['voltage']) > 0
        print(f"✅ Extracted voltages: {specs['voltage']}")
    
    def test_extract_current_specs(self):
        """Test current extraction"""
        text = """
        Current Consumption: 150mA typical
        Max Current: 500mA
        Quiescent Current: 10µA
        """
        
        specs = self.parser._extract_specifications(text)
        
        assert 'current' in specs
        assert len(specs['current']) > 0
        print(f"✅ Extracted currents: {specs['current']}")
    
    def test_extract_frequency_specs(self):
        """Test frequency extraction"""
        text = """
        Clock Frequency: 168MHz
        Operating Range: 50kHz to 2.4GHz
        """
        
        specs = self.parser._extract_specifications(text)
        
        assert 'frequency' in specs
        print(f"✅ Extracted frequencies: {specs['frequency']}")
    
    def test_extract_temperature_specs(self):
        """Test temperature extraction"""
        text = """
        Operating Temperature: -40°C to +85°C
        Storage: -55°C to +125°C
        """
        
        specs = self.parser._extract_specifications(text)
        
        assert 'temperature' in specs
        print(f"✅ Extracted temperatures: {specs['temperature']}")
    
    def test_extract_multiple_specs(self):
        """Test extracting multiple spec types"""
        text = """
        Supply Voltage: 3.3V
        Current Consumption: 25mA
        Operating Frequency: 100MHz
        Temperature Range: -40°C to 85°C
        Power Consumption: 82mW
        Efficiency: 92%
        """
        
        specs = self.parser._extract_specifications(text)
        
        assert len(specs) >= 5  # Should find most spec types
        print(f"✅ Extracted {len(specs)} spec types")
    
    def test_extract_features_with_bullets(self):
        """Test feature extraction with bullet points"""
        text = """
        Key Features:
        • Low power consumption
        • Integrated ADC
        • Hardware encryption
        • Real-time clock
        • DMA controller
        """
        
        features = self.parser._extract_features(text)
        
        assert len(features) >= 3
        assert any("power" in f.lower() for f in features)
        print(f"✅ Extracted {len(features)} features")
    
    def test_extract_applications(self):
        """Test application keyword extraction"""
        text = """
        Applications:
        - Automotive sensor interfaces
        - Industrial automation
        - IoT edge devices
        - Medical monitoring
        - Battery-powered systems
        """
        
        apps = self.parser._extract_applications(text)
        
        assert len(apps) > 0
        assert "automotive" in apps
        assert "industrial" in apps
        print(f"✅ Extracted applications: {apps}")
    
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        specs = self.parser._extract_specifications("")
        features = self.parser._extract_features("")
        apps = self.parser._extract_applications("")
        
        assert isinstance(specs, dict)
        assert isinstance(features, list)
        assert isinstance(apps, list)
        print("✅ Empty text handled gracefully")


def run_parser_tests():
    """Run datasheet parser tests"""
    pytest.main([__file__, '-v', '-s'])


if __name__ == "__main__":
    run_parser_tests()