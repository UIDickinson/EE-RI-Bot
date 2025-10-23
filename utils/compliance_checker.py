"""Compliance and Standards Checker"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ComplianceChecker:
    def __init__(self):
        self.standards = {
            "CE": {
                "region": "EU",
                "directives": ["EMC", "LVD", "RoHS", "REACH", "RED"],
                "required_docs": ["DoC", "Technical File", "Risk Assessment"]
            },
            "FCC": {
                "region": "USA",
                "parts": ["Part 15", "Part 18"],
                "classes": ["Class A (Industrial)", "Class B (Residential)"]
            },
            "CCC": {
                "region": "China",
                "categories": ["Electronics", "Safety", "EMC"],
                "mandatory": True
            },
            "RoHS": {
                "region": "Global",
                "restricted_substances": ["Lead", "Mercury", "Cadmium", "Hexavalent chromium"],
                "exemptions": ["Medical", "Industrial monitoring"]
            }
        }
    
    def check_compliance(
        self,
        product_type: str,
        target_markets: List[str]
    ) -> Dict[str, Any]:
        """
        Check required compliance for product and markets
        """
        compliance_requirements = {
            "product_type": product_type,
            "target_markets": target_markets,
            "required_certifications": [],
            "estimated_timeline": {},
            "estimated_costs": {}
        }
        
        for market in target_markets:
            if market.upper() in ["EU", "EUROPE"]:
                compliance_requirements["required_certifications"].extend([
                    "CE Mark", "RoHS", "REACH"
                ])
                compliance_requirements["estimated_timeline"]["EU"] = "3-6 months"
                compliance_requirements["estimated_costs"]["EU"] = "€5,000-€15,000"
            
            elif market.upper() in ["USA", "US"]:
                compliance_requirements["required_certifications"].extend([
                    "FCC Part 15", "UL/ETL (optional)"
                ])
                compliance_requirements["estimated_timeline"]["USA"] = "2-4 months"
                compliance_requirements["estimated_costs"]["USA"] = "$3,000-$10,000"
            
            elif market.upper() in ["CHINA", "CN"]:
                compliance_requirements["required_certifications"].extend([
                    "CCC", "RoHS China"
                ])
                compliance_requirements["estimated_timeline"]["China"] = "4-8 months"
                compliance_requirements["estimated_costs"]["China"] = "$8,000-$20,000"
        
        # Remove duplicates
        compliance_requirements["required_certifications"] = list(set(
            compliance_requirements["required_certifications"]
        ))
        
        return compliance_requirements
    
    def get_emc_standards(self, product_category: str) -> List[str]:
        """
        Get applicable EMC standards for product category
        """
        emc_standards = {
            "consumer_electronics": ["EN 55032", "EN 55035", "EN 61000-3-2", "EN 61000-3-3"],
            "industrial": ["EN 61000-6-2", "EN 61000-6-4"],
            "automotive": ["CISPR 25", "ISO 11452"],
            "medical": ["IEC 60601-1-2"],
            "wireless": ["EN 301 489", "EN 300 328"]
        }
        
        return emc_standards.get(product_category, ["EN 55032 (Generic)"])