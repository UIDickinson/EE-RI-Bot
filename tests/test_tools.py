"""
Unit tests for all tool modules
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.research_tools import ResearchTools
from tools.component_tools import ComponentAnalyzer
from tools.supply_chain import SupplyChainTracker
from tools.datasheet_parser import DatasheetParser
from tools.patent_search import PatentSearcher
from tools.web_scraper import TechnicalWebScraper


class TestResearchTools:
    """Test research tools functionality"""
    
    def setup_method(self):
        self.research_tools = ResearchTools()
    
    def test_initialization(self):
        """Test ResearchTools initializes correctly"""
        assert self.research_tools is not None
        assert hasattr(self.research_tools, 'apis')
        assert hasattr(self.research_tools, 'priority_institutions')
    
    def test_search_arxiv(self):
        """Test arXiv search functionality"""
        results = self.research_tools._search_arxiv(
            "power management",
            "2023-2024"
        )
        assert isinstance(results, list)
        print(f"✅ arXiv search returned {len(results)} papers")
    
    def test_search_semantic_scholar(self):
        """Test Semantic Scholar search"""
        results = self.research_tools._search_semantic_scholar(
            "embedded systems",
            "2023-2024"
        )
        assert isinstance(results, list)
        print(f"✅ Semantic Scholar search returned {len(results)} papers")
    
    def test_search_research_papers(self):
        """Test full research paper search"""
        results = self.research_tools.search_research_papers(
            query="GaN transistors",
            domain="power_management",
            date_range="2023-2024"
        )
        
        assert isinstance(results, dict)
        assert 'papers' in results
        assert 'metadata' in results
        assert isinstance(results['papers'], list)
        print(f"✅ Full research search returned {len(results['papers'])} papers")


class TestComponentAnalyzer:
    """Test component analysis tools"""
    
    def setup_method(self):
        self.analyzer = ComponentAnalyzer()
    
    def test_initialization(self):
        """Test ComponentAnalyzer initializes"""
        assert self.analyzer is not None
        assert hasattr(self.analyzer, 'datasheet_sources')
    
    def test_detect_component_type(self):
        """Test component type detection"""
        test_cases = [
            ("STM32F407", "microcontroller"),
            ("ESP32-S3", "microcontroller"),
            ("TPS54340", "power_ic"),
            ("LM317", "power_ic"),
            ("BME280", "sensor"),
            ("UNKNOWN123", "unknown")
        ]
        
        for component_id, expected_type in test_cases:
            detected = self.analyzer._detect_component_type(component_id)
            assert detected == expected_type, f"Failed for {component_id}"
            print(f"✅ Correctly identified {component_id} as {expected_type}")
    
    def test_analyze_component(self):
        """Test component analysis"""
        result = self.analyzer.analyze_component(
            component_id="STM32H743",
            analysis_depth="deep_dive"
        )
        
        assert isinstance(result, dict)
        assert 'component' in result
        assert 'specifications' in result
        assert result['component'] == "STM32H743"
        print(f"✅ Component analysis completed for STM32H743")


class TestSupplyChainTracker:
    """Test supply chain tracking"""
    
    def setup_method(self):
        self.tracker = SupplyChainTracker()
    
    def test_initialization(self):
        """Test SupplyChainTracker initializes"""
        assert self.tracker is not None
        assert hasattr(self.tracker, 'distributors')
        assert 'EU' in self.tracker.distributors
        assert 'Asia' in self.tracker.distributors
    
    def test_check_availability(self):
        """Test availability checking"""
        components = ["STM32F407", "ESP32-S3", "nRF52840"]
        result = self.tracker.check_availability(
            components=components,
            region="both"
        )
        
        assert isinstance(result, dict)
        assert 'components' in result
        assert 'region' in result
        assert result['region'] == "both"
        assert len(result['components']) == len(components)
        print(f"✅ Availability check completed for {len(components)} components")


class TestDatasheetParser:
    """Test datasheet parsing functionality"""
    
    def setup_method(self):
        self.parser = DatasheetParser()
    
    def test_initialization(self):
        """Test DatasheetParser initializes"""
        assert self.parser is not None
        assert hasattr(self.parser, 'spec_patterns')
        assert 'voltage' in self.parser.spec_patterns
        assert 'current' in self.parser.spec_patterns
    
    def test_extract_specifications(self):
        """Test specification extraction from text"""
        test_text = """
        Operating Voltage: 3.3V to 5.5V
        Current Consumption: 150mA typical, 200mA max
        Frequency: 168MHz
        Temperature Range: -40°C to +85°C
        Efficiency: 95% at full load
        Power Dissipation: 2.5W maximum
        """
        
        specs = self.parser._extract_specifications(test_text)
        
        assert isinstance(specs, dict)
        assert 'voltage' in specs
        assert 'current' in specs
        assert 'frequency' in specs
        assert 'temperature' in specs
        print(f"✅ Extracted {len(specs)} specification types from text")
    
    def test_extract_features(self):
        """Test feature extraction"""
        test_text = """
        Key Features:
        • Ultra-low power consumption
        • Integrated Bluetooth 5.0
        • Hardware AES encryption
        • 12-bit ADC with 16 channels
        • RTC with calendar
        """
        
        features = self.parser._extract_features(test_text)
        
        assert isinstance(features, list)
        assert len(features) > 0
        print(f"✅ Extracted {len(features)} features")
    
    def test_extract_applications(self):
        """Test application keyword extraction"""
        test_text = """
        Typical Applications:
        - Automotive sensor interfaces
        - Industrial IoT devices
        - Battery-powered wearables
        - Wireless sensor networks
        - Medical monitoring devices
        """
        
        applications = self.parser._extract_applications(test_text)
        
        assert isinstance(applications, list)
        assert 'automotive' in applications
        assert 'industrial' in applications
        print(f"✅ Extracted {len(applications)} application areas")


class TestPatentSearcher:
    """Test patent search functionality"""
    
    def setup_method(self):
        self.searcher = PatentSearcher()
    
    def test_initialization(self):
        """Test PatentSearcher initializes"""
        assert self.searcher is not None
        assert hasattr(self.searcher, 'google_patents_api')
    
    def test_search_patents(self):
        """Test patent search"""
        results = self.searcher.search_patents(
            query="GaN power transistor",
            country_codes=["US", "EP"],
            date_from="2022-01-01",
            max_results=10
        )
        
        assert isinstance(results, dict)
        assert 'patents' in results
        assert 'total_found' in results
        assert 'query' in results
        print(f"✅ Patent search completed, found {results['total_found']} patents")
    
    def test_analyze_patent_trends(self):
        """Test patent trend analysis"""
        mock_patents = [
            {"assignee": "Company A", "filing_date": "2023-01-01"},
            {"assignee": "Company A", "filing_date": "2023-02-01"},
            {"assignee": "Company B", "filing_date": "2023-03-01"}
        ]
        
        analysis = self.searcher.analyze_patent_trends(
            patents=mock_patents,
            domain="power_management"
        )
        
        assert isinstance(analysis, dict)
        assert 'total_patents' in analysis
        assert 'top_assignees' in analysis
        assert analysis['total_patents'] == 3
        print(f"✅ Patent trend analysis completed")


class TestTechnicalWebScraper:
    """Test web scraping functionality"""
    
    def setup_method(self):
        self.scraper = TechnicalWebScraper()
    
    def test_initialization(self):
        """Test TechnicalWebScraper initializes"""
        assert self.scraper is not None
        assert hasattr(self.scraper, 'trusted_sources')
        assert len(self.scraper.trusted_sources) > 0
    
    def test_extract_component_info(self):
        """Test component info extraction"""
        result = self.scraper.extract_component_info("STM32F407")
        
        assert isinstance(result, dict)
        assert 'component' in result
        assert result['component'] == "STM32F407"
        print(f"✅ Component info extraction completed")


def run_all_tests():
    """Run all tests with pytest"""
    pytest.main([__file__, '-v', '-s'])


if __name__ == "__main__":
    run_all_tests()