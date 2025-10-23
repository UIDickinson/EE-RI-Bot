"""Datasheet Parsing and Extraction"""

import pdfplumber
import re
import logging
from typing import Dict, Any, Optional, List
import requests
from io import BytesIO

logger = logging.getLogger(__name__)


class DatasheetParser:
    def __init__(self):
        self.spec_patterns = {
            "voltage": r"(\d+\.?\d*)\s*V(?:olts?)?",
            "current": r"(\d+\.?\d*)\s*(?:m|µ)?A(?:mps?)?",
            "frequency": r"(\d+\.?\d*)\s*(?:k|M|G)?Hz",
            "temperature": r"(-?\d+\.?\d*)\s*°?C",
            "power": r"(\d+\.?\d*)\s*(?:m|µ)?W(?:atts?)?",
            "efficiency": r"(\d+\.?\d*)\s*%\s*(?:efficiency|eff\.)"
        }
    
    def parse_pdf_datasheet(self, pdf_path_or_url: str) -> Dict[str, Any]:
        """
        Parse datasheet PDF and extract key specifications
        """
        try:
            if pdf_path_or_url.startswith('http'):
                response = requests.get(pdf_path_or_url, timeout=30)
                pdf_file = BytesIO(response.content)
            else:
                pdf_file = pdf_path_or_url
            
            extracted_data = {
                "specifications": {},
                "features": [],
                "applications": [],
                "raw_text": ""
            }
            
            with pdfplumber.open(pdf_file) as pdf:
                for page_num, page in enumerate(pdf.pages[:10]):  # First 10 pages
                    text = page.extract_text()
                    if text:
                        extracted_data["raw_text"] += text + "\n"
                        
                        if page_num == 0:
                            extracted_data["features"] = self._extract_features(text)
                            extracted_data["applications"] = self._extract_applications(text)
                        
                        specs = self._extract_specifications(text)
                        extracted_data["specifications"].update(specs)
            
            return extracted_data
        
        except Exception as e:
            logger.error(f"Datasheet parsing error: {e}")
            return {"error": str(e)}
    
    def _extract_specifications(self, text: str) -> Dict[str, List[str]]:
        """Extract numerical specifications from text"""
        specs = {}
        
        for spec_type, pattern in self.spec_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                specs[spec_type] = matches[:5]  # Top 5 matches
        
        return specs
    
    def _extract_features(self, text: str) -> List[str]:
        """Extract bullet-pointed features"""
        features = []
        lines = text.split('\n')
        
        for line in lines:
            if line.strip().startswith(('•', '-', '●', '◦')):
                feature = line.strip().lstrip('•-●◦ ').strip()
                if len(feature) > 10:
                    features.append(feature)
        
        return features[:15]
    
    def _extract_applications(self, text: str) -> List[str]:
        """Extract application keywords"""
        app_keywords = [
            "automotive", "industrial", "consumer", "medical", "IoT",
            "wearable", "battery-powered", "wireless", "motor control",
            "power supply", "LED driver", "sensor interface"
        ]
        
        applications = []
        text_lower = text.lower()
        
        for keyword in app_keywords:
            if keyword in text_lower:
                applications.append(keyword)
        
        return applications
    
    def extract_electrical_table(self, pdf_path: str, table_index: int = 0) -> Optional[List[List[str]]]:
        """Extract electrical characteristics table"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if tables and len(tables) > table_index:
                        return tables[table_index]
            return None
        except Exception as e:
            logger.error(f"Table extraction error: {e}")
            return None